# analyze area of surface and underground material
# (x,y,z) reference point is the lower left corner. 
# Namely, if (x,y,z) is (0,0,0), the range of surface will be (x+rangeX, y+rangeY, z+rangeZ), the range of underground will be (x+rangeX, y-rangeY, z+rangeZ),

from gdpc import direct_interface as DI

def analyzeAreaMaterial(x, y, z):
    surfaceRange = {'x':16, 'y':16, 'z':16}
    undergroundRange = {'x':16, 'y':4, 'z':16}
    surfaceContent = []
    undergroundContent = []
    for rangeX in range(surfaceRange['x']):
        for rangeY in range(surfaceRange['y']):
            for rangeZ in range(surfaceRange['z']):
                surfaceContent.append(DI.getBlock(x+rangeX,y+rangeY,z+rangeZ))
    for rangeX in range(undergroundRange['x']):
        for rangeY in range(undergroundRange['y']):
            for rangeZ in range(undergroundRange['z']):
                undergroundContent.append(DI.getBlock(x+rangeX,y-rangeY,z+rangeZ))
    # print('surfaceContent: ', surfaceContent)
    # print('undergroundContent: ', undergroundContent)
    surfaceMaterialAnalyzeList = {}
    undergroundMaterialAnalyzeList = {}
    for idx in surfaceContent:
        if idx in surfaceMaterialAnalyzeList:
            surfaceMaterialAnalyzeList[idx] += 1
        else:
            surfaceMaterialAnalyzeList[idx] = 1
    surfaceSortedMaterialAnalyzeList = sorted(surfaceMaterialAnalyzeList.items(), key=lambda x: x[1], reverse=True)
    # print(surfaceSortedMaterialAnalyzeList)
    for idx in undergroundContent:
        if idx in undergroundMaterialAnalyzeList:
            undergroundMaterialAnalyzeList[idx] += 1
        else:
            undergroundMaterialAnalyzeList[idx] = 1
    undergroundSortedMaterialAnalyzeList = sorted(undergroundMaterialAnalyzeList.items(), key=lambda x: x[1], reverse=True)
    # print(undergroundSortedMaterialAnalyzeList)
    return surfaceSortedMaterialAnalyzeList, undergroundSortedMaterialAnalyzeList