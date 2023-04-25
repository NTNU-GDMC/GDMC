# analyze area of surface and underground material
# (x,y,z) reference point is the lower left corner.
# Namely, if (x,y,z) is (0,0,0), the range of surface will be (x+rangeX, y+rangeY, z+rangeZ), the range of underground will be (x+rangeX, y-rangeY, z+rangeZ),
import time
from gdpc import interface as DI
from gdpc import Editor, WorldSlice
import glm
from globalUtils import editor
from gdpc.vector_tools import Box

def getBiome(surface, under):
    tmpList = {}
    grassAmount = int(0)
    sandstoneAmount = int(0)
    redSandAmount = int(0)
    snowAmount = int(0)
    for idx in range(len(surface)):
        block, amount = surface[idx]
        if (block == 'minecraft:grass_block'):
            grassAmount = amount
        elif (block == 'minecraft:sandstone'):
            sandstoneAmount = amount
        elif (block == 'minecraft:red_sand'):
            redSandAmount = amount
        elif (block == 'minecraft:snow'):
            snowAmount = amount
    for idx in range(len(under)):
        block, amount = under[idx]
        if (block == 'minecraft:grass_block'):
            tmpList['minecraft:grass_block'] = amount + grassAmount
        elif (block == 'minecraft:sandstone'):
            tmpList['minecraft:sandstone'] = amount + sandstoneAmount
        elif (block == 'minecraft:red_sand'):
            tmpList['minecraft:red_sand'] = amount + redSandAmount
        elif (block == 'minecraft:snow'):
            tmpList['minecraft:snow'] = amount + snowAmount
    tmpList = sorted(tmpList.items(), key=lambda x: x[1], reverse=True)
    if not tmpList:
        return str("origin")
    block, amount = tmpList[0]
    if (block == 'minecraft:grass_block'):
        return str("origin")
    elif (block == 'minecraft:sandstone'):
        return str("desert")
    elif (block == 'minecraft:red_sand'):
        return str("badland")
    elif (block == 'minecraft:snow'):
        return str("snow")


def analyzeAreaMaterial(x, y, z):
    editor = Editor(buffering=True)
    surfaceRange = {'x': 16, 'y': 12, 'z': 16}
    undergroundRange = {'x': 16, 'y': 4, 'z': 16}
    surfaceContent = []
    undergroundContent = []
    for rangeX in range(surfaceRange['x']):
        for rangeY in range(surfaceRange['y']):
            for rangeZ in range(surfaceRange['z']):
                surfaceContent.append(
                    str(editor.worldSlice.getBlock(glm.ivec3(x+rangeX, y+rangeY, z+rangeZ))))
    for rangeX in range(undergroundRange['x']):
        for rangeY in range(undergroundRange['y']):
            for rangeZ in range(undergroundRange['z']):
                undergroundContent.append(
                    str(editor.worldSlice.getBlock(glm.ivec3(x+rangeX, y-rangeY, z+rangeZ))))
    # print('surfaceContent: ', surfaceContent)
    # print('undergroundContent: ', undergroundContent)\
    surfaceMaterialAnalyzeList = {}
    undergroundMaterialAnalyzeList = {}
    for idx in surfaceContent:
        if idx in surfaceMaterialAnalyzeList:
            surfaceMaterialAnalyzeList[idx] += 1
        else:
            surfaceMaterialAnalyzeList[idx] = 1
    surfaceSortedMaterialAnalyzeList = sorted(
        surfaceMaterialAnalyzeList.items(), key=lambda x: x[1], reverse=True)
    print(surfaceSortedMaterialAnalyzeList)
    for idx in undergroundContent:
        if idx in undergroundMaterialAnalyzeList:
            undergroundMaterialAnalyzeList[idx] += 1
        else:
            undergroundMaterialAnalyzeList[idx] = 1
    undergroundSortedMaterialAnalyzeList = sorted(
        undergroundMaterialAnalyzeList.items(), key=lambda x: x[1], reverse=True)
    # print(surfaceSortedMaterialAnalyzeList)
    print(undergroundSortedMaterialAnalyzeList)
    return getBiome(surfaceSortedMaterialAnalyzeList, undergroundSortedMaterialAnalyzeList)


def analyzeOneBlockVerticalMaterial(WORLDSLICE: WorldSlice, x, z):
    content = []
    noLeavesHeights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    leavesHeights = WORLDSLICE.heightmaps["MOTION_BLOCKING"]
    surfaceHeight = int(noLeavesHeights[(x, z)])
    leavesHeight = int(leavesHeights[(x, z)])
    # print(surfaceHeight)
    # print(leavesHeight)
    # in case there is a tree, it'll detect the tree top surface
    if (leavesHeight == surfaceHeight):  # surface is not tree
        for y in range(surfaceHeight-10, surfaceHeight+6):
            content.append(editor.worldSlice.getBlock((x, y, z)).id)
    else:                              # surface is tree
        for y in range(surfaceHeight-15, surfaceHeight+1):
            content.append(editor.worldSlice.getBlock((x, y, z)).id)
    contentList = {}
    for idx in content:
        if idx in contentList:
            contentList[idx] += 1
        else:
            contentList[idx] = 1
    contentList = dict(
        sorted(contentList.items(), key=lambda x: x[1], reverse=True))
    # print("analyzeOneBlockVerticalMaterial x= ", x, "z = ", z)
    # print(content)
    # print(contentList)
    return content, contentList


def analyzeSettlementMaterial(WORLDSLICE: WorldSlice, settlementArea: Box):
    contentTmp = []
    contentListTmp = {}
    content = []
    contentList = {}
   
    x, _, z = settlementArea.size
    # x, y = len(settlementArea), len(settlementArea[0])
    # 01 Map to coord of (x, z)
    for i in range(0, x):
        for j in range(0, z):
            # print("x = ", i, "y = ", j)
            
            #  TODO: check if settlement or not _ SubaRya
            
            #  if (settlementArea[i][j] == 1):
            a, _, c = settlementArea.offset
            contentTmp, contentListTmp = analyzeOneBlockVerticalMaterial(WORLDSLICE, i+a, j+c)
            content.extend(contentTmp)
            # combine contentList, if there is the same key, add it, sort it then!
            for key, value in contentListTmp.items():
                # print("key: ", key, "value: ", value)
                # print(contentList.get(key))
                if (contentList.get(key) != None):
                    contentList[key] += contentListTmp[key]
                else:
                    contentList.update({key: value})
            contentList = dict(
                sorted(contentList.items(), key=lambda x: x[1], reverse=True))
                # print("analyzeSettlementMaterial")
                # print(contentTmp)
                # print(contentListTmp)
                # print("final: ")
                # print(content)
                # print(contentList)
            content = list(set(content))
    return content, contentList
