from gdpc import Editor
from gdpc.vector_tools import Rect, Box
from typing import Literal
import numpy as np
from BuildingUtil.building import Building

from heightinfo import HeightInfo
from resource.AnalyzeAreaBiomeList import getAllBiomeList
from resource.ChangeMaterialToResource import changeMaterialToResource
from resource.AnalyzeAreaMaterial import analyzeSettlementMaterial

DEFAULT_BUILD_AREA = Box((0, 0, 0), (255, 255, 255))


class Core():
    def __init__(self, buildArea=DEFAULT_BUILD_AREA) -> None:
        """
        the core will connect with the game
        """
        # initalize editor
        editor = Editor(buffering=True, caching=True)
        editor.setBuildArea(buildArea)
        # get world slice and height maps
        worldSlice = editor.loadWorldSlice(buildArea.toRect(), cache=True)
        heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

        # get top left and bottom right coordnidate
        x1, _, x2 = buildArea.offset
        z1, _, z2 = buildArea.offset + buildArea.size
        x, _, z = buildArea.size

        self._roadMap = np.ndarray((x, z))
        self._liquidMap = np.where(
            worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] > worldSlice.heightmaps["OCEAN_FLOOR"], 1, 0)
        self._biomeList = getAllBiomeList(worldSlice, buildArea)
        self._editor = editor
        self._resources = changeMaterialToResource(worldSlice, buildArea)
        # contains: height, sd, var, mean
        self._heightInfo = HeightInfo((x1, z1, x2, z2), heights)
        self._blueprint = np.zeros((x // 2, z // 2), dtype=int)  # unit is 2x2
        self._blueprintData: dict[int, Building] = {}

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
    def blueprint(self):
        return self._blueprint

    def getBlueprintBuildingData(self, id: int):
        return self._blueprintData[id]

    def addBuilding(self, building: Building):
        """Append a building on to the blueprint. We trust our agent, if there's any overlap, it's agent's fault."""
        (x, z) = building.position
        (xlen, zlen) = building.offset
        id = len(self._blueprintData) + 1

        self._blueprintData[id] = building
        self._blueprint[x:x+xlen, z:z+zlen] = id

    def getHeightMap(self, heightType: Literal["var", "mean", "sum", "squareSum"], bound: Rect):
        x1, x2 = bound.offset
        z1, z2 = bound.offset + bound.size
        area = (x1, z1, x2, z2)
        if heightType == "var":
            return self._heightInfo.varArea(area)
        if heightType == "mean":
            return self._heightInfo.meanArea(area)
        if heightType == "sum":
            return self._heightInfo.sumArea(area)
        if heightType == "squareSum":
            return self._heightInfo.squareSumArea(area)
        raise Exception("This type does not exist on heightType")

    def getEmptyArea(self, height: int, width: int) -> list[Rect]:
        def isEmpty(val: any):
            if val == 0:
                return 0
            return 1
        prefix = np.zeros_like(self.blueprint)
        h, w = prefix.shape[:2]

        prefix[0][0] = isEmpty(self.blueprint[0][0])

        for i in range(1, h):
            prefix[i][0] = prefix[i-1][0] + isEmpty(self.blueprint[i][0])

        for i in range(1, w):
            prefix[0][i] = prefix[0][i-1] + isEmpty(self.blueprint[0][i])

        # probably can figure out a way to cache this
        for i in range(1, h):
            for j in range(1, w):
                prefix[i][j] = prefix[i-1][j] + prefix[i][j-1] - \
                    prefix[i-1][j-1] + isEmpty(self.blueprint[i][j])
        result: list[Rect] = []

        for i in range(h - height):
            for j in range(w - width):
                lh = i + height
                lw = j + width
                left = 0
                top = 0
                leftTop = 0
                if i > 0:
                    top = prefix[i-1][lw]
                if j > 0:
                    left = prefix[lh][j - 1]
                if i > 0 and j > 0:
                    leftTop = prefix[i-1][j-1]

                used = prefix[lh][lw] - top - left + leftTop
                if used == 0:
                    result.append(Rect((i, j), (lh, lw)))

        return result

    def startBuildingInMinecraft(self):
        """Send the blueprint to Minecraft"""
        pass
