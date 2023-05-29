from typing import Callable
from ..classes.core import Core
from ..classes.agent import RunableAgent
from ..classes.agent import BuildAgent
from ..analyze_util.basic import isFlat, hasEnoughWood, closeEnoughToRoad, isLiquid, isDesert


# basic buildings

CHALET = "chalet"
DESERT_BUILDING = "desert_building"

# Special buildings

SAWMILL = "sawmill"
FARM = "farm"
QUARRY = "quarry"
FORGE = "forge"
CHURCH = "church"

def newChaleteAgent(core: Core):
    # Obviously fun(X
    def analFun(c, a):
        if isLiquid(c, a) or isDesert(c, a):
            return 0
        return isFlat(c, a) 
    return BuildAgent(core, analFun, CHALET)


def newDesertBuildingAgent(core: Core):
    def analFun(c, a):
        if isLiquid(c, a) or not isDesert(c, a):
            return 0
        return isFlat(c, a)
    return BuildAgent(core, analFun, DESERT_BUILDING)


def newSawmillAgent(core: Core):
    if isLiquid(c, a):
            return 0
    def analyzeFunction(c, a): return isFlat(c, a) + hasEnoughWood(c, a) * 5
    return BuildAgent(core, analyzeFunction, HUGE_SAWMILL)


def placeholder(core: Core):
    def analyzeFunction(c, a): return isFlat(c, a) + hasEnoughWood(c, a) * 5
    return BuildAgent(core, analyzeFunction, HUGE_SAWMILL)


RunableAgentGenerator = Callable[[Core], RunableAgent]

RUNABLE_AGENT_TABLE: dict[str, RunableAgentGenerator] = {
    CHALET: newChaleteAgent,
    DESERT_BUILDING: newDesertBuildingAgent,
    SAWMILL: newSawmillAgent
}

# TODO: add real agent after the building is completed
UNLOCKABLE_AGENT_TABLE: dict[str, RunableAgentGenerator] = {
    "sawmill": placeholder,
    "farm": placeholder,
    "quarry": placeholder,
    "forge": placeholder,
    "church": placeholder,
}
