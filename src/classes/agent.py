from typing import Callable
from gdpc.vector_tools import Rect, ivec2
from .core import Core
from .baseagent import RunableAgent, withCooldown
from ..building.building import Building
from ..building.master_building_info import GLOBAL_BUILDING_INFO
from random import sample

class BuildAgent(RunableAgent):
    def __init__(self, core: Core, analyzeFunction: Callable[[Core, Rect], float], buildingType: str, cooldown: int, special: bool = False) -> None:
        """Assume one agent one build one building for now"""
        super().__init__(core, cooldown)
        # the larger value analyzeFunction returns, the better
        self.analysis = analyzeFunction
        self.buildingType = buildingType
        # FIXME: this is a temporary solution for the building info
        self.buildingInfo = GLOBAL_BUILDING_INFO[buildingType][0]
        self.speical = special

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

        return True

    def gatherResource(self, resourceType: str):
        self.core.resource[resourceType] += self.core.resourceLimit[resourceType] * 0.05 # gain 5% of the limit
