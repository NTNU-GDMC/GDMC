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

    unlockAgents: list[str]
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
            unlockAgents: list[str] = limit["unlock_agents"]
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
