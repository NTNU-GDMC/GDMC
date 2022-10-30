from typing import Iterable, Union
from gdpc import worldLoader as WL
from gdpc import toolbox as TB
from gdpc import interface as INTF
from gdpc import geometry as GEO
import math
import astar
import pprint

Location = tuple[int, int, int]
Area = tuple[int, int, int, int, int, int]

# STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = INTF.requestBuildArea(
#     0, 1, 0, 500, 10, 500)
# WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)

dirs: dict[str, tuple[int, int]] = {
    "north": (0, 1),
    "east": (1, 0),
    "south": (0, -1),
    "west": (-1, 0),
}


def pathFind(start: Location,
             exists: list[Location] = [],
             ignores: list[Location] = [],
             buildArea: Area = INTF.globalBuildArea) -> Union[Iterable, None]:
    STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = buildArea
    WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    # print(f'start: {start}')
    # print('exists:')
    # pprint.pprint(exists)
    # print('ignores:')
    # pprint.pprint(ignores)

    # first init
    if exists == []:
        exists.append(start)
        INTF.placeBlock(*start, "gravel")
        return iter(exists)

    def neighbors(n: Location):
        # print(f'neighbors: {n}')
        x, y, z = n
        for _, (dx, dz) in dirs.items():
            x1, z1 = x + dx, z + dz

            # check if x1 and z1 out of bound
            if x1 not in range(STARTX, ENDX+1) or \
                    z1 not in range(STARTZ, ENDZ+1):
                continue

            y1 = heights[(x1, z1)]-1

            # check if x1, y1, z1 out of bound
            if (INTF.checkOutOfBounds(x1, y1, z1)):
                continue

            # height diff not greater than 1
            if abs(y1-y) > 1:
                continue

            n1: Location = (x1, y1, z1)
            # skip ingores
            if n1 in ignores:
                continue
            # print(f'available: {(x1, y1, z1)}')
            yield n1

    def distance(n1: Location, n2: Location):
        x1, y1, z1 = n1
        x2, y2, z2 = n2
        if (abs(x2-x1) + abs(z2-z1) == 1):
            return math.dist(n1, n2)

    def cost(n: Location, goals: list[Location]):
        x1, y1, z1 = n
        dis = min([math.dist((x1, z1), (x2, z2))
                   for (x2, y2, z2) in goals])
        # print(f'dis({n}) = {dis}')
        return dis

    def isReached(n: Location, goals: list[Location]):
        return n in goals

    return astar.find_path(start, exists, neighbors_fnct=neighbors,
                           heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance,
                           is_goal_reached_fnct=isReached)


def buildRoad(start: Location,
              roads: list[Location] = [],
              buildings: list[Location] = [],
              ):
    res = pathFind(start, roads, buildings)
    if res == None:
        print('astar failed')
        print(f'build road from: {start}')
        print('build road to:')
        pprint.pprint(roads)
        return

    path = list(res)
    for x, y, z in path:
        loc: Location = (x, y, z)
        roads.append(loc)
        INTF.placeBlock(*loc, "gravel")
