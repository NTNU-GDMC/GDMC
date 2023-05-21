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
