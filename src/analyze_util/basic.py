from ..classes.core import Core
from gdpc.geometry import Rect
from math import sqrt
from typing import Callable, Any
from numpy import ndarray
from ..resource.terrain_analyzer import analyzeAreaMaterialToResource


def checkEdge(map: ndarray, area: Rect, cmp: Callable[[Any], bool]) -> bool:
    x1, y1 = area.offset
    xlen, ylen = area.size
    x2 = x1 + xlen
    y2 = y1 + ylen

    for i in range(x1, x2):
        if cmp(map[i, y1]) or cmp(map[i, y2 - 1]):
            return True

    for i in range(y1, y2):
        if cmp(map[x1, i]) or cmp(map[x2 - 1, i]):
            return True

    return False


MAXIMUM_SD = 5


def isFlat(core: Core, area: Rect, maxSD=MAXIMUM_SD) -> float:
    """Only pick if the area's standard deviation is less than maxSD (more flat)"""
    return maxSD - sqrt(core.getHeightMap("var", area))


MINIMUM_WOOD = 50  # TODO: Ask Subarya how many is enough


def hasEnoughWood(core: Core, area: Rect, minWood=MINIMUM_WOOD) -> bool:
    """Choose if the wood in this area is above the threshold"""
    # TODO: change the resource to a new method to get the resources in the area only
    return analyzeAreaMaterialToResource(core.worldSlice, area).wood >= minWood


MAXIMUM_ROAD_DISTANCE = 30


def closeEnoughToRoad(core: Core, area: Rect, maxAverageDistance=MAXIMUM_ROAD_DISTANCE) -> bool:
    """Check if the edge of the area is close enough to a road"""
    def cmp(height: int):
        return height <= maxAverageDistance

    return checkEdge(core.roadMap, area, cmp)


def closeEnoughToLiquid(core: Core, area: Rect) -> bool:
    """Check if there's liquid in the range of area"""
    def cmp(isLiquid: int):
        return isLiquid == 1

    return checkEdge(core.liquidMap, area, cmp)
