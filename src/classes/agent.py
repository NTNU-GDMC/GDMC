import time
from math import ceil
from random import sample, choices, choice
from typing import Callable
from gdpc.vector_tools import Rect, ivec2, l1Distance, dropY
from .core import Core
from .event import Observer, BuildEvent
from .baseagent import RunableAgent, withCooldown, Agent
from ..building.master_building_info import GLOBAL_BUILDING_INFO, BuildingInfo
from ..building.building import Building
from ..config.config import config
from ..road.road_network import RoadEdge, RoadNode
from ..road.pathfind import pathfind

UNIT = config.unit
SAMPLE_RATE = config.sampleRate
MAX_SAMPLE_TIMES = config.maxSampleTimes
NO_SUITABLE_LOCATION_PENALTY = config.noSuitableLocationPenalty


class BuildAgent(RunableAgent):
    def __init__(self, core: Core, analyzeFunction: Callable[[Core, Rect, BuildingInfo], float], buildingName: str, cooldown: int = 0) -> None:
        """Assume one agent one build one building for now"""
        super().__init__(core, cooldown)
        # the larger value analyzeFunction returns, the better
        self.analysis = analyzeFunction
        self.buildingName = buildingName
        # FIXME: this is a temporary solution for the building info
        self.buildingInfo = choice(GLOBAL_BUILDING_INFO[buildingName])

    def __str__(self) -> str:
        return f"BuildAgent({self.buildingInfo.type})"

    def __repr__(self) -> str:
        return self.__str__()

    @withCooldown
    def run(self) -> bool:
        core = self.core
        maxLevel = self.buildingInfo.maxLevel
        levels = [level for level in range(1, maxLevel+1)]

        def calcWeight(level: int):
            num = core.numberOfBuildings(level)
            limit = core.getBuildingLimit(level)

            if limit == 0:
                return 0
            return 1 - num / limit

        weights = [calcWeight(level) for level in levels]

        if all([weight == 0 for weight in weights]):
            print("No building can be built, all building limit reached")
            return False

        level = choices(levels, weights=weights, k=1)[0]

        if not core.canBuildOrUpgradeTo(level):
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

        print(f"{self}: Start analysis and build")

        core = self.core
        buildingInfo = self.buildingInfo

        if core.resources < buildingInfo.structures[0].requirement:
            print(f"No enough resources to build")
            return False

        size = buildingInfo.max_size
        possibleLocations = core.getEmptyArea(dropY(size))
        numPossibleLocations = len(possibleLocations)

        bestLocation = None
        bestLocationValue = 0

        print(f"Analyzing {numPossibleLocations} locations...")

        timeStart = time.time()

        possibleLocations = sample(possibleLocations, numPossibleLocations)

        def getNextCheckIndex(lastIndex: int = 0):
            sampleTimes = ceil((numPossibleLocations-lastIndex) * SAMPLE_RATE)
            return lastIndex + min(sampleTimes, MAX_SAMPLE_TIMES)

        nextCheckIndex = getNextCheckIndex()
        for i in range(numPossibleLocations):
            if i == nextCheckIndex:
                print(f"{i}/{numPossibleLocations} locations analyzed")
                if bestLocation is not None:
                    break
                nextCheckIndex = getNextCheckIndex(i)

            location = possibleLocations[i]

            value = self.analysis(core, location, buildingInfo)

            if value == 0:
                continue

            if value <= bestLocationValue:
                continue

            bestLocationValue = value
            bestLocation = location

        print(f"Analysis done, Time used: {time.time() - timeStart:.2f}s")

        if bestLocation is None:
            print("No suitable location found")
            self.remainCD += self.cooldown * NO_SUITABLE_LOCATION_PENALTY
            return False

        building = Building(buildingInfo, bestLocation.begin)
        print(
            f"Build {buildingInfo.type} at position: {building.position.to_tuple()}")

        core.addBuilding(building)
        core.buildSubject.notify(BuildEvent(building))

        return True

    def upgrade(self, buildingLevel: int) -> bool:
        core = self.core

        buildings = list(core.getBuildings(
            buildingLevel=buildingLevel-1, buildingType=self.buildingInfo.type))

        if len(buildings) == 0:
            return False

        building = choice(buildings)
        building.level += 1

        return True

    def gatherResource(self, resourceType: str):
        # gain 5% of the limit
        self.core.resources[resourceType] += ceil(
            self.core.resourceLimit[resourceType] * 0.05)


class RoadAgent(RunableAgent):
    def __init__(self, core: Core, cooldown: int = 0) -> None:
        super().__init__(core, cooldown)
        self.buildObserver = Observer[BuildEvent](self, self.onBuild)
        self.core.buildSubject.attach(self.buildObserver)

    def __del__(self) -> None:
        self.core.buildSubject.detach(self.buildObserver)

    @withCooldown
    def run(self) -> bool:
        components = self.core.roadNetwork.components

        if len(components) < 2:
            return False

        def calcWeight(component: set[RoadNode[ivec2]]):
            return 1/len(component)

        weights = map(calcWeight, components)

        beginCompoent = choices(
            components, weights=weights, k=1)[0]
        begin = choice(list(beginCompoent))

        otherComponents: list[set[RoadNode[ivec2]]] = filter(
            lambda component: component != beginCompoent, components)
        endComponent = choices(otherComponents, weights=self._calcWeights(
            begin, map(choice, otherComponents)), k=1)[0]
        end = choice(list(endComponent))
        return self.connectRoad(begin, end)

    def rest(self) -> bool:
        resourceType = self.core.getMostLackResource(
            self.core.resources, self.core.resourceLimit)
        if resourceType != "none":
            self.gatherResource(resourceType)
            return True
        return False

    def _calcWeights(self, begin: RoadNode[ivec2], nodes: list[RoadNode[ivec2]]) -> list[float]:
        def calcWeight(node: RoadNode[ivec2]):
            dis = max(l1Distance(node.val, begin.val), 1)
            return 1/dis

        weights = list(map(calcWeight, nodes))
        return weights

    def onBuild(self, event: BuildEvent) -> None:
        """When a building is built, connect it to the road network"""

        roadNetwork = self.core.roadNetwork
        entryPos = event.building.entryPos
        if entryPos is None:
            return

        # align the entryPos to the grid
        entryPos = (entryPos // UNIT) * UNIT

        begin = roadNetwork.newNode(entryPos)
        roadNetwork.addNode(begin)
        self.connectRoadToNear(begin)

    def connectRoadToNear(self, begin: RoadNode[ivec2]) -> bool:
        """Connect the building to the road network"""
        roadNetwork = self.core.roadNetwork

        others = list(filter(lambda node: node != begin, roadNetwork.nodes))

        if len(others) == 0:
            return False

        weights = self._calcWeights(begin, others)
        end = choices(others, weights=weights, k=1)[0]

        return self.connectRoad(begin, end)

    def connectRoad(self, begin: RoadNode[ivec2], end: RoadNode[ivec2]) -> bool:
        """Connect two nodes in the road network"""

        if begin == end:
            return False

        core = self.core

        print(
            f"Connecting road: {begin.val.to_tuple()} -> {end.val.to_tuple()}...")

        edge = pathfind(core, begin, end)
        if edge is None:
            print("Connecting road failed")
            return False
        print("Connecting road done")

        print("Update road network...")
        core.addRoadEdge(edge)
        print("Update road network done")

        return True

    def gatherResource(self, resourceType: str):
        # gain 5% of the limit
        self.core.resources[resourceType] += ceil(
            self.core.resourceLimit[resourceType] * 0.05)
