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

levelData: list[Resource] = []
maxLevel:int = 0

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
            levelData.append(Resource(human, wood, stone, iron_ore, iron, food))

def getLimitResource(level: int) -> Resource:
    return levelData[level]

@dataclass
class LevelManager:
    resource: Resource
    level: int = 1
    def __init__(self):
        initLimitResource()
        self.resource = getLimitResource(self.level - 1)
    def __str__(self):
        return "maxLevel:" + str(maxLevel) + "Level:" + str(self.level) + " " + str(self.resource)
    def getLimitResource(self) -> Resource: 
        """ return the limit resource of current level """
        return self.resource
    def levelUp(self) -> bool: 
        """ return true if level up successfully, else false """
        if self.level ==  maxLevel:
            return False
        self.level += 1
        self.resource = getLimitResource(self.level - 1)
        return True
    def getLevel(self) -> int:
        return self.level

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