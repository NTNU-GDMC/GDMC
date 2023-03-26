from gdpc.vector_tools import Rect
from .core import Core
from glm import ivec3


class Agent():
    def __init__(self, pos: ivec3) -> None:
        self.position = pos # the position of the agent

    def analysis(self, bound: ivec3) -> bool:
        """Analysis i"""
        return False
    
    def build(self, bound: Rect, core: Core, build):
        """Request to build a building on the blueprint at bound"""
        pass

    def moveTo(self, pos: ivec3):
        """Move the agent to pos"""
        self.position = pos


class Specialist(Agent):
    def __init__(self, pos: ivec3, buildings: list,analysisFunc) -> None:
        """Init the position and types of building this agent will build"""
        super().__init__(pos)
        self.analysis = analysisFunc

