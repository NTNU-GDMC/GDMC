from .agent import RunableAgent
from .agent_generator import BASIC_BUILDINGS, SPECIAL_BUILDINGS, newAgent
from ..classes.core import Core


class AgentPool(object):
    core: Core
    _basic: dict[str, list[RunableAgent]]
    _special: dict[str, list[RunableAgent]]
    numBasic: int
    numSpecial: int

    def __init__(self, core: Core, numBasic: int, numSpecial: int) -> None:
        self.core = core
        self._basic = {}
        self._special = {}
        self.numBasic = numBasic
        self.numSpecial = numSpecial

        for name in BASIC_BUILDINGS:
            for _ in range(numBasic):
                self._basic.setdefault(name, []).append(newAgent(core, name))

    @property
    def agents(self):
        for agents in self._basic.values():
            yield from agents
        for agents in self._special.values():
            yield from agents

    def unlockSpecial(self, name: str):
        if name not in SPECIAL_BUILDINGS:
            raise KeyError(f"{name} is not a special building")

        if name in self._special:
            return

        self._special[name] = []
        for _ in range(self.numSpecial):
            try:
                self._special[name].append(newAgent(self.core, name))
            except KeyError:
                break
