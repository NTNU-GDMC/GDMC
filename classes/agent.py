from gdpc.vector_tools import Rect
from .core import Core
from ..building import Building


class Agent():
    def __init__(self, analyzeFunction: callable[[Core, Rect], int], building: Building) -> None:
        """Assume one agent one build one building for now"""
        self.building = building
        self.analysis = analyzeFunction
    
    def analysisAndBuild(self, core: Core, building: Building):
        """Request to build a building on the blueprint at bound"""
        possibleLocation = core.getEmptyArea(building.length, building.width)
        if len(possibleLocation) == 0:
            return
        bestLocation = possibleLocation[0]
        bestLocationValue = 0
        for location in possibleLocation:
            value = self.analysis(core, location)
            if value > bestLocationValue:
                bestLocationValue = value
                bestLocation = location

        # do something about the building class (add nessarry data to it)
        core.addBuilding(building)
        pass

