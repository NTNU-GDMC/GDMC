import json
from pathlib import Path
from dataclasses import dataclass
from ..config.config import config
from ..resource.terrain_analyzer import Resource


@dataclass
class LevelLimit:
    """Limit of level"""

    maxLevel: int

    resources: list[Resource]
    """Resource limit of level"""

    buildings: list[list[int]]
    """Building limit of level"""

    unlockAgents: list[list[str]]
    """Unlock agents of level"""

    buildingRequirements: list[int]
    """Building requirements of level up"""

    @staticmethod
    def load(path: Path = config.levelLimitPath) -> "LevelLimit":
        """Load limit from a json file"""

        with path.open("r") as f:
            limit: dict = json.load(f)
            maxLevel: int = limit["maxLevel"]
            resourcesLimit: dict = limit["resources"]
            buildings: list[list[int]] = limit["buildings"]
            unlockAgents: list[list[str]] = limit["unlock_agents"]
            buildingRequirements: list[int] = limit["building_requirements"]

            resources = list[Resource]()
            for (human, wood, stone, food, ironOre, iron) in zip(
                resourcesLimit["human"],
                resourcesLimit["wood"],
                resourcesLimit["stone"],
                resourcesLimit["food"],
                resourcesLimit["ironOre"],
                resourcesLimit["iron"]
            ):
                resources.append(
                    Resource(human, wood, stone, food, ironOre, iron))

            return LevelLimit(
                maxLevel, resources, buildings, unlockAgents, buildingRequirements)


levelLimit: LevelLimit = LevelLimit.load()


def getResourceLimit(coreLevel: int) -> Resource:
    """Return resource limit of level"""
    return levelLimit.resources[coreLevel-1]


def getBuildingLimit(coreLevel: int, buildingLevel: int) -> int:
    """Return building limit of level"""
    return levelLimit.buildings[buildingLevel-1][coreLevel-1]


def getUnlockAgents(coreLevel: int) -> list[str]:
    """Return unlock agents of level"""
    return levelLimit.unlockAgents[coreLevel-1]


def getBuildingRequirements(coreLevel: int) -> int:
    """Return building requirements of level up"""
    return levelLimit.buildingRequirements[coreLevel-1]
