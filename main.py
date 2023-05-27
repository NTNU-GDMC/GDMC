"""
In main.py, use levelManager = LevelManager() to create a LevelManager object
    LevelManager path is src/level/level_manager.py

Use islevelup = levelManager.isLevelUp(core.level, core.resources, len(core.blueprintData))
    to ask levelManager whether core can level up or not
    if islevelup == True, it means that:
        1. level is not reach the maxlevel
        2. all resources items reach the goal in this level
        3. number of building reach the goal in this level

Call core to level up:
    core.levelUp(levelManager.getLimitResource(core.level), levelManager.getLimitBuilding(core.level))
    use the code above can make core level to level up and update resourceLimit and buildingLimit simultaneously
    
Use levelManager.getMostLackResource(...), (return value type is str)
    to get the resource name(str) that is MOST SHORTAGE
    this function CAN/MAYBE used to decide which resource should be gathered by agents who have nothing to do

Use levelManager.isLackBuilding(...), (return value type is bool)
    to check if building is lack, namely, existBuilding < limitBuilding(in this level)
    this function CAN/MAYBE used to decide if agent should build building in this level or not

Use core.conformToResourceLimit
    to make the resource conform to the resource limit
    namely, if current resource is more than resource limit, then set current resource to resource limit

Use levelManager.getUnlockAgent(...), (return value type is str) (please see the name(str) in agent_limit.json)
    to get the SPECIAL agent name(str) that can be unlocked after this level
    if the return value is "none", it means that there is NO SPECIAL agent can be generate after this level
    NOTICE 1: this agent can only generate ONCE, for example, you can ONLY generate one sawmill agent in whole game. 
              (Because it is special agent, not wood/sand house agent)
    NOTICE 2: if you want to add new action like "some SPECIFIC building can only be upgraded after ? level", 
              you can add new name(str) in agent_limit.json, 
              and use this function to get the name(str) while you reach the level,
              then write YOUR OWN LOGIC to distinguish the name(str)
"""

# ! /usr/bin/python3
from nbt import nbt
from src.classes.core import Core
from src.classes.agent import RunableAgent
from src.classes.agent_generator import RUNABLE_AGENT_TABLE
from src.level.level_manager import LevelManager
from src.visual.blueprint import plotBlueprint


import random
# TODO: logic per round

if __name__ == '__main__':
    COOLDOWN = 5
    ROUND = 500
    core = Core()
    levelManager = LevelManager()
    agentPool: list[RunableAgent] = []
    generators = list(RUNABLE_AGENT_TABLE.values())
    for _ in range(7):
        generator = random.choice(generators)
        agent = generator(core)
        agentPool.append(agent)

    for agent in agentPool:
        print(agent)

    # iterate rounds
    for i in range(ROUND):
        core.updateResource()

        for agent in random.sample(agentPool, len(agentPool)):
            # run agent
            success = agent.run()

            if not success:
                # gather resource if the agent cannot do their job
                resourceType = levelManager.getMostLackResource(core.resource, core.resourceLimit)
                if resourceType != "none":
                    agent.gatherResource(resourceType)

        if levelManager.canLevelUp(core.level, core.resource , core.numberOfBuildings):
            core.levelUp()

        # clamp resource to limit
        core.conformToResourceLimit()


    core.startBuildingInMinecraft()
    core._editor.flushBuffer()

    plotBlueprint(core)
