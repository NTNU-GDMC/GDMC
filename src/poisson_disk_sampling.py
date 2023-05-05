from math import sqrt, floor, pi, sin, cos
from random import choice
from glm import ivec2
from gdpc.vector_tools import Rect, distance, neighbors2D
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt


def defaultSampleFunction(point: ivec2, r: int) -> ivec2:
    rad = 2 * pi * np.random.random()
    dis = np.random.random() * r + r
    offset = ivec2(floor(dis * cos(rad)), floor(dis * sin(rad)))
    return point + offset


def poissonDiskSample(bound: Rect, limit: int, r: float, k: int = 30, sampleFunc: Callable[[ivec2, int], ivec2] = defaultSampleFunction, initPoints: list[ivec2] = []) -> list[ivec2]:
    """
    get the sample positions of the bound, samepleFunc is to check if the chunk can add a point
    r is the minimum distance between two points
    return a list of ivec2
    """
    # random number generator
    rng = np.random.default_rng()

    # cell side length
    h, w = bound.size
    # cell side length
    a = r / sqrt(2)

    # cell number
    cols = floor(h / a) + 1
    rows = floor(w / a) + 1
    cellBound = Rect(ivec2(0, 0), ivec2(cols, rows))
    # cell array
    cells = np.full(cellBound.size, None, dtype=ivec2)

    # get the cell position of the point
    def getCellPos(point: ivec2) -> ivec2:
        return ivec2(floor(point[0] / a), floor(point[1] / a))

    # set the point to the cell
    def setCell(point: ivec2):
        pos = getCellPos(point)
        cells[pos[0]][pos[1]] = point

    # active set
    activeSet = set[ivec2]()
    # sample set
    samples = list[ivec2]()

    # init start point
    start = ivec2(rng.integers(0, h), rng.integers(
        0, w)) if not initPoints else choice(initPoints)
    setCell(start)
    activeSet.add(start)
    samples.append(start)

    while activeSet and len(samples) < limit:
        curPoint = activeSet.pop()

        for _ in range(k):
            samplePoint = sampleFunc(curPoint, r)
            # check if the point is in the bound
            if not bound.contains(samplePoint):
                continue

            # check if the point is in the cell
            samplePos = getCellPos(samplePoint)
            if cells[samplePos[0]][samplePos[1]]:
                continue

            # check if the point is in the range of other points
            for neighborPos in neighbors2D(samplePos, cellBound, True):
                neighbor = cells[neighborPos[0]][neighborPos[1]]
                if not neighbor:
                    continue
                if distance(neighbor, samplePoint) < r:
                    break
            # if the point is not in the range of other points
            else:
                # add the point to the cell
                setCell(samplePoint)
                activeSet.add(curPoint)
                activeSet.add(samplePoint)
                samples.append(samplePoint)
                break

    return samples


if __name__ == "__main__":
    h, w = 100, 100
    n = 1000
    d = 10

    bound = Rect(ivec2(0, 0), ivec2(h, w))
    samples = poissonDiskSample(bound, n, d)
    print(*samples, sep='\n')

    plt.scatter([p[0] for p in samples], [p[1] for p in samples])
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.xticks(range(0, 100, 7))
    plt.yticks(range(0, 100, 7))
    plt.grid()
    plt.show()
