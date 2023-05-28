from typing import Callable
from src.classes.core import Core
from src.classes.agent import RunableAgent
from src.classes.agent import BuildAgent
from src.building.building_info import CHALET, DESERT_BUILDING, HUGE_SAWMILL
from src.analyze_util.basic import isFlat, hasEnoughWood, closeEnoughToRoad, isLiquid


def newChaleteAgent(core: Core):
    # Obviously fun(X
    def analFun(c, a):
        return isFlat(c, a) and isLiquid(c, a)
    return BuildAgent(core, analFun, CHALET, 5)


def newDesertBuildingAgent(core: Core):
    def analFun(c, a):
        return isFlat(c, a) and isLiquid(c, a)
    return BuildAgent(core, analFun, DESERT_BUILDING, 5)


def newSawmillAgent(core: Core):
    def analyzeFunction(c, a): return isLiquid(
        c, a) + isFlat(c, a) + hasEnoughWood(c, a) * 5
    return BuildAgent(core, analyzeFunction, HUGE_SAWMILL, 5)


def placeholder(core: Core):
    def analyzeFunction(c, a): return isFlat(c, a) + hasEnoughWood(c, a) * 5
    return BuildAgent(core, analyzeFunction, HUGE_SAWMILL, 5)


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
