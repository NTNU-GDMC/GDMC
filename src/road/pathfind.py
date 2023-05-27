from astar import find_path
from random import choices
from gdpc.vector_tools import ivec2, Rect, l1Distance, l1Norm, neighbors2D, addY
from ..classes.core import Core
from ..road.road_network import RoadNode, RoadEdge
from ..config.config import config

UNIT = config.unit

# hash function of ivec2 for RoadNode


def hashfunc(o: object) -> int:
    if isinstance(o, ivec2):
        return o.to_tuple().__hash__()
    raise TypeError


def pathfind(
        core: Core,
        begin: RoadNode[ivec2],
        end: RoadNode[ivec2],
) -> RoadEdge[ivec2] | None:

    roadNetwork = core.roadNetwork
    boundingRect = core.buildArea.toRect()

    def exists(n: RoadNode[ivec2]) -> bool:
        return n in roadNetwork.subnodes

    def height(n: RoadNode[ivec2]):
        return round(core.getHeightMap("mean", Rect(n.val, (UNIT, UNIT))))

    def tooFar(n: RoadNode[ivec2]) -> bool:
        return l1Distance(n.val, begin.val) + l1Distance(n.val, end.val) > 2 * l1Distance(begin.val, end.val)

    def isRoad(n: RoadNode[ivec2]) -> bool:
        return core.blueprint[n.val.x//UNIT, n.val.y//UNIT] == -1

    def isEmpty(n: RoadNode[ivec2]) -> bool:
        return core.blueprint[n.val.x//UNIT, n.val.y//UNIT] == 0

    def neighbors(n: RoadNode[ivec2]):
        for neighbor in neighbors2D(n.val, boundingRect=boundingRect, stride=UNIT):
            node = roadNetwork.newNode(neighbor)

            if tooFar(node):
                continue

            if abs(height(node) - height(n)) > 1:
                continue

            if not isEmpty(node) and not isRoad(node):
                continue

            yield node

    # real distance
    def distance(a: RoadNode[ivec2], b: RoadNode[ivec2]) -> float:
        if exists(a) and exists(b):
            return 0.0

        delta2D = b.val - a.val

        # weight for distance
        delta3D = addY(delta2D, (height(b) - height(a))*2)

        return l1Norm(delta3D)

    # heuristic function
    def heuristic(a: RoadNode[ivec2], b: RoadNode[ivec2]) -> float:
        dis = l1Distance(a.val, b.val)
        totalDis = l1Distance(begin.val, end.val)

        if dis / totalDis < 0.25:
            dis *= 0.8
        else:
            dis *= 3

        if exists(a):
            dis *= 0.5

        return dis

    def isGoal(a: RoadNode[ivec2], b: RoadNode[ivec2]) -> bool:
        return a == b

    path = find_path(begin,
                     end,
                     neighbors_fnct=neighbors,
                     reversePath=True,
                     heuristic_cost_estimate_fnct=heuristic,
                     distance_between_fnct=distance,
                     is_goal_reached_fnct=isGoal)

    if path is None:
        return None

    return RoadEdge(list(path))
