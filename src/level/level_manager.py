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
levelUnlockAgentData: list[str] = []
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

def initUnlockAgent():
    with open("src/level/agent_limit.json", "r") as f:
        data = json.load(f)
        for i in range(maxLevel):
            levelUnlockAgentData.append(data["unlock_agent"][i])

@dataclass
class LevelManager:
    def __init__(self):
        initLimitResource()
        initLimitBuilding()
        initUnlockAgent()

    def getMostLackResource(self, existResource: Resource, limitResource: Resource) -> str:
        """ return one lack resource name(str) which is the most shortage"""
        lack: list[tuple[int, str]] =[]
        lack.append((limitResource.human - existResource.human, str("human")))
        lack.append((limitResource.wood - existResource.wood, str("wood")))
        lack.append((limitResource.stone - existResource.stone, str("stone")))
        lack.append((limitResource.ironOre - existResource.ironOre, str("iron_ore")))
        lack.append((limitResource.iron - existResource.iron, str("iron")))
        lack.append((limitResource.food - existResource.food, str("food")))
        maxlack:tuple[int, str] = max(lack)
        if maxlack[0] <= 0:
            return str("None")
        return maxlack[1]
    
    def isLackBuilding(self, existBuilding: int, limitBuilding: int) -> bool:
        """ return true if building is lack, else false """
        if existBuilding < limitBuilding:
            return True
        return False
    
    def canLevelUp(self, level:int, resource:Resource, numberOfBuilding:int) -> bool: 
        """ 
            if level up successfully, it means that:
                1. level is not maxLevel
                2. all resources are enough
                3. number of building is enough
        """
        if level ==  maxLevel:
            return False
        elif self.getMostLackResource(resource, levelResourceData[level]) != "None":
            return False
        elif self.isLackBuilding(numberOfBuilding, levelBuildingData[level]):
            return False
        return True
    def resourceNeededToLevelUp(self, currentLevel: int, resource: Resource) -> Resource:
        targetResource = levelResourceData[currentLevel]
        return Resource(
            human=max(0,targetResource.human - resource.human),
            wood=max(0,targetResource.wood - resource.wood),
            stone=max(0, targetResource.stone - resource.stone),
            ironOre=max(0, targetResource.ironOre - resource.ironOre),
            iron=max(0, targetResource.iron - resource.iron),
            foof=max(0, targetResource.food - resource.food),
        )
    def getLimitResource(self, level: int) -> Resource:
        return levelResourceData[level-1]
    def getLimitBuilding(self, level: int) -> int:
        return levelBuildingData[level-1]
    def getUnlockAgent(self, level: int) -> str:
        return levelUnlockAgentData[level-1]
