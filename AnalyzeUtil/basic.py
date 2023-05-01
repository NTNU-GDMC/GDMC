from ..classes.core import Core
from gdpc.geometry import Rect
from math import sqrt


MAXIMUM_SD= 5

def isFlat(core: Core, area: Rect, maxSD=MAXIMUM_SD) -> bool:
    """Only pick if the area's standard deviation is less than maxSD (more flat)"""
    return sqrt(core.getHeightMap("var", area)) <= maxSD

