#! /usr/bin/python3
import getBuildingEntryInfo as BEI
import pprint
import nbt_builder
from nbt import nbt
import os
from pathfind import Location
import pathfind
from gdpc import geometry as GEO
from gdpc import interface as INTF
from gdpc import toolbox as TB
from gdpc import worldLoader as WL
from math import floor
from NTNUBasicBuilding import InitialChalet
from heightAnalysis import getSmoothChunk
import random
from poissionDiskSampling import poissionSample as pS
from roadDecoration import roadDecoration, treeDecoration, lightDecoration
from AnalyzeAreaMaterial import analyzeAreaMaterial
from interface import Interface

intf = Interface()

STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = buildArea = (0, 1, 0, 255, 255, 255)

intf.runCommand(
    f"/setbuildarea {STARTX} {STARTY} {STARTZ} {ENDX} {ENDY} {ENDZ}", 0)
print("Build Area: ", *INTF.requestBuildArea())

# IMPORTANT: Keep in mind that a wold slice is a 'snapshot' of the world,
#   and any changes you make later on will not be reflected in the world slice
WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)

buildings: list[Location] = []
roads: list[Location] = []

STRUCTURE_DIR = os.path.abspath("./data/structures")
BUILDING_TYPE = ["chalet", "chalet_2", "modern_house"]
# BUILDING_TYPE = ["nbt_example"]

analyzeReferCoord = ()


def getBuildingDir(name: str):
    return os.path.join(STRUCTURE_DIR, name)


def getBuildingNBTDir(name: str):

    return os.path.join(getBuildingDir(name), f"{name}.nbt")


def getBuildingInfoDir(name: str):
    return os.path.join(getBuildingDir(name), f"{name}.json")


def buildBasicBuilding():
    global buildings
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    buildArea = getSmoothChunk(heights)
    coBuildingList = pS(STARTX, STARTZ, ENDX, ENDZ, 10, 23, buildArea)

    print("coBuildingList:")
    pprint.pprint(coBuildingList)

    x, z = coBuildingList[0]

    # analyze Biome
    # return "origin", "desert", "badland", or "snow"
    x, z = int(x), int(z)
    y = int(heights[(x, z)])
    analyzeReferCoord = (x, y, z)
    biome = str(analyzeAreaMaterial(*analyzeReferCoord))

    print("Biome of this certain region is : ", biome)

    INTF.runCommand(f"tp @a {x} 100 {z}")

    for pos in coBuildingList:
        x, z = pos
        x, z = floor(x), floor(z)

        y = int(heights[(x, z)])
        x = int(x+STARTX)
        z = int(z+STARTZ)
        print(x, y, z)

        buildingType = random.choice(BUILDING_TYPE)
        nbt_struct = nbt.NBTFile(getBuildingNBTDir(buildingType))

        sizeX, sizeY, sizeZ = map(lambda e: int(e.value), nbt_struct["size"])
        print("size x, y, z:", sizeX, sizeY, sizeZ)

        buildingInfo = BEI.BuildingInfo(getBuildingInfoDir(buildingType))

        entryNames = buildingInfo.getBuildingNameList()
        entry = buildingInfo.getEntryInfo(entryNames[0])

        tmpBuildings = buildings.copy()

        print("entry pos:", entry.pos)
        dx, dy, dz = entry.pos
        entryPos: Location = (x+dx, y+dy, z+dz)
        print("entry pos(T):", entryPos)
        for dx in range(sizeX):
            for dy in range(sizeY):
                for dz in range(sizeZ):
                    x1, y1, z1 = x+dx, y+dy, z+dz
                    buildingBlk: Location = (x1, y1, z1)
                    if buildingBlk == entryPos:
                        continue
                    tmpBuildings.append(buildingBlk)

        ok = pathfind.buildRoad(entryPos, roads, tmpBuildings)

        if ok:
            size = nbt_builder.getStructureSizeNBT(nbt_struct)
            for ix in range(x, x + size[0]):
                for iz in range(z, z + size[2]):
                    for iy in range(WORLDSLICE.heightmaps["MOTION_BLOCKING"][(ix, iz)], y):
                        INTF.placeBlock(ix, iy, iz, "minecraft:dirt")
            nbt_builder.buildFromStructureNBT(nbt_struct, x, y, z, biome)
            buildings = tmpBuildings
            print(f"{'-'*25}build one finish{'-'*25}")
        else:
            print(f"{'-'*25}build one failed{'-'*25}")


def buildRoadDecoration():
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    data = roadDecoration(roads, 8, heights)
    for flower in data:
        [x, y, z, name] = flower
        INTF.placeBlock(x, y, z, name)
    return


def buildTreeDecoration():
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    data = treeDecoration(roads, 12, heights)
    nbt_struct = nbt.NBTFile(getBuildingNBTDir("tree"))

    for tree in data:
        [x, y, z] = tree
        nbt_builder.buildFromStructureNBT(nbt_struct, x, y, z, True)
    for road in roads:
        [x, y, z] = road
        INTF.placeBlock(x, y+1, z, "air")
        INTF.placeBlock(x, y+1, z, "air")
    return


def placeStreetLight(x: int, y: int, z: int):
    INTF.placeBlock(x, y, z, "cobblestone")
    INTF.placeBlock(x, y+1, z, "cobblestone_wall")
    INTF.placeBlock(x, y+2, z, "torch")


def buildLightDecoration():
    locs = lightDecoration(roads, 16, None)
    for loc in locs:
        placeStreetLight(*loc)


if __name__ == '__main__':
    try:
        height = WORLDSLICE.heightmaps["MOTION_BLOCKING"][(STARTX, STARTY)]
        # INTF.runCommand(f"tp @a {STARTX} {height} {STARTZ}")
        # print(f"/tp @a {STARTX} {height} {STARTZ}")
        buildBasicBuilding()
        buildRoadDecoration()
        buildTreeDecoration()
        buildLightDecoration()

        print("Done!")
    except KeyboardInterrupt:   # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")
