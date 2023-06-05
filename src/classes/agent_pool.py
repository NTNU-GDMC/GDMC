from .agent import RunableAgent
from .agent_generator import BASIC_BUILDINGS, SPECIAL_BUILDINGS, newBuildAgent, newRoadAgent
from ..classes.core import Core


class AgentPool(object):
    core: Core
    _basic: dict[str, list[RunableAgent]]
    _special: dict[str, list[RunableAgent]]
    _road: list[RunableAgent]
    numBasic: int
    numSpecial: int

    def __init__(self, core: Core, numBasic: int, numSpecial: int) -> None:
        self.core = core
        self._basic = {}
        self._special = {}
        self._road = []
        self.numBasic = numBasic
        self.numSpecial = numSpecial

        for name in BASIC_BUILDINGS:
            self.addBasic(name, numBasic)

    @property
    def agents(self):
        for agents in self._basic.values():
            yield from agents
        for agents in self._special.values():
            yield from agents
        yield from self._road

    def unlockSpecial(self, name: str):
        if name in self._special:
            return

        self.addSpecial(name, self.numSpecial)

    def addBasic(self, name: str, num: int):
        if name not in BASIC_BUILDINGS:
            raise KeyError(f"{name} is not a basic building")

        for _ in range(num):
            try:
                self._basic.setdefault(name, []).append(
                    newBuildAgent(self.core, name))
            except KeyError:
                break

    def addSpecial(self, name: str, num: int):
        if name not in SPECIAL_BUILDINGS:
            raise KeyError(f"{name} is not a special building")

        for _ in range(num):
            try:
                self._special.setdefault(name, []).append(
                    newBuildAgent(self.core, name))
            except KeyError:
                break

    def addRoad(self, num: int):
        for _ in range(num):
            try:
                self._road.append(newRoadAgent(self.core))
            except KeyError:
                break
