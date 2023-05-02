from ..classes.core import Core
from gdpc.geometry import Rect
from math import sqrt


MAXIMUM_SD = 5
def isFlat(core: Core, area: Rect, maxSD=MAXIMUM_SD) -> bool:
    """Only pick if the area's standard deviation is less than maxSD (more flat)"""
    return sqrt(core.getHeightMap("var", area)) <= maxSD

MINIMUM_WOOD = 50 # TODO: Ask Subarya how many is enough
def hasEnoughWood(core: Core, area: Rect, minWood=MINIMUM_WOOD) -> bool:
    """Choose if the wood in this area is above the threshold"""
    # TODO: change the resource to a new method to get the resources in the area only
    return core.resources.wood >= minWood 

MAXIMUM_ROAD_DISTANCE = 30
def closeEnoughToRoad(core: Core, area:Rect, maxAverageDistance=MAXIMUM_ROAD_DISTANCE) -> bool:
    """Check if the edge of the area is close enough to a road"""
    x1, y1 = area.offset
    xlen, ylen = area.size
    x2 = x1 + xlen
    y2 = y1 + ylen

    for i in range(x1, x2):
        if max(core.roadMap[i, y1], core.roadMap[i, y2 - 1]) <= maxAverageDistance:
            return True

    for i in range(y1, y2):
        if max(core.roadMap[x1, i], core.roadMap[x2 - 1, i]) <= maxAverageDistance:
            return True

    return False
