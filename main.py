"""
Use islevelup = levelManager.isLevelUp(core.level, core.resources, len(core.blueprintData))
    to ask levelManager can level up or not
    if islevelup == True, it means that:
        1. level is not reach the maxlevel
        2. all resources items reach the goal in this level
        3. number of building reach the goal in this level

Call core to level up:
    core.levelUp(levelManager.getLimitResource(core.level), levelManager.getLimitBuilding(core.level))
    use the code above can level up and update resourceLimit and buildingLimit
    
Use levelManager.getMostLackResource(...), (return value type is str)
    to get the resource name(str) that is MOST SHORTAGE
    this function CAN/MAYBE used to decide which resource should be gathered by agents

Use levelManager.isLackBuilding(...), (return value type is bool)
    to check if building is lack, namely, existBuilding < limitBuilding
    this function CAN/MAYBE used to decide if agent should build building in this level or not

Use core.conformToResourceLimit
    to make the resource conform to the resource limit
    namely, if current resource is more than resource limit, then set current resource to resource limit
"""

# ! /usr/bin/python3
from nbt import nbt
from src.classes.core import Core
from src.classes.agent import RunableAgent
from src.classes.agent_generator import RUNABLE_AGENT_TABLE
from src.visual.blueprint import plotBlueprint


import random
# TODO: logic per round

if __name__ == '__main__':
    COOLDOWN = 5
    ROUND = 50
    core = Core()

    agents: list[RunableAgent] = []
    generators = list(RUNABLE_AGENT_TABLE.values())
    for _ in range(7):
        generator = random.choice(generators)
        agent = generator(core)
        agents.append(agent)

    for agent in agents:
        print(agent)

    # iterate rounds
    for i in range(ROUND):
        # TODO: increase game resources
        for agent in random.sample(agents, len(agents)):
            # run agent
            success = agent.run()

            if not success:
                # gather resource if the agent cannot do their job
                pass
        # TODO: update state if needed

    core.startBuildingInMinecraft()
    core._editor.flushBuffer()

    plotBlueprint(core)
