# ! /usr/bin/python3
from nbt import nbt
from src.classes.core import Core
from src.classes.agent import BuildAgent
from src.building_util.building_info import CHALET, DESERT_BUILDING
from src.visual.blueprint import plotBlueprint
from src.analyze_util.basic import isFlat
from src.building_util.nbt_builder import getNBTAbsPath, buildFromStructureNBT
from gdpc.vector_tools import addY, Rect

import random
# TODO: logic per round
if __name__ == '__main__':
    core = Core()
    agents = [
        # TODO: analyzeFunction: 決定一塊空地的價值(偏好程度)
        # building type 決定 Agent 要 build 什麼類型的建築
        BuildAgent(core, isFlat, CHALET),
        BuildAgent(core, isFlat, DESERT_BUILDING),
    ]

    for agent in agents:
        print(agent.buildingType)
        print(agent.buildingInfo.getCurrentBuildingLengthAndWidth())
        print(agent.buildingInfo.getCurrentBuildingType())
        print(agent.buildingInfo.getCurrentBuildingMaterial())
        print(agent.buildingInfo.getCurrentRequiredResource().stone)
        print(agent.buildingInfo.getCurrentRequiredResource().wood)

    # iterate 10 rounds
    round = 10

    for i in range(round):
        # randomize agent order
        for agent in random.sample(agents, len(agents)):
            # run agent
            agent.run()

    plotBlueprint(core)
