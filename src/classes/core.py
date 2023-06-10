from random import choice, shuffle
from math import ceil
from ..road.road_network import RoadNetwork, RoadEdge
from ..level.limit import getResourceLimit, getBuildingLimit
from ..resource.terrain_analyzer import Resource
from gdpc import Editor
from gdpc.vector_tools import addY, dropY, Rect, Box, ivec2, ivec3, neighbors2D
from typing import Literal, Any, Callable
import numpy as np
from .event import Subject, BuildEvent, UpgradeEvent
from ..building.building import Building
from ..height_info import HeightInfo
from ..resource.terrain_analyzer import ResourceMap
from ..config.config import config
from ..building.nbt_builder import buildFromNBT
from ..resource.biome_substitute import getChangeMaterial
from ..resource.analyze_biome import BiomeMap
from ..poisson_disk_sampling import poissonDiskSample
from ..road.road_network import RoadNode

UNIT = config.unit
ROAD = -1
ROAD_RESERVE = -2


def hashfunc(o: object) -> int:
    return o.to_tuple().__hash__() if isinstance(o, ivec2) else o.__hash__()


class Core():

    def __init__(self, buildArea: Box = config.buildArea) -> None:
        """
        the core will connect with the game
        """
        # initalize editor
        editor = Editor(buffering=config.buffering,
                        bufferLimit=config.bufferLimit,
                        caching=config.caching, host=config.host)
        editor.doBlockUpdates = config.doBlockUpdates
        buildArea = editor.getBuildArea()
        # get world slice and height maps
        print("Loading world slice...")
        worldSlice = editor.loadWorldSlice(buildArea.toRect(), cache=True)
        print("World slice loaded")

        heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

        # get top left and bottom right coordnidate
        x, _, z = buildArea.size

        self._buildArea = buildArea
        self._editor = editor
        self._worldSlice = worldSlice
        self._roadMap = np.zeros((x, z), dtype=int)
        self._liquidMap = np.where(
            worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] > worldSlice.heightmaps["OCEAN_FLOOR"], 1, 0)

        print("Analyzing biome...")
        self._biomeMap = BiomeMap(worldSlice)
        print("Biome analyzed")

        print("Analyzing resource...")
        self._resourceMap = ResourceMap(self.worldSlice)
        self._resources = self._resourceMap.analyzeResource()
        print(self._resourceMap)
        print(self._resources)
        print("Resource analyzed")

        # contains: height, sd, var, mean
        self._heightInfo = HeightInfo(heights)
        self._blueprint = np.zeros(
            (x // UNIT, z // UNIT), dtype=int)  # unit is 2x2
        self._blueprintData: dict[int, Building] = {}
        # init level is 1, and get resource limit and building limit of level 1
        self._level = int(1)
        self._roadNetwork = RoadNetwork[ivec2](
            hashfunc=lambda o: o.to_tuple().__hash__() if isinstance(o, ivec2) else o.__hash__())

        self.buildSubject = Subject[BuildEvent]()
        self.upgradeSubject = Subject[UpgradeEvent]()

        self.emptyAreaPrefix = np.zeros_like(self.blueprint)

    @property
    def buildArea(self):
        return self._buildArea

    @property
    def editor(self):
        return self._editor

    @property
    def worldSlice(self):
        return self._worldSlice

    @property
    def roadMap(self):
        return self._roadMap

    @property
    def liquidMap(self):
        return self._liquidMap

    @property
    def biomeMap(self):
        return self._biomeMap

    @property
    def resources(self):
        return self._resources

    @property
    def resourcesMap(self):
        return self._resourceMap

    @property
    def blueprint(self):
        return self._blueprint

    @property
    def blueprintData(self):
        return self._blueprintData

    @property
    def roadNetwork(self):
        return self._roadNetwork

    @property
    def level(self):
        return self._level

    @property
    def resourceLimit(self):
        return getResourceLimit(self._level)

    def getBuildings(self, buildingLevel: int | None = None, buildingType: str | None = None):
        for building in self._blueprintData.values():
            if (buildingLevel is None or building.level == buildingLevel) and \
                    (buildingType is None or building.building_info.type == buildingType):
                yield building

    def getBuildingLimit(self, buildingLevel: int):
        return getBuildingLimit(self._level, buildingLevel)

    def numberOfBuildings(self, buildingLevel: int = 0):
        if buildingLevel == 0:
            return len(self._blueprintData)
        return len([building for building in self._blueprintData.values() if building.level == buildingLevel])

    def canBuildOrUpgradeTo(self, buildingLevel: int):
        """
        Check if the core can build or upgrade a building of the given level\n
        level 1 is the lowest level for build\n
        level 2 or higher is for upgrade
        """
        return self.numberOfBuildings(buildingLevel) < self.getBuildingLimit(buildingLevel)

    def updateResource(self):
        for _, building in self.blueprintData.items():
            buildingLevel = building.level
            self._resources += building.building_info.structures[buildingLevel-1].production

    def getBlueprintBuildingData(self, id: int):
        return self._blueprintData.get(id, None)

    def maxBuildingID(self):
        ids = self._blueprintData.keys()
        return max(ids) if ids else 0

    def increaseGrass(self):
        self._resources.grass += 10

    def addBuilding(self, building: Building):
        """Append a building on to the blueprint. We trust our agent, if there's any overlap, it's agent's fault."""
        (x, z) = building.position
        (xlen, _, zlen) = building.maxSize
        id = self.maxBuildingID() + 1
        x = x // UNIT
        z = z // UNIT
        xlen = ceil(xlen / UNIT)
        zlen = ceil(zlen / UNIT)

        building.id = id

        biome = self.biomeMap.getPrimaryBiome(
            Rect((x * UNIT, z * UNIT), (xlen * UNIT, z * UNIT)))
        building.material = getChangeMaterial(biome)

        area = Rect((x, z), (xlen, zlen))
        begin, end = area.begin, area.end

        self._blueprintData[id] = building
        self._blueprint[begin.x:end.x, begin.y:end.y] = id

        area.dilate(1)
        begin, end = area.begin, area.end

        for (x, z) in area.outline:
            self._blueprint[x, z] = ROAD_RESERVE

        self.updateEmptyArea()

    def addRoadEdge(self, edge: RoadEdge[ivec2]):
        self._roadNetwork.addEdge(edge)
        for node in edge.path:
            x, z = node.val // UNIT
            self._blueprint[x, z] = ROAD

    def removeBuilding(self, id: int):
        building = self._blueprintData[id]
        (x, z) = building.position
        (xlen, _, zlen) = building.maxSize
        x = x // UNIT
        z = z // UNIT
        xlen = ceil(xlen / UNIT)
        zlen = ceil(zlen / UNIT)

        area = Rect((x, z), (xlen, zlen))
        begin, end = area.begin, area.end

        self._blueprintData.pop(id)
        self._blueprint[begin.x:end.x, begin.y:end.y] = 0

        area.dilate(1)
        begin, end = area.begin, area.end

        for (x, z) in area.outline:
            for neighbor in neighbors2D((x, z), self.buildArea.toRect()):
                if self._blueprint[neighbor.to_tuple()] != 0:
                    continue
            self._blueprint[x, z] = 0

    def getHeightMap(self, heightType: Literal["var", "mean", "sum", "squareSum", "std"], bound: Rect):
        if heightType == "var":
            return self._heightInfo.var(bound)
        if heightType == "mean":
            return self._heightInfo.mean(bound)
        if heightType == "sum":
            return self._heightInfo.sum(bound)
        if heightType == "squareSum":
            return self._heightInfo.squareSum(bound)
        if heightType == "std":
            return self._heightInfo.std(bound)
        raise Exception("This type does not exist on heightType")

    def updateEmptyArea(self):
        def isEmpty(val: Any):
            if val == 0:
                return 0
            return 1

        prefix = np.zeros_like(self.blueprint)
        h, w = prefix.shape[:2]

        prefix[0][0] = isEmpty(self.blueprint[0][0])

        for i in range(1, h):
            prefix[i][0] = prefix[i - 1][0] + isEmpty(self.blueprint[i][0])

        for i in range(1, w):
            prefix[0][i] = prefix[0][i - 1] + isEmpty(self.blueprint[0][i])

        # probably can figure out a way to cache this
        for i in range(1, h):
            for j in range(1, w):
                prefix[i][j] = prefix[i - 1][j] + prefix[i][j - 1] - \
                    prefix[i - 1][j - 1] + isEmpty(self.blueprint[i][j])

        self.emptyAreaPrefix = prefix
        pass

    def getEmptyArea(self, size: ivec2) -> list[Rect]:
        height, width = size
        height = ceil(height / UNIT)
        width = ceil(width / UNIT)
        blueprintHeight, blueprintWidth = self.emptyAreaPrefix.shape[:2]

        result: list[Rect] = []

        for i in range(blueprintHeight - height):
            for j in range(blueprintWidth - width):
                lh = i + height
                lw = j + width
                left = 0
                top = 0
                leftTop = 0
                if i > 0:
                    top = self.emptyAreaPrefix[i - 1][lw]
                if j > 0:
                    left = self.emptyAreaPrefix[lh][j - 1]
                if i > 0 and j > 0:
                    leftTop = self.emptyAreaPrefix[i - 1][j - 1]

                used = self.emptyAreaPrefix[lh][lw] - top - left + leftTop
                if used == 0:
                    result.append(Rect((i * UNIT, j * UNIT),
                                  (height * UNIT, width * UNIT)))

        return result

    def getMostLackResource(self, existResource: Resource, limitResource: Resource) -> str:
        """ return one lack resource name(str) which is the most shortage"""
        lack: list[tuple[int, str]] = []
        lack.append((limitResource.human - existResource.human, str("human")))
        lack.append((limitResource.wood - existResource.wood, str("wood")))
        lack.append((limitResource.stone - existResource.stone, str("stone")))
        lack.append((limitResource.ironOre -
                    existResource.ironOre, str("ironOre")))
        lack.append((limitResource.iron - existResource.iron, str("iron")))
        lack.append((limitResource.food - existResource.food, str("food")))
        maxlack: tuple[int, str] = max(lack)
        if maxlack[0] <= 0:
            return str("none")
        return maxlack[1]

    def levelUp(self):
        """"level up and update resource limit and building limit"""
        self._level += 1

    def conformToResourceLimit(self):
        """
            Conform the resources to the resource limit, and this method should be called every round.
            if resource.item > resourceLimit.item, resource.item = resourceLimit.item
            else resource.item = resource.item
        """
        self.resources.human = min(
            self.resourceLimit.human, self._resources.human)
        self.resources.wood = min(
            self.resourceLimit.wood, self._resources.wood)
        self.resources.stone = min(
            self.resourceLimit.stone, self._resources.stone)
        self.resources.food = min(
            self.resourceLimit.food, self._resources.food)
        self.resources.ironOre = min(
            self.resourceLimit.ironOre, self._resources.ironOre)
        self.resources.iron = min(
            self.resourceLimit.iron, self._resources.iron)

    def startBuildingInMinecraft(self):
        """Send the blueprint to Minecraft"""

        globalBound = self.buildArea.toRect()
        globalOffset = globalBound.offset
        localBound = globalBound.translated(-globalOffset)

        sureRoadHeights = dict[RoadNode[ivec2], int]()

        # ====== Add building to Minecraft ======

        for id, building in self._blueprintData.items():
            pos = building.position
            level = building.level
            structure = building.building_info.structures[level-1]
            size = building.building_info.max_size
            area = Rect(pos, dropY(size))
            y = round(self.getHeightMap("mean", area))
            print(f"Build at {pos + globalOffset} with height {y}")
            buildFromNBT(self._editor, structure.nbtFile, addY(globalOffset),
                         addY(pos, y) + structure.offsets, building.material)

            if building.entryPos is not None:
                x, z = building.entryPos
                x, z = (x//UNIT)*UNIT, (z//UNIT)*UNIT
                sureRoadHeights[self.roadNetwork.newNode(ivec2(x, z))] = y

        self.editor.flushBuffer()

        # ====== Add road to Minecraft ======

        # Fix the road height

        for edge in self._roadNetwork.edges:
            lastY = None
            for node in edge:
                if node in sureRoadHeights:
                    lastY = sureRoadHeights[node]
                    continue
                if lastY is None:
                    break
                area = Rect(node.val, (UNIT, UNIT))
                y = round(self.getHeightMap("mean", area))
                delta = y - lastY
                if abs(delta) > 1:
                    delta = delta // abs(delta)
                    y = lastY + delta
                else:
                    break
                sureRoadHeights[node] = y
                lastY = y

        # Build the road

        roadNodes = set(self._roadNetwork.subnodes)
        for node in roadNodes:
            area = Rect(node.val, (UNIT, UNIT))

            if node in sureRoadHeights:
                y = sureRoadHeights[node]
            else:
                y = round(self.getHeightMap("mean", area))

            sureRoadHeights[node] = y
            pos = addY(node.val+globalOffset, y)

            clearBox = area.toBox(y, 2)
            for x, y, z in clearBox.inner:
                block = self.worldSlice.getBlock((x, y, z))
                if block.id != "minecraft:air":
                    begin, last = clearBox.begin + \
                        addY(globalOffset, 0), clearBox.last + \
                        addY(globalOffset, 0)
                    self.editor.runCommand(
                        f"fill {begin.x} {begin.y} {begin.z} {last.x} {last.y} {last.z} minecraft:air", syncWithBuffer=True)
                    break

            self.editor.runCommand(
                f"fill {pos.x} {pos.y-1} {pos.z} {pos.x+1} {pos.y-1} {pos.z+1} {config.roadMaterial}", syncWithBuffer=True)

        self.editor.flushBuffer()

        # ====== Add light to Minecraft ======

        def sampleRoadNode(point: ivec2, r: int):
            return choice(list(roadNodes)).val

        def placeLight1(point: ivec3):
            x, y, z = point
            self.editor.runCommand(
                f"setblock {x} {y-1} {z} minecraft:cobblestone", syncWithBuffer=True)
            self.editor.runCommand(
                f"setblock {x} {y} {z} minecraft:oak_fence", syncWithBuffer=True)
            self.editor.runCommand(
                f"setblock {x} {y+1} {z} minecraft:lantern", syncWithBuffer=True)

        def placeLight2(point: ivec3):
            x, y, z = point
            self.editor.runCommand(
                f"setblock {x} {y-1} {z} minecraft:cobblestone", syncWithBuffer=True)
            self.editor.runCommand(
                f"setblock {x} {y} {z} minecraft:cobblestone_wall", syncWithBuffer=True)
            self.editor.runCommand(
                f"setblock {x} {y+1} {z} minecraft:torch", syncWithBuffer=True)

        lightPositions = poissonDiskSample(
            bound=localBound,
            limit=len(roadNodes)//3,
            r=10,
            k=50,
            sampleFunc=sampleRoadNode,
            initPoints=list([roadNode.val for roadNode in roadNodes])
        )

        for pos in lightPositions:
            node = self.roadNetwork.newNode(pos)
            y = sureRoadHeights[node]
            neighbors = list(neighbors2D(pos, localBound, stride=UNIT))
            shuffle(neighbors)
            for neighbor in neighbors:
                x, z = neighbor
                if self.blueprint[x//UNIT, z//UNIT] == 0:

                    if x-pos.x < 0:
                        x = pos.x - 1
                    if z-pos.y < 0:
                        z = pos.y - 1

                    choice([placeLight1, placeLight2])(
                        (x, y, z) + addY(globalOffset, 0))
                    break

        self.editor.flushBuffer()
