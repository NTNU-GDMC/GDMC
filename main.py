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

# Here we read start and end coordinates of our build area
# STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()
STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.setBuildArea(
    0, 1, 0, 200, 255, 200)
print("Build Area: ", *INTF.requestBuildArea())

# IMPORTANT: Keep in mind that a wold slice is a 'snapshot' of the world,
#   and any changes you make later on will not be reflected in the world slice
WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)

buildings: list[Location] = []
roads: list[Location] = []

STRUCTURE_DIR = os.path.abspath("./data/structures")
# BUILDING_TYPE = ["chalet", "chalet_2", "modern_house"]
BUILDING_TYPE = ["nbt_example"]


def getBuildingDir(name: str):
    return os.path.join(STRUCTURE_DIR, name)


def getBuildingNBTDir(name: str):

    return os.path.join(getBuildingDir(name), f"{name}.nbt")


def getBuildingInfoDir(name: str):
    return os.path.join(getBuildingDir(name), f"{name}.json")


def buildBasicBuilding():
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    buildArea = getSmoothChunk(heights)
    coBuildingList = pS(STARTX, STARTZ, ENDX, ENDZ, 5, 30, buildArea)

    print("coBuildingList:")
    pprint.pprint(coBuildingList)

    x, z = coBuildingList[0]
    INTF.runCommand(f"tp @a {x} 100 {z}")

    for pos in coBuildingList:
        x, z = pos
        x, z = floor(x), floor(z)

        y = int(heights[(x, z)])
        x = int(x + STARTX)
        z = int(z + STARTZ)
        print(x, y, z)

        buildingType = random.choice(BUILDING_TYPE)

        nbt_struct = nbt.NBTFile(getBuildingNBTDir(buildingType))
        nbt_builder.buildFromStructureNBT(nbt_struct, x, y, z)

        sizeX, sizeY, sizeZ = tmp = map(
            lambda e: int(e.value), nbt_struct["size"])
        print("size x, y, z:", sizeX, sizeY, sizeZ)

        buildingInfo = BEI.BuildingInfo(getBuildingInfoDir(buildingType))

        entryNames = buildingInfo.getBuildingNameList()
        entry = buildingInfo.getEntryInfo(entryNames[0])

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
                    buildings.append(buildingBlk)

        pathfind.buildRoad(start=entryPos, roads=roads, buildings=buildings)
        print(f"{'-'*50}build one finish")


def buildRoadDecoration():
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    data = roadDecoration(roads, 8, heights)
    for flower in data:
        [x, y, z, name] = flower
        INTF.placeBlock(x, y, z, name)
    for road in roads:
        [x, y, z] = road
        INTF.placeBlock(x, y+1, z, "air")
        INTF.placeBlock(x, y+1, z, "air")
    return


if __name__ == '__main__':
    try:
        height = WORLDSLICE.heightmaps["MOTION_BLOCKING"][(STARTX, STARTY)]
        # INTF.runCommand(f"tp @a {STARTX} {height} {STARTZ}")
        # print(f"/tp @a {STARTX} {height} {STARTZ}")
        buildBasicBuilding()
        buildRoadDecoration()
        print("Done!")
    except KeyboardInterrupt:   # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")
