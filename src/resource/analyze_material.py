"""
analyze area of surface and underground material
(x,y,z) reference point is the lower left corner.
Namely, if (x,y,z) is (0,0,0), the range of surface will be (x+rangeX, y+rangeY, z+rangeZ), the range of underground will be (x+rangeX, y-rangeY, z+rangeZ),
"""
from gdpc import WorldSlice
from gdpc.vector_tools import Box
from collections import Counter

def printSortedcontenDict(contenDict):
    contenDict = dict(
                sorted(contenDict.items(), key=lambda x: x[1], reverse=True))
    print(contenDict)

def analyzeOneBlockVerticalMaterial(worldSlice: WorldSlice, x, z):
    content = []
    noLeavesHeights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    leavesHeights = worldSlice.heightmaps["MOTION_BLOCKING"]
    surfaceHeight = int(noLeavesHeights[(x, z)])
    leavesHeight = int(leavesHeights[(x, z)])
    # in case there is a tree, it'll detect the tree top surface
    if (leavesHeight == surfaceHeight):  # surface is not tree
        for y in range(surfaceHeight - 10, surfaceHeight + 6):
            content.append(worldSlice.getBlock((x, y, z)).id)
    else:                              # surface is tree
        for y in range(surfaceHeight - 15, surfaceHeight + 1):
            content.append(worldSlice.getBlock((x, y, z)).id)
    return content


def analyzeSettlementMaterial(worldSlice: WorldSlice, settlementArea: Box):
    contenDictTmp = {}
    contenDict = Counter()
    x, _, z = settlementArea.size
    for i in range(0, x):
        for j in range(0, z):
            #  TODO: check if settlement or not _ SubaRya
            a, _, c = settlementArea.offset
            contenDictTmp = analyzeOneBlockVerticalMaterial(
                worldSlice, i+a, j+c)
            contenDict.update(Counter(contenDictTmp))
    printSortedcontenDict(contenDict)
    return contenDict
