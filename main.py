# ! /usr/bin/python3
from nbt import nbt
from src.classes.core import Core
from src.classes.agent import BuildAgent
from src.building_util.building_info import CHALET, DESERT_BUILDING, HUGE_SAWMILL
from src.visual.blueprint import plotBlueprint

from src.analyze_util.basic import isFlat, hasEnoughWood, closeEnoughToRoad
from src.building_util.nbt_builder import getNBTAbsPath, buildFromStructureNBT
from gdpc.vector_tools import addY, Rect

import random
# TODO: logic per round
analyzeFunctions = [isFlat, hasEnoughWood, closeEnoughToRoad]
buildingTypes = [CHALET, DESERT_BUILDING]

if __name__ == '__main__':
    COOLDOWN = 5
    ROUND = 50
    core = Core()

    agents: list[BuildAgent]= []
    for _ in range(7):
        agents.append(BuildAgent(core, random.choice(analyzeFunctions), random.choice(buildingTypes)))
    # Agents that built , as a pair (agent, int)
    coolDownAgent: list[tuple[BuildAgent, int]] = []


    for agent in agents:
        print(agent.buildingType)
        print(agent.buildingInfo.getCurrentBuildingLengthAndWidth())
        print(agent.buildingInfo.getCurrentBuildingType())
        print(agent.buildingInfo.getCurrentBuildingMaterial())
        print(agent.buildingInfo.getCurrentRequiredResource().stone)
        print(agent.buildingInfo.getCurrentRequiredResource().wood)

    # iterate 10 rounds
    for i in range(ROUND):
        # TODO: increase game resources

        # agent run
        for agent in agents:
            # run agent
            if agent.run():
                coolDownAgent.append((agent, COOLDOWN))
                agents.remove(agent)
            else:
                # gather resource if the agent cannot do their job
                pass

        # iterate cooldown agents
        for index,(agent,remainCD) in enumerate(coolDownAgent):
            if remainCD == 0:
                agents.append(agent)
            else:
                coolDownAgent[index] = (agent, remainCD - 1)

        coolDownAgent = filter(coolDownAgent, lambda agent: agent[1] != 0)

        # TODO: update state if needed



    plotBlueprint(core)
