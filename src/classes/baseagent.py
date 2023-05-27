from abc import ABC, abstractmethod
from .core import Core


class Agent(ABC):
    def __init__(self, core: Core) -> None:
        self.core = core


class RunableAgent(Agent):
    def __init__(self, core: Core, cooldown: int) -> None:
        super().__init__(core)
        self.cooldown = cooldown
        self._remainCD = 0

    @property
    def remainCD(self):
        return self._remainCD

    @remainCD.setter
    def remainCD(self, value: int):
        if value < 0:
            raise ValueError("RemainCD cannot be negative")
        self._remainCD = value

    @abstractmethod
    def run(self) -> bool:
        pass

    @abstractmethod
    def rest(self) -> bool:
        pass


def withCooldown(func):
    """Decorator for RunableAgent.run() to add cooldown"""

    def wrapper(self: RunableAgent):
        if self.remainCD > 0:
            self.remainCD -= 1
            return False
        else:
            self.remainCD = self.cooldown
            return func(self)
    return wrapper
