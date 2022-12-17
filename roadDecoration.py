from math import sqrt, floor, pi, sin, cos, dist
from random import random, randint, choice

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
treeStampSize = [8, 3]

# return value is [x,z,flowerName]


def roadDecoration(roadCoord, interval, heights) -> []:
    flowerData = []
    size = len(roadCoord)
    for idx in range(0, size, interval):
        [x, y, z] = roadCoord[idx]
        [size, count] = choice(flowerStampSize)
        flower = choice(flowers)
        for _ in range(count):
            nx = randint(x - size, x+size)
            nz = randint(z - size, z+size)
            flowerData.append(
                [nx, heights[nx][nz], nz, flower])

    return flowerData


def treeDecoration(roadCoord, interval, heights) -> []:
    treeData = []
    size = len(roadCoord)
    for idx in range(0, size, interval):
        [x, y, z] = roadCoord[idx]
        [size, count] = treeStampSize
        for _ in range(count):
            nx = randint(x - size, x+size)
            nz = randint(z - size, z+size)
            if len([x for x in roadCoord if (x[0] == nx and x[2] == nz)]) > 0:
                continue

            treeData.append([nx, heights[nx][nz], nz])

    return treeData
