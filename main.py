# ! /usr/bin/python3
# import time
# import getBuildingEntryInfo as BEI
# import pprint
# import nbt_builder
# from nbt import nbt
# import os
# import pathfind
# from gdpc import geometry as GEO
# from gdpc import interface as INTF
# from gdpc import minecraft_tools as TB
# from gdpc import world_slice as WL
# from gdpc.vector_tools import *
# from gdpc import Editor, Block
# from math import floor
# from heightAnalysis import getSmoothChunk
# from heightAnalysis import getAvailableBuildArea
# from resource.AnalyzeAreaBiomeList import getAllBiomeList
# from resource.AnalyzeAreaMaterial import analyzeOneBlockVerticalMaterial
# from resource.AnalyzeAreaMaterial import analyzeSettlementMaterial
# from resource.ChangeMaterialToResource import changeMaterialToResource
# import random
# from poissionDiskSampling import poissionSample as pS
# from roadDecoration import roadDecoration, treeDecoration, lightDecoration
# from glm import ivec3
# from globalUtils import editor
# from resource.AnalyzeAreaMaterial import analyzeAreaMaterial

# # * Change the build area here
# # ! Notice that set Box((0, 0, 0), (255, 255, 255)) will return Box((0, 0, 0), (256, 256, 256))
# buildArea = editor.setBuildArea(Box((0, 0, 0), (255, 255, 255)))
# worldSlice = editor.loadWorldSlice(buildArea.toRect(), cache=True)
# print("Build Area:", buildArea)

# START = buildArea.begin
# END = buildArea.last

# buildings: list[ivec3] = []
# roads: list[ivec3] = []

# STRUCTURE_DIR = os.path.abspath("./data/structures")
# BUILDING_TYPE = ["chalet", "chalet_2", "modern_house"]


# def getBuildingDir(name: str):
#     return os.path.join(STRUCTURE_DIR, name)

# FIXME: remove this function, cuz it was moved to building.py - SubaRya
# def getBuildingNBTDir(name: str):

#     return os.path.join(getBuildingDir(name), f"{name}.nbt")

# FIXME: remove this function, cuz it was moved to building.py - SubaRya
# def getBuildingInfoDir(name: str):
#     return os.path.join(getBuildingDir(name), f"{name}.json")


# def buildBasicBuilding():
#     global buildings
#     heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

#     buildArea = getSmoothChunk(heights)
#     coBuildingList = pS(START.x, START.z, END.x, END.z, 10, 23, buildArea)

#     print("coBuildingList:")
#     pprint.pprint(coBuildingList)

#     x, z = coBuildingList[0]

#     # analyze Biome
#     # return "origin", "desert", "badland", or "snow"
#     # x, z = int(x), int(z)
#     # y = int(heights[(x, z)])
#     # analyzeReferCoord = (x, y, z)
#     # biome = getAllBiomeList(WORLDSLICE, getAvailableBuildArea(WORLDSLICE))

#     # print("Biome of this certain region is : ", biome)

#     editor.runCommand(f"tp @a {x} 100 {z}")

#     for pos in coBuildingList:
#         x, z = pos
#         x, z = floor(x), floor(z)

#         y = int(heights[(x, z)])
#         x = int(x+START.x)
#         z = int(z+START.z)
#         print(x, y, z)

#         buildingType = random.choice(BUILDING_TYPE)
#         nbt_struct = nbt.NBTFile(getBuildingNBTDir(buildingType))

#         sizeX, sizeY, sizeZ = map(lambda e: int(e.value), nbt_struct["size"])
#         print("size x, y, z:", sizeX, sizeY, sizeZ)

#         buildingInfo = BEI.BuildingInfo(getBuildingInfoDir(buildingType))

#         entryNames = buildingInfo.getBuildingNameList()
#         entry = buildingInfo.getEntryInfo(entryNames[0])

#         tmpBuildings = buildings.copy()

