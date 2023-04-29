import numpy as np
import math
from gdpc.vector_tools import Rect, Vec2iLike


class HeightInfo():
    def __init__(self, heights: np.ndarray):
        # accumulate 2D array
        def acc2D(a) -> np.ndarray: return np.cumsum(
            np.cumsum(a, axis=0, dtype=int), axis=1, dtype=int)

        self.area = Rect((0, 0), heights.shape)
        self.heights = heights.copy()
        self.squareHeights = np.square(self.heights)
        self.accHeights = acc2D(self.heights)
        self.accSquareHeights = acc2D(self.squareHeights)

    def sumAreaFromAcc(self, acc: np.ndarray, area: Rect) -> int:
        # get sum of area from accumulated 2D array
        def get(pos: Vec2iLike) -> int:
            x, z = pos
            return acc[x, z] if self.area.contains(pos) else 0
        x1, z1 = area.begin
        x2, z2 = area.last
        return get((x2, z2)) - (get((x1-1, z2))+get((x2, z1-1))) + get((x1-1, z1-1))

    def sumArea(self, area: Rect) -> int:
        return self.sumAreaFromAcc(self.accHeights, area)

    def squareSumArea(self, area: Rect) -> int:
        return self.sumAreaFromAcc(self.accSquareHeights, area)

    def meanArea(self, area: Rect) -> float:
        return self.sumArea(area) / self.area.area

    def varArea(self, area: Rect) -> float:
        return self.squareSumArea(area) / self.area.area - self.meanArea(area) ** 2

    def stdArea(self, area: Rect) -> float:
        return math.sqrt(self.varArea(area))
