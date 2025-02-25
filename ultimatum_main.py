from dotenv import load_dotenv
from negotiationarena.agents.chatgpt import ChatGPTAgent
from negotiationarena.game_objects.resource import Resources
from negotiationarena.game_objects.goal import UltimatumGoal
from games.ultimatum.game import MultiTurnUltimatumGame
from negotiationarena.constants import *
import traceback

import matplotlib.pyplot as plt
import os

load_dotenv(".env")

if __name__ == "__main__":
    cnt = 0
    agent1_utility = []
    agent2_utility = []
    while cnt < 100:
        try:
            a1 = ChatGPTAgent(
                agent_name=AGENT_ONE,
                model="gpt-4-1106-preview",
            )
            a2 = ChatGPTAgent(
                agent_name=AGENT_TWO,
                model="gpt-4-1106-preview",
            )

            c = MultiTurnUltimatumGame(
                players=[a1, a2],
                iterations=6,
                resources_support_set=Resources({"Dollars": 0}),
                player_goals=[
                    UltimatumGoal(),
                    UltimatumGoal(),
                ],
                player_initial_resources=[
                    Resources({"Dollars": 100}),
                    Resources({"Dollars": 0}),
                ],
                player_social_behaviour=["You are an individual, and you are negotiating with a corporation.",
                                        "You are a corporation, and you are negotiating with an individual"],
                player_roles=[
                    f"You are {AGENT_ONE}.",
                    f"You are {AGENT_TWO}.",
                ],
                log_dir="example_logs/ultimatum_multi_period",
            )

            c.run()
            agent1_utility.append(c.game_state[-1]["summary"]["player_outcome"][0].resource_dict['Dollars'])
            agent2_utility.append(c.game_state[-1]["summary"]["player_outcome"][1].resource_dict['Dollars'])
            cnt += 1
        except Exception as e:
            exception_type = type(e).__name__
            exception_message = str(e)
            stack_trace = traceback.format_exc()

            # Print or use the information as needed
            print(f"Exception Type: {exception_type}")
            print(f"Exception Message: {exception_message}")
            print(f"Stack Trace:\n{stack_trace}")

    print("agent1 utility: ", sum(agent1_utility) / 100)
    print("agent2 utility: ", sum(agent2_utility) / 100)
    plt.hist(agent1_utility, bins=1, edgecolor='black')
    plt.title('a1_utility')
    plt.xlabel('Value')
    plt.ylabel('Frequency')

    plt.show()