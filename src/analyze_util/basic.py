from ..classes.core import Core
from gdpc.geometry import Rect
from math import sqrt, floor
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


def isFlat(core: Core, area: Rect) -> float:
    """Only pick if the area's standard deviation is less than maxSD (more flat)"""
    std = core.getHeightMap("std", area)
    if std == 0:
        return float('inf')
    return 1 / std


def isLiquid(core: Core, area: Rect) -> float:
    begin, end = area.begin, area.end
    sum = core.liquidMap[begin.x:end.x, begin.y:end.y].sum()
    return sum / area.area


def hasEnoughWood(core: Core, area: Rect) -> float:
    """Choose if the wood in this area is above the threshold"""
    # TODO: change the resource to a new method to get the resources in the area only
    begin, end = area.begin, area.end
    sum = core.resourcesMap.wood[begin.x:end.x, begin.y:end.y].sum()
    return sum/area.area


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


def isDesert(core: Core, area: Rect) -> float:
    """Check if the area is in the desert"""
    begin, end = area.begin, area.end
    sum = core.biomeMap.desert[begin.x:end.x, begin.y:end.y].sum() + \
        core.biomeMap.badlands[begin.x:end.x, begin.y:end.y].sum()
    return sum / area.area


MINIMUM_BOUND_PADDING = 10


def nearBound(core: Core, area: Rect, minPadding=MINIMUM_BOUND_PADDING) -> bool:
    """Check if the area is close enough to the bound"""
    bound = core.buildArea.toRect()

    left = area.begin.x - bound.begin.x
    bottom = area.begin.y - bound.begin.y
    right = bound.last.x - area.last.x
    top = bound.last.y - area.last.y

    return any([left < minPadding, right < minPadding, top < minPadding, bottom < minPadding])
