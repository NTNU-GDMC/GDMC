from typing import Callable
from gdpc.vector_tools import Rect
from ..classes.core import Core
from ..classes.agent import RunableAgent
from ..classes.agent import BuildAgent
from ..analyze_util.basic import isFlat, hasEnoughWood, closeEnoughToRoad, isLiquid, isDesert


# basic buildings

CHALET = "chalet"
DESERT_BUILDING = "desert_building"

BASIC_BUILDINGS = {
    CHALET,
    DESERT_BUILDING
}

# Special buildings

SAWMILL = "sawmill"
FARM = "farm"
QUARRY = "quarry"
FORGE = "forge"
CHURCH = "church"

SPECIAL_BUILDINGS = {
    SAWMILL,
    FARM,
    QUARRY,
    FORGE,
    CHURCH
}

# Building tags

TAG_LAND = "land"
TAG_DESERT = "desert"
TAG_CITY = "city"
TAG_FOREST = "forest"

BUILDING_TAGS = {
    CHALET: [TAG_LAND],
    DESERT_BUILDING: [TAG_LAND, TAG_DESERT],
    SAWMILL: [TAG_LAND],
    FARM: [TAG_LAND],
    QUARRY: [TAG_LAND],
    FORGE: [TAG_LAND],
    CHURCH: [TAG_LAND, TAG_CITY]
}


def newAgent(core: Core, name: str):
    tags = BUILDING_TAGS[name]

    def analyzeFunction(core: Core, area: Rect):
        total = 0

        if TAG_LAND in tags and isLiquid(core, area):
            return 0
        if TAG_DESERT in tags and not isDesert(core, area):
            return 0
        if TAG_DESERT not in tags and isDesert(core, area):
            return 0

        flatness = isFlat(core, area)
        if flatness == 0:
            return 0
        else:
            total += flatness
        if TAG_FOREST:
            total += hasEnoughWood(core, area)
        return total

    return BuildAgent(core, analyzeFunction, name)


RunableAgentGenerator = Callable[[Core], RunableAgent]

RUNABLE_AGENT_TABLE: dict[str, RunableAgentGenerator] = {
    name: lambda core: newAgent(core, name) for name in BASIC_BUILDINGS | SPECIAL_BUILDINGS
}
