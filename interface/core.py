from gdpc import Editor
from gdpc.vector_tools import Rect, Box
from typing import Literal
import numpy as np

from heightinfo import HeightInfo
from resource.AnalyzeAreaBiomeList import getAllBiomeList

DEFAULT_BUILD_AREA = Box((0, 0, 0), (255, 255, 255))

class Core():
    def __init__(self, buildArea=DEFAULT_BUILD_AREA) -> None:
        """
        the core will connect with the game
        """
        # initalize editor
        editor = Editor(buffering=True, caching=True)
        editor.setBuildArea(buildArea)
        # get world slice and height maps
        worldSlice = editor.loadWorldSlice(buildArea.toRect(), cache=True)
        heights = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

        # get top left and bottom right coordnidate
        x1, _, x2 = buildArea.offset
        z1, _, z2 = buildArea.offset + buildArea.size
        x, _, z = buildArea.size

        # To be discussed: Do we keep the class or save it into a 2d array
        gameData = {}
        gameData["biomes"] = getAllBiomeList(worldSlice, buildArea)
        self.editor = editor
        self.gameData = gameData
        self.heightInfo = HeightInfo((x1, z1, x2, z2), heights) # contains: height, sd, var, mean
        self.resources = {} 
        self.blueprint = np.ndarray((x,z)) 

    def getResource(self, type: str): # Do we specify the boundary here?
        """Get the amount of a certain resource. If the resource does not exist, raise Exception"""
        if type in self.resources:
            return self.resources[type]
        raise Exception(f"The type: {type}, does not exist in the core.")

    def addBuilding(self, pos, building, resourcesNeed) -> bool:
        """Append a building on to the blueprint. Return False if it fails to add the building onto the blueprint"""
        
        return True

    def getMap(self, type: str, bound: Rect = DEFAULT_BUILD_AREA.toRect()):
        if type in self.gameMap:
            return self.gameMap[type] # use the bound to get the map, need to check with lovesnow
        raise Exception(f"The requested map: {type}, does not exist in the core.")

    def getHeight(self, heightType: Literal["var" , "mean" , "sum" , "squareSum"], bound: Rect):
        x1, x2 = bound.offset
        z1, z2 = bound.offset + bound.size
        area = (x1, z1, x2, z2)
        if heightType == "var":
            return self.heightInfo.varArea(area)
        if heightType == "mean":
            return self.heightInfo.meanArea(area)
        if heightType == "sum":
            return self.heightInfo.sumArea(area)
        if heightType == "squareSum":
            return self.heightInfo.squareSumArea(area)
        raise Exception("This type does not exist on heightType")

    def startBuildingInMinecraft(self):
        """Send the blueprint to Minecraft"""
        pass

