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

flowerStampSize = [[3, 3], [5, 8], [8, 20]]


# return value is [x,z,flowerName]
def roadDecoration(roadCoord, interval) -> []:
    flowerData = []
    size = len(roadCoord)
    for idx in range(0, size, interval):
        [x, y] = roadCoord[idx]
        [size, count] = choice(flowerStampSize)
        for _ in range(count):
            flowerData.append(
                [randint(x, x+size), randint(y, y+size), choice(flowers)])

    return flowerData
