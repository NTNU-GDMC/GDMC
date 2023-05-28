from typing import Callable
from ..classes.core import Core
from ..classes.agent import RunableAgent
from ..classes.agent import BuildAgent
from ..building.building_info import CHALET, DESERT_BUILDING, HUGE_SAWMILL
from ..analyze_util.basic import isFlat, hasEnoughWood, closeEnoughToRoad


def newChaleteAgent(core: Core):
    # Obviously fun(X
    def analFun(c, a):
        return isFlat(c, a) and isLiquid(c, a)
    return BuildAgent(core, analFun, CHALET)


def newDesertBuildingAgent(core: Core):
    def analFun(c, a):
        return isFlat(c, a) and isLiquid(c, a)
    return BuildAgent(core, analFun, DESERT_BUILDING)


def newSawmillAgent(core: Core):
    def analyzeFunction(c, a): return isLiquid(
        c, a) + isFlat(c, a) + hasEnoughWood(c, a) * 5
    return BuildAgent(core, analyzeFunction, HUGE_SAWMILL)


def placeholder(core: Core):
    def analyzeFunction(c, a): return isFlat(c, a) + hasEnoughWood(c, a) * 5
    return BuildAgent(core, analyzeFunction, HUGE_SAWMILL)


RunableAgentGenerator = Callable[[Core], RunableAgent]

RUNABLE_AGENT_TABLE: dict[str, RunableAgentGenerator] = {
    CHALET: newChaleteAgent,
    DESERT_BUILDING: newDesertBuildingAgent,
    HUGE_SAWMILL: newSawmillAgent
}

# TODO: add real agent after the building is completed
UNLOCKABLE_AGENT_TABLE: dict[str, RunableAgentGenerator] = {
    "sawmill": placeholder,
    "farm": placeholder,
    "quarry": placeholder,
    "forge": placeholder,
    "church": placeholder,
}
