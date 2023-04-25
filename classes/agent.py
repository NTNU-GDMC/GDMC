import abc
from typing import Callable
from gdpc.vector_tools import Rect
from .core import Core
from BuildingUtil.building import Building
from BuildingUtil.buildingInfo import BuildingInfo

class Agent():
    def __init__(self, core: Core) -> None:
        self.core = core

    @abc.abstractmethod
    def run(self) -> None:
        pass


class BuildAgent(Agent):
    def __init__(self, core: Core, analyzeFunction: Callable[[Core, Rect], int], buildingType: str) -> None:
        """Assume one agent one build one building for now"""
        super().__init__(core)
        self.analysis = analyzeFunction
        self.buildingType = buildingType
        self.buidlingInfo = BuildingInfo(buildingType)

    def run(self):
        self.analysisAndBuild()

    def analysisAndBuild(self):
        """Request to build a building on the blueprint at bound"""
        length, width = self.buidlingInfo.getCurrentBuildingLengthAndWidth()
        possibleLocation = self.core.getEmptyArea(length, width)
        if len(possibleLocation) == 0:
            return
        bestLocation = possibleLocation[0]
        bestLocationValue = 0
        for location in possibleLocation:
            value = self.analysis(self.core, location)
            if value > bestLocationValue:
                bestLocationValue = value
                bestLocation = location

        building = Building(self.buildingType, self.buidlingInfo.getCurrentBuildingType(), bestLocation)
        # do something about the building class (add nessarry data to it)
        self.core.addBuilding(building)
