from gdpc.vector_tools import Rect
import numpy as np

class Core():
    def __init__(self,bound: Rect, heightMap, liquidMap, roadMap, sdMap, biomeMap, resources) -> None:
        gameMap = {}
        gameMap["height"] = heightMap
        gameMap["liquid"] = liquidMap
        gameMap["road"] = roadMap
        gameMap["SD"] = sdMap
        gameMap["biome"] = biomeMap
        self.gameMap = gameMap
        self.resources =  resources
        self.blueprint = np.array(bound.size) # what should type of the blueprint be?

    def getResource(self, type: str): # Do we specify the boundary here?
        """Get the amount of a certain resource. If the resource does not exist, raise Exception"""
        if type in self.resources:
            return self.resources[type]
        raise Exception(f"The type: {type}, does not exist in the core.")

    def addBuilding(self, pos, building, resourcesNeed) -> bool:
        """Append a building on to the blueprint. Return False if it fails to add the building onto the blueprint"""
        
        return True

    def canBuild(self, bound: Rect) -> bool:
        """Check if an area can build a new building"""
        return True

    def getMap(self, type: str, bound: Rect):
        if type in self.gameMap:
            return self.gameMap[type] # use the bound to get the map, need to check with lovesnow
        raise Exception(f"The requested map: {type}, does not exist in the core.")

    def startBuildingInMinecraft(self):
        """Send the blueprint to Minecraft"""
        pass
