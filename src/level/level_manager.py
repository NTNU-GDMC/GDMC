"""
only check human, wood, stone, ironOre, iron, food
not check grass limit

function levelUp:
    if level is up to maxLevel, it will return false
    else true
"""

from dataclasses import dataclass
from .limit import levelLimit
from ..resource.terrain_analyzer import Resource


def getResourceLimit(level: int) -> Resource:
    """ return resource limit of level """
    return levelLimit.resources[level-1]


def getBuildingLimit(coreLevel: int, buildingLevel: int) -> int:
    """ return building limit of level """
    return levelLimit.buildings[buildingLevel-1][coreLevel-1]


@dataclass
class LevelManager:
    def __init__(self):
        self.maxLevel: int = levelLimit.maxLevel
        self.levelResourceData: list[Resource] = levelLimit.resources
        self.levelBuildingData: list[int] = levelLimit.buildingRequirements

    def isLackBuilding(self, existBuilding: int, limitBuilding: int) -> bool:
        """ return true if building is lack, else false """
        if existBuilding < limitBuilding:
            return True
        return False

    def canLevelUp(self, level: int, resource: Resource, numberOfBuilding: int) -> bool:
        """
        if level up successfully, it means that:
            1. level is not maxLevel
            2. all resources are enough
            3. number of building is enough
        """
        if level == self.maxLevel:
            return False
        elif resource < self.levelResourceData[level-1]:
            return False
        elif self.isLackBuilding(numberOfBuilding, self.levelBuildingData[level-1]):
            return False
        return True

    def resourceNeededToLevelUp(self, currentLevel: int, resource: Resource) -> Resource:
        targetResource = self.levelResourceData[currentLevel]
        return Resource(
            human=max(0, targetResource.human - resource.human),
            wood=max(0, targetResource.wood - resource.wood),
            stone=max(0, targetResource.stone - resource.stone),
            ironOre=max(0, targetResource.ironOre - resource.ironOre),
            iron=max(0, targetResource.iron - resource.iron),
            food=max(0, targetResource.food - resource.food),
        )
