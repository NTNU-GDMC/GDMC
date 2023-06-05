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
    core.levelUp(levelManager.getLimitResource(core.level+1), levelManager.getLimitBuilding(core.level+1))
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
from time import time
from random import sample
from src.classes.core import Core
from src.classes.agent import RoadAgent
from src.classes.agent_pool import AgentPool
from src.level.level_manager import LevelManager
from src.level.limit import getUnlockAgents
from src.visual.blueprint import plotBlueprint
from src.config.config import config

if __name__ == '__main__':
    startTime = time()

    ROUND = config.gameRound
    NUM_BASIC_AGENTS = config.numBasicAgents
    NUM_SPECIAL_AGENTS = config.numSpecialAgents

    print("Initing core...")
    core = Core()
    print("Done initing core")

    levelManager = LevelManager()
    agentPool = AgentPool(core, NUM_BASIC_AGENTS, NUM_SPECIAL_AGENTS)
    RoadAgent(core)

    for agent in agentPool.agents:
        print(agent)

    # iterate rounds
    for i in range(ROUND):
        numbersOfBuildings = [
            core.numberOfBuildings(level) for level in (1, 2, 3)
        ]
        limitsOfBuildings = [
            core.getBuildingLimit(level) for level in (1, 2, 3)
        ]

        print(f"Round: {i}")
        print(f"Level: {core.level}")
        print(f"Buildings: {numbersOfBuildings}")
        print(f"Max Buildings:  {limitsOfBuildings}")
        print(f"Resources: {core.resources}")

        core.updateResource()

        unlockedAgents = getUnlockAgents(core.level)
        print("Unlocked agents: ", unlockedAgents)

        for unlockedAgent in unlockedAgents:
            agentPool.unlockSpecial(unlockedAgent)

        print("Start running agents")

        restingAgents = 0

        agents = list(agentPool.agents)
        for agent in sample(agents, len(agents)):
            # run agent
            success = agent.run()

            if not success:
                # gather resource if the agent cannot do their job
                restingAgents += 1
                agent.rest()

        core.increaseGrass()

        print(f"Resting agents: {restingAgents}")

        if levelManager.canLevelUp(core.level, core.resources,
                                   core.numberOfBuildings()):
            core.levelUp()

        # clamp resource to limit
        core.conformToResourceLimit()

        print("Round Done")
        print("=====")

    print(f"Time: {time() - startTime}")

    print("Start building in minecraft")

    core.startBuildingInMinecraft()

    print("Done building in minecraft")

    print(f"Time: {time() - startTime}")

    plotBlueprint(core)
