#! /usr/bin/python3
from poissionDiskSampling import poissionSample as pS
from NTNUBasicBuilding import InitialChalet
from math import floor
from gdpc import worldLoader as WL
from gdpc import toolbox as TB
from gdpc import interface as INTF
from gdpc import geometry as GEO
import pathfind
from pathfind import Location

# Here we read start and end coordinates of our build area
# STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea()
STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.setBuildArea(
    0, 1, 0, 500, 256, 500)
print("Build Area: ", *INTF.requestBuildArea())

# IMPORTANT: Keep in mind that a wold slice is a 'snapshot' of the world,
#   and any changes you make later on will not be reflected in the world slice
WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)

buildings: list[Location] = []
roads: list[Location] = []


def buildBasicBuilding():
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    coBuildingList = pS(STARTX, STARTZ, ENDX, ENDZ, 5, 10)
    print("coBuildingList:", coBuildingList)
    for pos in coBuildingList:
        x, z = pos
        x, z = floor(x), floor(z)
        y = int(heights[(x, z)])
        print(x, y, z)
        InitialChalet(x, y, z)

        INTF.runCommand(f"tp @a {x} {y} {z}")

        # buildingCenter = (x, y-1, z)
        road = (x, y-1, z-1)
        for dx in range(-2, 3):
            for dz in range(-1, 5):
                building = (x+dx, y-1, z+dz)
                if building == road:
                    continue                
                buildings.append(building)

        pathfind.buildRoad(road, roads, buildings)


if __name__ == '__main__':
    try:
        height = WORLDSLICE.heightmaps["MOTION_BLOCKING"][(STARTX, STARTY)]
        INTF.runCommand(f"tp @a {STARTX} {height} {STARTZ}")
        print(f"/tp @a {STARTX} {height} {STARTZ}")
        buildBasicBuilding()

        print("Done!")
    except KeyboardInterrupt:   # useful for aborting a run-away program
        print("Pressed Ctrl-C to kill program.")