#         print("entry pos:", entry.pos)
#         dx, dy, dz = entry.pos
#         entryPos = ivec3(x+dx, y+dy, z+dz)
#         print("entry pos(T):", entryPos)
#         for dx in range(sizeX):
#             for dy in range(sizeY):
#                 for dz in range(sizeZ):
#                     x1, y1, z1 = x+dx, y+dy, z+dz
#                     buildingBlk = ivec3(x1, y1, z1)
#                     if buildingBlk == entryPos:
#                         continue
#                     tmpBuildings.append(buildingBlk)

#         ok = pathfind.buildRoad(entryPos, roads, tmpBuildings)

#         if ok:
#             size = nbt_builder.getStructureSizeNBT(nbt_struct)
#             for ix in range(x, x + size[0]):
#                 for iz in range(z, z + size[2]):
#                     for iy in range(worldSlice.heightmaps["MOTION_BLOCKING"][(ix, iz)], y):
#                         editor.placeBlock(
#                             ivec3(ix, iy, iz), Block("minecraft:dirt"))
#             # fix: buildFromStructureNBT parameter biome list - SubaRya
#             nbt_builder.buildFromStructureNBT(nbt_struct, x, y, z, "fix_here")
#             buildings = tmpBuildings
#             print(f"{'-'*25}build one finish{'-'*25}")
#         else:
#             print(f"{'-'*25}build one failed{'-'*25}")


# def buildRoadDecoration():
#     heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
#     data = roadDecoration(roads, 8, heights)
#     for flower in data:
#         [x, y, z, name] = flower
#         editor.placeBlock(ivec3(x, y, z), Block(name))
#     return


# def buildTreeDecoration():
#     heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
#     data = treeDecoration(roads, 12, heights)
#     nbt_struct = nbt.NBTFile(getBuildingNBTDir("decorations/tree"))

#     for tree in data:
#         [x, y, z] = tree
#         nbt_builder.buildFromStructureNBT(nbt_struct, x, y, z, True)
#     for road in roads:
#         [x, y, z] = road
#         editor.placeBlock(ivec3(x, y+1, z), Block("air"))
#         editor.placeBlock(ivec3(x, y+1, z), Block("air"))
#     return


# def placeStreetLight(x: int, y: int, z: int):
#     editor.placeBlock(ivec3(x, y, z), Block("cobblestone"))
#     editor.placeBlock(ivec3(x, y+1, z), Block("cobblestone_wall"))
#     editor.placeBlock(ivec3(x, y+2, z), Block("torch"))


# def buildLightDecoration():
#     locs = lightDecoration(roads, 16, None)
#     for loc in locs:
#         placeStreetLight(*loc)


# def analyzeSettlement():
#     heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
#     settlement = getAvailableBuildArea(heights)
#     # print(settlement)
#     settlementMaterialContent, settlementMaterialList = analyzeSettlementMaterial(
#         worldSlice, settlement)
#     print("Settlement Content", settlementMaterialContent, "\n")
#     print("Settlement Material List", settlementMaterialList)
#     changeMaterialToResource(settlementMaterialList)
#     biomeList = getAllBiomeList(worldSlice, settlement)
#     print("Settlement Biome List = ", biomeList)


# if __name__ == '__main__':
#     # Change this to True if you want to teleport to the start location
#     tpToStart = False
#     try:
#         if tpToStart:
#             y = worldSlice.heightmaps["MOTION_BLOCKING"][(START.x, START.z)]
#             cmd = f"tp @a {START.x} {y} {START.z}"
#             editor.runCommand(cmd)
#             print(cmd)

#         start = time.time()

#         analyzeSettlement()
#         buildBasicBuilding()
#         buildRoadDecoration()
#         buildTreeDecoration()
#         buildLightDecoration()

#         print("Done!")
#         end = time.time()
#         print("The time of execution of above program is :",
#               (end-start) * 10**3, "ms")
#     except KeyboardInterrupt:   # useful for aborting a run-away program
#         print("Pressed Ctrl-C to kill program.")

from classes.core import Core
from classes.agent import BuildAgent
import random
#  TODO: logic per round
if __name__ == '__main__':
    core = Core()
    agents = [
        BuildAgent(core, lambda core, rect: 0, ""),
    ]

    # loop 10 rounds
    round = 10

    for i in range(round):
        # randomize agent order
        for agent in random.sample(agents, len(agents)):
            # run agent
            agent.run()
