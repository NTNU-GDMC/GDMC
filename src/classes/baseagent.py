from abc import ABC, abstractmethod
from .core import Core


class Agent(ABC):
    def __init__(self, core: Core) -> None:
        self.core = core


class RunableAgent(Agent):
    @abstractmethod
    def run(self):
        pass
