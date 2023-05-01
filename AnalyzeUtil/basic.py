from ..classes.core import Core
from gdpc.geometry import Rect
from math import sqrt


MAXIMUM_SD = 5
def isFlat(core: Core, area: Rect, maxSD=MAXIMUM_SD) -> bool:
    """Only pick if the area's standard deviation is less than maxSD (more flat)"""
    return sqrt(core.getHeightMap("var", area)) <= maxSD

MINIMUM_WOOD = 50 # TODO: Ask Subarya how many is enough
def hasEnoughWood(core: Core, area: Rect, minWood=MINIMUM_WOOD):
    """Choose if the wood in this area is above the threshold"""
    # TODO: change the resource to a new method to get the resources in the area only
    return core.resources.wood >= minWood 
