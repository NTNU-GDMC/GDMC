from abc import ABC, abstractmethod
from .core import Core


class Agent(ABC):
    def __init__(self, core: Core) -> None:
        self.core = core


class RunableAgent(Agent):
    def __init__(self, core: Core, cooldown: int) -> None:
        super().__init__(core)
        self.cooldown = cooldown

    @abstractmethod
    def run(self) -> bool:
        pass

def withCooldown(func):
    """Decorator for RunableAgent.run() to add cooldown"""
    remainCD = 0
    def wrapper(self: RunableAgent):
        nonlocal remainCD
        if remainCD > 0:
            remainCD -= 1
            return False
        else:
            remainCD = self.cooldown
            return func(self)
    return wrapper