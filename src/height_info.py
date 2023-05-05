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

    def __sumFromAcc__(self, acc: np.ndarray, area: Rect) -> int:
        # get sum of area from accumulated 2D array
        def get(pos: Vec2iLike) -> int:
            x, z = pos
            return acc[x, z] if self.area.contains(pos) else 0
        x1, z1 = area.begin
        x2, z2 = area.last
        return get((x2, z2)) - (get((x1 - 1, z2)) + get((x2, z1 - 1))) + get((x1 - 1, z1 - 1))

    def sum(self, area: Rect) -> int:
        return self.__sumFromAcc__(self.accHeights, area)

    def squareSum(self, area: Rect) -> int:
        return self.__sumFromAcc__(self.accSquareHeights, area)

    def mean(self, area: Rect) -> float:
        return self.sum(area) / self.area.area

    def var(self, area: Rect) -> float:
        return self.squareSum(area) / self.area.area - self.mean(area) ** 2

    def std(self, area: Rect) -> float:
        return math.sqrt(self.var(area))


if __name__ == "__main__":
    # test
    heights = np.array([[1, 2, 3, 4, 5],
                        [2, 3, 4, 5, 6],
                        [3, 4, 5, 6, 7],
                        [4, 5, 6, 7, 8],
                        [5, 6, 7, 8, 9]])
    area = Rect((1, 1), (3, 3))
    heightInfo = HeightInfo(heights)
    print(heightInfo.sum(area))
    print(heightInfo.squareSum(area))
    print(heightInfo.mean(area))
    print(heightInfo.var(area))
    print(heightInfo.std(area))
