import numpy as np
from gdpc.vector_tools import Rect, Vec2iLike


class HeightInfo():
    def __init__(self, heights: np.ndarray):
        def acc2D(a) -> np.ndarray:
            """accumulate 2D array"""
            return np.cumsum(
                np.cumsum(a, axis=0, dtype=np.int64), axis=1, dtype=np.int64)

        self.area = Rect(size=heights.shape)
        self.heights = np.copy(np.int64(heights))
        self.squareHeights = np.square(self.heights, dtype=np.int64)
        self.accHeights = acc2D(self.heights)
        self.accSquareHeights = acc2D(self.squareHeights)

    def __sumFromAcc__(self, acc: np.ndarray, area: Rect) -> int:
        maxX, maxZ = self.area.last

        def get(pos: Vec2iLike) -> int:
            """get sum of area from accumulated 2D array"""
            x, z = pos
            if x < 0 or z < 0:
                return 0

            return acc[min(x, maxX), min(z, maxZ)]
        x1, z1 = area.begin
        x2, z2 = area.last
        return get((x2, z2)) - (get((x1 - 1, z2)) + get((x2, z1 - 1))) + get((x1 - 1, z1 - 1))

    def sum(self, area: Rect) -> int:
        return self.__sumFromAcc__(self.accHeights, area)

    def squareSum(self, area: Rect) -> int:
        return self.__sumFromAcc__(self.accSquareHeights, area)

    def mean(self, area: Rect) -> float:
        return self.sum(area) / area.area

    def var(self, area: Rect) -> float:
        return self.squareSum(area) / area.area - self.mean(area) ** 2

    def std(self, area: Rect) -> float:
        return np.sqrt(self.var(area))


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
