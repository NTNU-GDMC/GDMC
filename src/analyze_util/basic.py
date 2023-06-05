import numpy as np
from gdpc.geometry import Rect
from typing import Callable, Any
from numpy import ndarray, average
from gdpc.vector_tools import distance2
from ..classes.core import Core
from ..building.building import Building
from ..building.building_info import BuildingInfo
from ..building.master_building_info import GLOBAL_BUILDING_INFO


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


def requiredBasement(core: Core, area: Rect) -> int:
    begin, end = area.begin, area.end
    heights = core.editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"][
        begin.x:end.x, begin.y:end.y]
    y = round(core.getHeightMap("mean", area))
    return np.sum(np.maximum(y - heights, 0))


def isLiquid(core: Core, area: Rect) -> float:
    begin, end = area.begin, area.end
    return average(core.liquidMap[begin.x:end.x, begin.y:end.y])


def hasEnoughWood(core: Core, area: Rect) -> float:
    """Choose if the wood in this area is above the threshold"""
    begin, end = area.begin, area.end
    return average(core.resourcesMap.wood[begin.x:end.x, begin.y:end.y])


def hasEnoughStone(core: Core, area: Rect) -> float:
    """Choose if the stone in this area is above the threshold"""
    begin, end = area.begin, area.end
    return average(core.resourcesMap.stone[begin.x:end.x, begin.y:end.y])


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
    return average(core.biomeMap.desert[begin.x:end.x, begin.y:end.y]) + \
        average(core.biomeMap.badlands[begin.x:end.x, begin.y:end.y])


def isVillage(core: Core, area: Rect) -> bool:
    """Check if the area is in the village"""
    begin, end = area.begin, area.end
    return np.sum(core.resourcesMap.artificial[begin.x:end.x, begin.y:end.y]) > 0


def nearBound(core: Core, area: Rect, minPadding: int) -> bool:
    """Check if the area is close enough to the bound"""
    bound = Rect(size=core.buildArea.toRect().size)

    left = area.begin.x - bound.begin.x
    bottom = area.begin.y - bound.begin.y
    right = bound.last.x - area.last.x
    top = bound.last.y - area.last.y

    return any((left < minPadding, right < minPadding, top < minPadding, bottom < minPadding))


def nearBuilding(core: Core, area: Rect, buildingInfo: BuildingInfo, minMargin: int) -> bool:
    """Check if the area is close enough to the bound"""
    variants = GLOBAL_BUILDING_INFO[buildingInfo.name]
    buildings = list[Building]()
    for variant in variants:
        buildings += core.getBuildings(buildingType=variant.type)

    return any([distance2(building.position, area.begin) < minMargin**2 for building in buildings])
