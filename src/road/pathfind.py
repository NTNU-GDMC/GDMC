import numpy as np
from astar import find_path
from gdpc.vector_tools import ivec2, Rect, l1Distance, l1Norm, neighbors2D, addY
from ..classes.core import Core
from ..road.road_network import RoadNode, RoadEdge
from ..config.config import config

UNIT = config.unit


class Pathfinder(object):
    def __init__(self, core: Core, begin: RoadNode[ivec2], end: RoadNode[ivec2]) -> None:
        self._core = core
        self._begin = begin
        self._end = end

    @property
    def core(self):
        return self._core

    @property
    def begin(self):
        return self._begin

    @property
    def end(self):
        return self._end

    @property
    def blueprint(self):
        return self._core.blueprint

    @property
    def roadNetwork(self):
        return self._core.roadNetwork

    @property
    def boundingRect(self):
        return Rect((0, 0), self._core.buildArea.toRect().size)

    def height(self, n: RoadNode[ivec2]):
        """Height of a node"""
        return round(self._core.getHeightMap("mean", Rect(n.val, (UNIT, UNIT))))

    def tooFar(self, n: RoadNode[ivec2]) -> bool:
        """Whether the node is too far from the begin and end nodes"""
        return l1Distance(n.val, self.begin.val) + l1Distance(n.val, self.end.val) > 2 * l1Distance(self.begin.val, self._end.val)

    def isBuilding(self, n: RoadNode[ivec2]) -> bool:
        """Whether the node is a building"""
        return self.blueprint[n.val.x//UNIT, n.val.y//UNIT] > 0

    def isLiquid(self, n: RoadNode[ivec2]) -> bool:
        """Whether the node is liquid"""
        return np.sum(self.core.liquidMap[n.val.x:n.val.x+UNIT, n.val.y:n.val.y+UNIT]) > 2

    def neighbors(self, n: RoadNode[ivec2]):
        """Neighbors of a node"""
        yield from self.mainNeighbors(n)
        yield from self.subNeighbors(n)

    def mainNeighbors(self, n: RoadNode[ivec2]):
        yield from self.roadNetwork.neighbors(n)

    def subNeighbors(self, n: RoadNode[ivec2]):
        """Sub neighbors of a node"""
        for pos in neighbors2D(n.val, boundingRect=self.boundingRect, stride=UNIT):
            neighbor = self.roadNetwork.newNode(pos)

            if self.tooFar(neighbor):
                continue

            if abs(self.height(neighbor) - self.height(n)) > 1:
                continue

            if self.isBuilding(neighbor):
                continue

            yield neighbor

    def distance(self, a: RoadNode[ivec2], b: RoadNode[ivec2]) -> float:
        """Real distance between two nodes"""
        if self.roadNetwork.edge(a, b) is not None:
            return 0

        delta2D = b.val - a.val
        delta3D = addY(delta2D, (self.height(b) - self.height(a))*2)
        dis = l1Norm(delta3D)

        hotness = self.roadNetwork.hotness(a) + self.roadNetwork.hotness(b)
        dis /= 1+hotness

        if self.isLiquid(a) or self.isLiquid(b):
            dis *= 10

        return dis

    def heuristic(self, a: RoadNode[ivec2], b: RoadNode[ivec2]) -> float:
        """Heuristic distance between two nodes"""
        dis = l1Distance(a.val, b.val)

        hotness = self.roadNetwork.hotness(a)
        dis /= 1+hotness

        if self.isLiquid(a) or self.isLiquid(b):
            dis *= 5

        return dis

    def isGoal(self, a: RoadNode[ivec2], b: RoadNode[ivec2]) -> bool:
        """Check if goal is reached"""
        return a == b


def pathfind(
    core: Core,
    begin: RoadNode[ivec2],
    end: RoadNode[ivec2],
) -> RoadEdge[ivec2] | None:

    pathfinder = Pathfinder(core, begin, end)

    path = find_path(begin,
                     end,
                     neighbors_fnct=pathfinder.neighbors,
                     reversePath=True,
                     heuristic_cost_estimate_fnct=pathfinder.heuristic,
                     distance_between_fnct=pathfinder.distance,
                     is_goal_reached_fnct=pathfinder.isGoal)

    if path is None:
        return None

    expandedPath = list[RoadNode[ivec2]]()

    def append(node: RoadNode[ivec2]):
        if not expandedPath or expandedPath[-1] != node:
            expandedPath.append(node)

    prevNode: RoadNode[ivec2] | None = None
    for node in path:
        if prevNode is None:
            append(node)
            prevNode = node
            continue

        edge = core.roadNetwork.edge(prevNode, node)

        if edge is None:
            append(node)
            prevNode = node
            continue

        for subNode in edge:
            append(subNode)

        prevNode = node

    return RoadEdge(expandedPath)
