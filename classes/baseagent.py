from abc import abstractmethod
from .core import Core


class Agent(object):
    def __init__(self, core: Core) -> None:
        self.core = core


class RunableAgent(Agent):
    def __init__(self, core: Core) -> None:
        super().__init__(core)

    @abstractmethod
    def run(self):
        pass


class Event():
    pass


class ObserverAgent(Agent):
    def __init__(self, core: Core) -> None:
        super().__init__(core)

    @abstractmethod
    def update(self, event: Event):
        pass
