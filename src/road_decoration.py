from math import sqrt, floor, pi, sin, cos, dist
from random import random, randint, choice
from operator import itemgetter
from glm import ivec3

flowers = [
    "dandelion",
    "poppy",
    "blue_orchid",
    "allium",
    "azure_bluet",
    "red_tulip",
    "orange_tulip",
    "white_tulip",
    "pink_tulip",
    "oxeye_daisy",
    "cornflower",
    "sunflower"
]

flowerStampSize = [[8, 3], [12, 5], [16, 2]]
treeStampSize = [14, 3]


def removeNear(l: list[ivec3], minDis: float):
    sotredLocs = sorted(l, key=itemgetter(0, 2))
    res: list[ivec3] = []
    for loc in sotredLocs:
        ok = True
        for j in range(len(res) - 1, -1, -1):
            if abs(loc[0] - res[j][0]) > minDis:
                break
            if dist(loc, res[j]) <= minDis:
                ok = False
                break
        if ok:
            res.append(loc)
    return res


def roadDecoration(roadCoord, interval, heights):
    flowerData = []
    size = len(roadCoord)
    for idx in range(0, size, interval):
        [x, y, z] = roadCoord[idx]
        [size, count] = choice(flowerStampSize)
        flower = choice(flowers)
        for _ in range(count):
            nx = randint(x - size, x + size)
            nz = randint(z - size, z + size)
            flowerData.append(
                [nx, heights[nx][nz], nz, flower])

    return flowerData


def treeDecoration(roadCoord, interval, heights):
    treeData = []
    size = len(roadCoord)
    for idx in range(0, size, interval):
        [x, y, z] = roadCoord[idx]
        [size, count] = treeStampSize
        for _ in range(count):
            nx = randint(x - size, x + size)
            nz = randint(z - size, z + size)
            print("does collide", [
                  x for x in roadCoord if (x[0] == nx and x[2] == nz)])
            if len([road for road in roadCoord if (road[0] == nx and road[2] == nz)]) == 0:
                treeData.append([nx, heights[nx][nz], nz])

    return removeNear(treeData, interval)


def lightDecoration(roadCoord: list[ivec3], interval: float, heights):
    lights: list[ivec3] = []
    for x, y, z in roadCoord:
        done = False
        for dx in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if done:
                    break
                if abs(dx) + abs(dz) != 1:
                    continue
                x1, z1 = x + dx, z + dz
                if (x1, y, z1) in roadCoord:
                    continue
                done = True
                lights.append((x1, y, z1))
    return removeNear(lights, interval)
