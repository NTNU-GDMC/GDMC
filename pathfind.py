from typing import Iterable, Union
from gdpc import world_slice as WL
from gdpc import minecraft_tools as TB
from gdpc import interface as INTF
from gdpc import geometry as GEO
from gdpc import vector_tools as VT
from gdpc import Editor, Block
import astar
import random
from gdpc.vector_tools import *


def groundY(point: ivec2, heights: np.ndarray) -> int:
    return heights[*point]-1


def setGroundY2D(point: ivec2, heights: np.ndarray) -> ivec3:
    return addY(point, groundY(point, heights))


def setGroundY3D(point: ivec3, heights: np.ndarray) -> ivec3:
    return setGroundY2D(dropY(point), heights)


# fix path y around target
def fixedPath(path: list[ivec3], targetY: int):
    for i in range(len(path)):
        if i != 0:
            if targetY > path[i][1]:
                targetY -= 1
            elif targetY < path[i][1]:
                targetY += 1

        # break if already at target y
        if path[i][1] == targetY:
            break

        newLoc = setY(path[i], targetY)
        print(f"fixing path: {path[i]} -> {newLoc}")
        path[i] = newLoc

    return path


def pathFind(
    start: ivec3,
    target: ivec3,
    exists: set[ivec3],
    ignores: set[ivec3],
    buildArea: VT.Box,
    heights: np.ndarray,
) -> Union[Iterable[ivec3], None]:

    # return true if n is too far to start and target
    def tooFar(n: ivec3) -> bool:
        return l1Distance(n, start) + l1Distance(n, target) > 2 * l1Distance(start, target)

    # get neighbors of n
    def neighbors(n: ivec3):
        for (x1, z1) in neighbors2D(dropY(n), buildArea.toRect()):
            n1 = setGroundY2D((x1, z1), heights)

            # skip if too far
            if tooFar(n1):
                continue

            # skip if delta y is > 1
            if abs(n[1]-n1[1]) > 1:
                continue

            # skip if not in build area
            if not buildArea.contains(n1):
                continue

            # skip if in ignore list
            if n1 in ignores:
                continue

            yield n1

    # real distance
    def adjDistance(n1: ivec3, n2: ivec3) -> float:
        if n1 in exists and n2 in exists:
            return 0.0

        delta = n2 - n1

        # weight for distance
        delta = setY(delta, delta[1] * 2)

        return l1Norm(delta)

    # heuristic cost
    def cost(n: ivec3, goal: ivec3) -> float:
        dis = l1Distance(n, goal)

        if dis / l1Distance(start, goal) < 0.25:
            dis *= 0.8
        else:
            dis *= 3

        if n in exists:
            dis *= 0.5

        return dis

    # check if n is goal
    def isReached(n: ivec3, goal: ivec3):
        return n == goal

    return astar.find_path(start,
                           target,
                           neighbors_fnct=neighbors,
                           reversePath=True,
                           heuristic_cost_estimate_fnct=cost,
                           distance_between_fnct=adjDistance,
                           is_goal_reached_fnct=isReached)


def buildRoad(target: Vec3iLike,
              roads: list[Vec3iLike],
              buildings: list[Vec3iLike],
              block: Block = Block("minecraft:dirt_path")):
    editor = Editor(buffering=True)
    buildArea = INTF.getBuildArea()
    WORLDSLICE = WL.WorldSlice(buildArea.toRect())
    heights = WORLDSLICE.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    # run astar with retries
    def run(retries: int = 1) -> Union[Iterable[ivec3], None]:
        if len(roads) == 0:
            return iter([target])

        def randomStart():
            return random.choice(list(roads))

        start = randomStart()

        print("[astar] searching...")
        print(f"start: {start}, target: {target}")
        res = pathFind(
            start=start,
            target=setGroundY3D(target, heights),
            exists=roads,
            ignores=buildings,
            buildArea=buildArea,
            heights=heights)
        if res == None and retries > 0:
            return run(retries-1)
        return res

    res = run()
    if res is None:
        print("[astar] searching failed!")
        return False
    print("[astar] searching sucessful!")

    path = fixedPath(list(res), target[1])

    for loc in path:
        roads.append(loc)

        # remove blocks above
        ground = groundY(dropY(loc), heights)
        if loc.y < ground:
            for i in range(ground, loc.y, -1):
                editor.placeBlock(setY(loc, i), Block("minecraft:air"))

        editor.placeBlock(loc, block)

    return True
