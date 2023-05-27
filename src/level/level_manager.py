"""
only check human, wood, stone, iron_ore, iron, food
not check grass limit

function levelUp:
    if level is up to maxLevel, it will return false
    else true
"""

import json
from dataclasses import dataclass
from pathlib import Path
from ..resource.terrain_analyzer import Resource

levelResourceData: list[Resource] = []
levelBuildingData: list[int] = []
maxLevel:int = 0

def getResourceLimit(level:int) -> Resource:
    """ return resource limit of level """
    with open("src/level/resource_limit.json", "r") as f:
        data = json.load(f)
        human = data["human"][level-1]
        wood = data["wood"][level-1]
        stone = data["stone"][level-1]
        iron_ore = data["iron_ore"][level-1]
        iron = data["iron"][level-1]
        food = data["food"][level-1]
        return Resource(human, wood, stone, food, iron_ore, iron)

def getBuildingLimit(level:int) -> int:
    """ return building limit of level """
    with open("src/level/building_limit.json", "r") as f:
        data = json.load(f)
        return data["building_limit"][level-1]

def initLimitResource():
        global maxLevel
        with open("src/level/resource_limit.json", "r") as f:
            data = json.load(f)
            maxLevel = data["maxLevel"]
            for i in range(maxLevel):
                human = data["human"][i]
                wood = data["wood"][i]
                stone = data["stone"][i]
                iron_ore = data["iron_ore"][i]
                iron = data["iron"][i]
                food = data["food"][i]
                levelResourceData.append(Resource(human, wood, stone, food, iron_ore, iron))
def initLimitBuilding():
    with open("src/level/building_limit.json", "r") as f:
        data = json.load(f)
        for i in range(maxLevel):
            levelBuildingData.append(data["building_limit"][i])

@dataclass
class LevelManager:
    def __init__(self):
        initLimitResource()
        initLimitBuilding()
    
    def isLevelUp(self, level:int) -> bool: 
        """ return true if level up successfully, else false """
        if level ==  maxLevel:
            return False
        return True
    def getLimitResource(self, level: int) -> Resource:
        return levelResourceData[level]
    def getLimitBuilding(self, level: int) -> int:
        return levelBuildingData[level]