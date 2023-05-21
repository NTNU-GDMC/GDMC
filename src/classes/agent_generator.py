from typing import Callable
from src.classes.core import Core
from src.classes.agent import RunableAgent
from src.classes.agent import BuildAgent
from src.building_util.building_info import CHALET, DESERT_BUILDING, HUGE_SAWMILL
from src.analyze_util.basic import isFlat, hasEnoughWood, closeEnoughToRoad


def newChaleteAgent(core: Core):
    return BuildAgent(core, isFlat, CHALET, 5)


def newDesertBuildingAgent(core: Core):
    return BuildAgent(core, isFlat, DESERT_BUILDING, 5)


def newSawmillAgent(core: Core):
    def analyzeFunction(c, a): return isFlat(c, a) + hasEnoughWood(c, a) * 5
    return BuildAgent(core, analyzeFunction, HUGE_SAWMILL, 5)


RunableAgentGenerator = Callable[[Core], RunableAgent]

RUNABLE_AGENT_TABLE: dict[str, RunableAgentGenerator] = {
    CHALET: newChaleteAgent,
    DESERT_BUILDING: newDesertBuildingAgent,
    HUGE_SAWMILL: newSawmillAgent
}
