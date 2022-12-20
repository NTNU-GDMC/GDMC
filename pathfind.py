from typing import Iterable, Union
from gdpc import worldLoader as WL
from gdpc import toolbox as TB
from gdpc import interface as INTF
from gdpc import geometry as GEO
import math
import astar
import pprint
import random
from interface import Interface

intf = Interface()

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


def pathFind(target: Location,
             exists: list[Location] = [],
             ignores: list[Location] = [],
             buildArea: Area = INTF.requestBuildArea()) -> Union[Iterable, None]:
    STARTX, STARTY, STARTZ, ENDX, ENDY, ENDZ = buildArea
    WORLDSLICE = WL.WorldSlice(STARTX, STARTZ, ENDX + 1, ENDZ + 1)
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    # first init
    if exists == []:
        return iter([target])

    existsDict = dict.fromkeys(exists)
    ignoresDict = dict.fromkeys(ignores)

    start = exists[0]

    def randomStart():
        return random.choice(exists)

    # print('exists:')
    # pprint.pprint(exists)
    # print('ignores:')
    # pprint.pprint(ignores)

    def height(x: int, z: int) -> int:
        return int(heights[(x, z)])-1

    def neighbors(n: Location):
        # print(f'neighbors: {n}')
        x, y, z = n
        for _, (dx, dz) in dirs.items():
            x1, z1 = x + dx, z + dz

            # check if x1 and z1 out of bound
            if x1 < STARTX or x1 > ENDX or z1 < STARTZ or z1 > ENDZ:
                continue

            dys = [0]

            if math.dist((x1, z1), (start[0], start[2])) < 3 or \
                    math.dist((x1, z1), (target[0], target[2])) < 3:
                dys += [-1, 1]

            for dy in dys:
                y1 = height(x1, z1) + dy

                # check if x1, y1, z1 out of bound
                if y1 < STARTY or y1 > ENDY:
                    continue

                # height diff not greater than 1
                if abs(y1-y) > 1:
                    continue

                n1: Location = (x1, y1, z1)
                # skip ingores
                if n1 in ignoresDict:
                    continue
                yield n1

    def distance(n1: Location, n2: Location):
        if n1 in existsDict and n2 in existsDict:
            return 0.0
        x1, y1, z1 = n1
        x2, y2, z2 = n2
        wx, wy, wz = 1, 1.2, 1
        dx, dy, dz = abs(x2-x1), abs(y2-y1), abs(z2-z1)
        if dx + dz == 1:
            dis = math.sqrt((dx*wx)**2 + (dy*wy)**2 + (dz*wz)**2)
            if y1 != height(x1, z1) or y2 != height(x2, z2):
                dis += 0.5
            return dis

    def cost(n: Location, goal: Location):
        dis = math.dist(n, goal)
        if dis / math.dist(start, goal) < 0.25:
            dis *= 0.8
        else:
            dis *= 3
        return dis

    def isReached(n: Location, goal: Location):
        return n == goal

    def run(retries: int = 1) -> Union[Iterable, None]:
        start = randomStart()
        print(f'start: {start}, target: {target}')
        res = astar.find_path(start, target, neighbors_fnct=neighbors,
                              heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance,
                              is_goal_reached_fnct=isReached)
        if res == None and retries > 0:
            return run(retries-1)
        return res

    return run()


def buildRoad(start: Location,
              roads: list[Location] = [],
              buildings: list[Location] = [],
              blocks: any = "grass_path"):
    res = pathFind(start, roads, buildings)
    if res == None:
        print('astar failed')
        print(f'build road from: {start}')
        print('build road to:')
        pprint.pprint(roads)
        return False

    path = list(res)
    for x, y, z in path:
        loc: Location = (x, y, z)
        roads.append(loc)
        if INTF.getBlock(x, y+1, z) != "minecraft:air":
            INTF.placeBlock(x, y+1, z, "air")
        INTF.placeBlock(*loc, blocks)

    return True
