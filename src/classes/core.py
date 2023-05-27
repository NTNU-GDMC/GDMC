from gdpc import Editor
from gdpc.vector_tools import addY, dropY, Rect, Box
from typing import Literal, Any
import numpy as np
from .event import Subject, BuildEvent, UpgradeEvent
from ..building.building import Building
from ..height_info import HeightInfo
from ..resource.analyze_biome import getAllBiomeList
from ..resource.terrain_analyzer import analyzeAreaMaterialToResource, getMaterialToResourceMap
from ..config.config import config
from ..building.nbt_builder import buildFromNBT

UNIT = config.unit


class Core():

    def __init__(self, buildArea: Box = config.buildArea) -> None:
        """
        the core will connect with the game
        """
        # initalize editor
        editor = Editor(buffering=config.buffering, caching=config.caching)
        editor.doBlockUpdates = config.doBlockUpdates
        buildArea = editor.setBuildArea(buildArea)
        # get world slice and height maps
        worldSlice = editor.loadWorldSlice(buildArea.toRect(), cache=True)
        heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

        # get top left and bottom right coordnidate
        x, _, z = buildArea.size

        self._buildArea = buildArea
        self._editor = editor
        self._worldSlice = worldSlice
        self._roadMap = np.zeros((x, z), dtype=int)
        self._liquidMap = np.where(
            worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] > worldSlice.heightmaps["OCEAN_FLOOR"], 1, 0)
        self._biomeList = getAllBiomeList(worldSlice, buildArea)
        self._resources = analyzeAreaMaterialToResource(
            worldSlice, buildArea.toRect())
        self._resourceMap = getMaterialToResourceMap(
            worldSlice, buildArea.toRect())
        # contains: height, sd, var, mean
        self._heightInfo = HeightInfo(heights)
        self._blueprint = np.zeros(
            (x // UNIT, z // UNIT), dtype=int)  # unit is 2x2
        self._blueprintData: dict[int, Building] = {}
        self.buildSubject = Subject[BuildEvent]()
        self.upgradeSubject = Subject[UpgradeEvent]()

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
    def biomeList(self):
        return self._biomeList

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

    def getBlueprintBuildingData(self, id: int):
        return self._blueprintData[id]

    def addBuilding(self, building: Building):
        """Append a building on to the blueprint. We trust our agent, if there's any overlap, it's agent's fault."""
        (x, z) = building.position
        (xlen, _, zlen) = building.dimension
        id = len(self._blueprintData) + 1
        x = (x + UNIT) // UNIT
        z = (z + UNIT) // UNIT
        xlen = (xlen + UNIT) // UNIT
        zlen = (zlen + UNIT) // UNIT

        self._blueprintData[id] = building
        self._blueprint[x:x + xlen, z:z + zlen] = id

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

    def getEmptyArea(self, height: int, width: int) -> list[Rect]:
        height = (height + UNIT) // UNIT
        width = (width + UNIT) // UNIT

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
        result: list[Rect] = []

        for i in range(h - height):
            for j in range(w - width):
                lh = i + height
                lw = j + width
                left = 0
                top = 0
                leftTop = 0
                if i > 0:
                    top = prefix[i - 1][lw]
                if j > 0:
                    left = prefix[lh][j - 1]
                if i > 0 and j > 0:
                    leftTop = prefix[i - 1][j - 1]

                used = prefix[lh][lw] - top - left + leftTop
                if used == 0:
                    result.append(Rect((i * UNIT, j * UNIT),
                                  (height * UNIT, height * UNIT)))

        return result

    def startBuildingInMinecraft(self):
        """Send the blueprint to Minecraft"""
        for id, building in self._blueprintData.items():
            pos = building.position
            level = building.level
            structure = building.building_info.structures[level-1]
            size = building.building_info.max_size
            area = Rect(pos, dropY(size))
            y = round(self.getHeightMap("mean", area))
            print("build at:", area, ",y:", y)
            buildFromNBT(self._editor, structure.nbtFile, addY(pos, y))
