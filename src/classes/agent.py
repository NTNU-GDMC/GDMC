from typing import Callable
from gdpc.vector_tools import Rect
from .core import Core
from .baseagent import RunableAgent
from ..building_util.building import Building
from ..building_util.building_info import BuildingInfo, getJsonAbsPath


class BuildAgent(RunableAgent):
    def __init__(self, core: Core, analyzeFunction: Callable[[Core, Rect], float], buildingType: str) -> None:
        """Assume one agent one build one building for now"""
        super().__init__(core)
        # the larger value analyzeFunction returns, the better
        self.analysis = analyzeFunction
        self.buildingType = buildingType
        # FIXME: this is a temporary solution for the building info
        self.buildingInfo = BuildingInfo(getJsonAbsPath(buildingType, 1, 1))

    def run(self) -> bool:
        return self.analysisAndBuild()

    def analysisAndBuild(self) -> bool:
        """Request to build a building on the blueprint at bound"""
        length, width = self.buildingInfo.getCurrentBuildingLengthAndWidth()
        possibleLocation = self.core.getEmptyArea(
            length, width)
        if len(possibleLocation) == 0:
            return False
        bestLocation = possibleLocation[0]
        bestLocationValue = 0
        for location in possibleLocation:
            value = self.analysis(self.core, location)
            if value > bestLocationValue:
                bestLocationValue = value
                bestLocation = location
        building = Building(
            self.buildingType, self.buildingInfo.getCurrentBuildingType(), 1, bestLocation.begin)
        print(
            f"building position: {building.getBuildingPos()}, building level: {building.getBuildingLevel()}")
        # do something about the building class (add nessarry data to it)
        self.core.addBuilding(building)

        return True
