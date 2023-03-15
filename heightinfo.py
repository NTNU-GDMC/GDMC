import numpy as np
import math


def acc2D(a: np.ndarray) -> np.ndarray:
    return np.cumsum(np.cumsum(a, axis=0, dtype=int), axis=1, dtype=int)


class Area(tuple[int, int, int, int]):
    def __new__(cls, x1: int, z1: int, x2: int, z2: int):
        return tuple.__new__(cls, (x1, z1, x2, z2))

    def contains(self, x: int, z: int):
        return x >= self[0] and z >= self[1] and \
            x <= self[2] and z <= self[3]

    def size(self) -> int:
        x1, z1, x2, z2 = self
        return (abs(x2-x1)+1)*(abs(z2-z1)+1)


class HeightInfo():
    def __init__(self, area: Area, heights: np.ndarray):
        x1, z1, x2, z2 = area
        x1, x2 = min(x1, x2), max(x1, x2)
        z1, z2 = min(z1, z2), max(z1, z2)
        self.area = Area(x1, z1, x2, z2)
        self.sizes = (x2-x1+1, z2-z1+1)
        self.heights = heights[:self.sizes[0], :self.sizes[1]].copy()
        self.squareHeights = np.square(self.heights)
        self.accHeights = acc2D(self.heights)
        self.accSquareHeights = acc2D(self.squareHeights)
        print(self.squareHeights)
        print(self.accHeights)
        print(self.accSquareHeights)

    def sumAreaFromAcc(self, a: np.ndarray, area: Area) -> int:
        x1, z1, x2, z2 = area

        def get(x, z) -> int:
            return a[x, z] if self.area.contains(x, z) else 0
        return get(x2, z2) - (get(x1-1, z2)+get(x2, z1-1)) + get(x1-1, z1-1)

    def sumArea(self, area: Area) -> int:
        return self.sumAreaFromAcc(self.accHeights, area)

    def squareSumArea(self, area: Area) -> int:
        return self.sumAreaFromAcc(self.accSquareHeights, area)

    def meanArea(self, area: Area) -> float:
        return self.sumArea(area) / self.area.size()

    def varArea(self, area: Area):
        return math.sqrt(self.squareSumArea(area) / self.area.size() -
                         self.meanArea(area) ** 2)
