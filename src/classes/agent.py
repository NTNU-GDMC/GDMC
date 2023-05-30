import math
import time
from random import sample, choices, choice
from typing import Callable
from gdpc.vector_tools import Rect, ivec2, l1Distance, dropY
from .core import Core
from .event import Observer, BuildEvent
from .baseagent import RunableAgent, withCooldown, Agent
from ..building.master_building_info import GLOBAL_BUILDING_INFO
from ..building.building import Building
from ..config.config import config
from ..road.road_network import RoadEdge, RoadNode
from ..road.pathfind import pathfind

UNIT = config.unit
COOLDOWN = config.agentCooldown
ANALYZE_THRESHOLD = config.analyzeThreshold


class BuildAgent(RunableAgent):
    def __init__(self, core: Core, analyzeFunction: Callable[[Core, Rect], float], buildingName: str, cooldown: int = COOLDOWN, special: bool = False) -> None:
        """Assume one agent one build one building for now"""
        super().__init__(core, cooldown)
        # the larger value analyzeFunction returns, the better
        self.analysis = analyzeFunction
        self.buildingName = buildingName
        # FIXME: this is a temporary solution for the building info
        self.buildingInfo = choice(GLOBAL_BUILDING_INFO[buildingName])
        self.speical = special

    def __str__(self) -> str:
        return f"BuildAgent({self.buildingInfo})"

    def __repr__(self) -> str:
        return self.__str__()

    @withCooldown
    def run(self) -> bool:
        maxLevel = len(self.buildingInfo.structures)
        levels = [level for level in range(1, maxLevel+1)]

        def calcWeight(level: int):
            num = self.core.numberOfBuildings(level)
            limit = self.core.getBuildingLimit(level)

            if limit == 0:
                return 0
            return 1 - num / limit

        weights = [calcWeight(level) for level in levels]

        if all([weight == 0 for weight in weights]):
            print("No building can be built, all building limit reached")
            return False

        level = choices(levels, weights=weights, k=1)[0]

        if not self.core.canBuildOrUpgradeTo(level):
            return False

        if level == 1:
            return self.analysisAndBuild()

        return self.upgrade(level)

    def rest(self) -> bool:
        resourceType = self.core.getMostLackResource(
            self.core.resources, self.core.resourceLimit)
        if resourceType != "none":
            self.gatherResource(resourceType)
            return True
        return False

    def analysisAndBuild(self) -> bool:
        """Request to build a building on the blueprint at bound"""

        if self.core.resources < self.buildingInfo.structures[0].requirement:
            print("Agent: not enough resources")
            return False

        print("Agent: analysis and build")

        size = self.buildingInfo.max_size
        possibleLocations = self.core.getEmptyArea(dropY(size))

        if len(possibleLocations) == 0:
            return False

        bestLocation = None
        bestLocationValue = 0

        buildArea = self.core.buildArea.toRect()

        print(f"Analyzing {len(possibleLocations)} locations...")

        timeStart = time.time()
        print("Analyzing...")
        for location in sample(possibleLocations, len(possibleLocations)):
            # FIXME: this is a temporary solution for checking if the location is in the build area

            def inBuildArea():
                return buildArea.contains(location.begin) and buildArea.contains(location.last)

            if not inBuildArea():
                continue

            value = self.analysis(self.core, location)

            if value < ANALYZE_THRESHOLD:
                continue

            if value <= bestLocationValue:
                continue

            bestLocationValue = value
            bestLocation = location

        print(f"Analysis done, Time used: {time.time() - timeStart:.2f}s")

        if bestLocation is None:
            print("Agent: no suitable location found")
            return False

        building = Building(self.buildingInfo, bestLocation.begin)
        print(
            f"Build '{building.building_info.type}' at position: {building.position.to_tuple()}")

        self.core.addBuilding(building)
        self.core.buildSubject.notify(BuildEvent(building))

        print(f"Agent: {self.buildingInfo.type} built")

        return True

    def upgrade(self, buildingLevel) -> bool:
        buildings = list(self.core.getBuildings(
            buildingLevel=buildingLevel-1, buildingType=self.buildingInfo.type))

        if len(buildings) == 0:
            return False

        building = choice(buildings)
        building.level += 1

        return True

    def gatherResource(self, resourceType: str):
        # gain 5% of the limit
        self.core.resources[resourceType] += math.ceil(
            self.core.resourceLimit[resourceType] * 0.05)


class RoadAgent(Agent):
    def __init__(self, core: Core) -> None:
        Agent.__init__(self, core)
        self.buildObserver = Observer[BuildEvent](self, self.onBuild)
        self.core.buildSubject.attach(self.buildObserver)

    def __del__(self) -> None:
        self.core.buildSubject.detach(self.buildObserver)

    def onBuild(self, event: BuildEvent) -> None:
        self.connectRoadTo(event.building)

    def connectRoadTo(self, building: Building):
        """Connect the building to the road network"""
        entryPos = building.entryPos
        if entryPos is None:
            return

        # align the entryPos to the grid
        entryPos = (entryPos // UNIT) * UNIT

        roadNetwork = self.core.roadNetwork

        begin = roadNetwork.newNode(entryPos)

        nodes = list(roadNetwork.nodes)

        # if there is no node in the network, just add the node
        if len(nodes) == 0:
            roadNetwork.addNode(begin)
            x, y = entryPos//UNIT
            self.core.blueprint[x, y] = -1
            return

        def calcWeight(node: RoadNode[ivec2]):
            dis = l1Distance(node.val, begin.val)
            return 1/dis if dis != 0 else 10

        weights = list(map(calcWeight, nodes))
        end = choices(nodes, weights=weights, k=1)[0]

        print(
            f"Connecting {begin.val.to_tuple()} -> {end.val.to_tuple()}...", end=" ")

        edge = pathfind(self.core, begin, end)

        if edge is None:
            print("Failed.")
            return

        print("Done.")

        print(f"Adding edge to road network...")

        self.core.addRoadEdge(edge)

        print(f"Adding edge done.")
