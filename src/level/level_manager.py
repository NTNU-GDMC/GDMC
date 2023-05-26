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

@dataclass
class LevelManager:
    levelResourceData: list[Resource] = []
    levelBuildingData: list[int] = []
    maxLevel:int = 0
    def __init__(self):
        self.initLimitResource()
        self.initLimitBuilding()
    def initLimitResource(self):
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
                self.levelResourceData.append(Resource(human, wood, stone, iron_ore, iron, food))
    def initLimitBuilding(self):
        with open("src/level/building_limit.json", "r") as f:
            data = json.load(f)
            for i in range(maxLevel):
                self.levelBuildingData.append(data["building_limit"][i])
    def islevelUp(level:int) -> bool: 
        """ return true if level up successfully, else false """
        if level ==  maxLevel:
            return False
        return True
    def getLimitResource(self, level: int) -> Resource:
        return self.levelResourceData[level]
    def getLimitBuilding(self, level: int) -> int:
        return self.levelBuildingData[level]

if __name__ == "__main__":
    levelManger = LevelManager()
    print(levelManger)
    isLevelUp:bool = True
    for i in range(100):
        print("round:", i+1)

        isLevelUp = levelManger.levelUp()
        if not isLevelUp:
            print("level max!")
            break
        print(levelManger)