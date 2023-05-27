from random import sample, choices
from typing import Callable
from gdpc.vector_tools import Rect, ivec2, l1Distance
from .core import Core
from .event import Observer, BuildEvent
from .baseagent import RunableAgent, withCooldown, Agent
from ..building.master_building_info import GLOBAL_BUILDING_INFO
from ..building.building import Building
from ..config.config import config
from ..road.road_network import RoadEdge, RoadNode

UNIT = config.unit


class BuildAgent(RunableAgent):
    def __init__(self, core: Core, analyzeFunction: Callable[[Core, Rect], float], buildingType: str, cooldown: int) -> None:
        """Assume one agent one build one building for now"""
        super().__init__(core, cooldown)
        # the larger value analyzeFunction returns, the better
        self.analysis = analyzeFunction
        self.buildingType = buildingType
        # FIXME: this is a temporary solution for the building info
        self.buildingInfo = GLOBAL_BUILDING_INFO[buildingType][0]

    def __str__(self) -> str:
        return f"BuildAgent({self.buildingInfo})"

    def __repr__(self) -> str:
        return self.__str__()

    @withCooldown
    def run(self) -> bool:
        return self.analysisAndBuild()

    def analysisAndBuild(self) -> bool:
        """Request to build a building on the blueprint at bound"""
        length, _, width = self.buildingInfo.max_size
        possibleLocations = self.core.getEmptyArea(
            length, width)
        if len(possibleLocations) == 0:
            return
        bestLocation = possibleLocations[0]
        bestLocationValue = 0
        buildArea = self.core._editor.getBuildArea().toRect()
        for location in sample(possibleLocations, len(possibleLocations)):
            # FIXME: this is a temporary solution for checking if the location is in the build area

            def inBuildArea():
                return buildArea.contains(location.begin) and buildArea.contains(location.last)

            if not inBuildArea():
                continue

            value = self.analysis(self.core, location)
            if value > bestLocationValue:
                bestLocationValue = value
                bestLocation = location
        building = Building(self.buildingInfo, bestLocation.begin)
        print(
            f"building position: {building.position}, building level: {building.level}")
        # do something about the building class (add necessary data to it)
        self.core.addBuilding(building)
        self.core.buildSubject.notify(BuildEvent(building))

        return True


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
        entryPos = building.entryPos
        if entryPos is None:
            return

        roadNetwork = self.core.roadNetwork

        nodes = list(roadNetwork.nodes)
        begin = entryPos // UNIT
        weights = list(map(lambda node: 1/l1Distance(node.val, begin), nodes))
        end = choices(nodes, weights=weights, k=1)[0].val

        # TODO: add a path finding algorithm here

        path: list[RoadNode[ivec2]] = [RoadNode(begin), RoadNode(end)]
        edge: RoadEdge[ivec2] = RoadEdge(path)
        roadNetwork.addEdge(edge)

        for node in path:
            for pos in Rect(node.val, ivec2(UNIT, UNIT)).inner:
                self.core.blueprint[pos.x, pos.y] = -1
