from math import sqrt, floor, pi, sin, cos
from random import choice
from glm import ivec2
from gdpc.vector_tools import Rect, distance, neighbors2D
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt


# def poissionSample(sx, sy, ex, ey, num, minRange, acceptPos) -> list:
#     k = 30  # sample number
#     if sx > ex:
#         sx, ex = ex, sx
#     if sy > ey:
#         sy, ey = ey, sy
#     acceptPositionSet = set(acceptPos)
#     # maxRange = 2 * minRange
#     w = minRange / sqrt(2)
#     xlen = ex - sx
#     ylen = ey - sy
#     cols = floor(xlen / w) + 1
#     rows = floor(ylen / w) + 1
#     cells = [[-1 for i in range(cols)] for i in range(rows)]
#     activeList = []
#     randChunk = acceptPos[randint(0, len(acceptPos) - 1)]
#     pos = [randChunk[0] + randint(0, 16) - sx,
#            randChunk[1] + randint(0, 16) - sy]
#     x = floor((pos[0]-sx) / w)
#     y = floor((pos[1]-sy) / w)
#     cells[x][y] = pos
#     activeList.append(pos)
#     count = 0
#     print("init = ", pos)
#     while len(activeList) > 0 and count < num:
#         idx = floor(len(activeList) * random())
#         curPos = activeList[idx]
#         found = False
#         for i in range(k):
#             rad = 2*pi*random()
#             offsetX = cos(rad)
#             offsetY = sin(rad)
#             mag = random() * minRange + minRange
#             samplePoint = [curPos[0] + offsetX*mag, curPos[1] + offsetY*mag]
#             sampleChunk = (
#                 floor(samplePoint[0] / 16) * 16, floor(samplePoint[1] / 16) * 16)

#             sampleX = floor((samplePoint[0]) / w)
#             sampleY = floor((samplePoint[1]) / w)

#             if sampleX < 0 or sampleY < 0 or sampleX >= cols or sampleY >= rows or cells[sampleX][sampleY] != -1:
#                 continue

#             if sampleChunk not in acceptPositionSet:

#                 continue
#             flag = True
#             for i in range(sampleX-1, sampleX+2):
#                 for j in range(sampleY-1, sampleY+2):
#                     if i == sampleX and j == sampleY:
#                         continue
#                     if i < 0 or j < 0 or i >= cols or j >= rows:
#                         continue
#                     if cells[i][j] == -1:
#                         continue
#                     curDist = dist(cells[i][j], samplePoint)
#                     if curDist < minRange:
#                         flag = False
#             if flag:
#                 cells[sampleX][sampleY] = samplePoint
#                 activeList.append(samplePoint)
#                 found = True
#                 count += 1
#                 # mycanvas.create_oval(samplePoint[0],samplePoint[1],samplePoint[0]+3,samplePoint[1]+3, fill='red')
#                 break

#         if not found:
#             del activeList[idx]
#     coords = []

#     for row in cells:
#         for p in row:
#             if p != -1:
#                 coords.append([p[0] + sx, p[1] + sy])

#     return coords


def defaultSampleFunction(point: ivec2, r: int) -> ivec2:
    rad = 2*pi*np.random.random()
    dis = np.random.random()*r+r
    offset = ivec2(floor(dis*cos(rad)), floor(dis*sin(rad)))
    return point+offset


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
