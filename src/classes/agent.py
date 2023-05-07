from typing import Callable
from gdpc.vector_tools import Rect
from .core import Core
from .baseagent import RunableAgent
from ..building.building import Building
from ..building.master_building_info import GLOBAL_BUILDING_INFO
from ..building.building_info import BuildingInfo


class BuildAgent(RunableAgent):
    buildingInfo: BuildingInfo

    def __init__(self, core: Core, analyzeFunction: Callable[[Core, Rect], int], buildingType: str) -> None:
        """Assume one agent one build one building for now"""
        super().__init__(core)
        self.analysis = analyzeFunction
        self.buildingType = buildingType
        # FIXME: this is a temporary solution for the building info
        self.buildingInfo = GLOBAL_BUILDING_INFO.get_buildings_by_key(buildingType)[0]

    def run(self):
        self.analysisAndBuild()

    def analysisAndBuild(self):
        """Request to build a building on the blueprint at bound"""
        length, _, width = self.buildingInfo.dimension
        possibleLocation = self.core.getEmptyArea(
            length, width)
        if len(possibleLocation) == 0:
            return
        bestLocation = possibleLocation[0]
        bestLocationValue = 0
        for location in possibleLocation:
            value = self.analysis(self.core, location)
            if value > bestLocationValue:
                bestLocationValue = value
                bestLocation = location
        building = Building(self.buildingInfo, bestLocation.begin)
        print(
            f"building position: {building.position}, building level: {building.level}")
        # do something about the building class (add necessary data to it)
        self.core.addBuilding(building)
