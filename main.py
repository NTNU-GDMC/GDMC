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

    agents: list[BuildAgent] = []
    for _ in range(7):
        agents.append(BuildAgent(core, random.choice(
            analyzeFunctions), random.choice(buildingTypes), COOLDOWN))

    for agent in agents:
        print(agent.buildingType)
        print(agent.buildingInfo.getCurrentBuildingLengthAndWidth())
        print(agent.buildingInfo.getCurrentBuildingType())
        print(agent.buildingInfo.getCurrentBuildingMaterial())
        print(agent.buildingInfo.getCurrentRequiredResource().stone)
        print(agent.buildingInfo.getCurrentRequiredResource().wood)

    # iterate rounds
    for i in range(ROUND):
        core.updateResource()

        for agent in random.sample(agents, len(agents)):
            # run agent
            success = agent.run()

            if not success:
                # gather resource if the agent cannot do their job
                core.storeResource(agent.gather())

        # TODO: update state if needed

    plotBlueprint(core)
