import sys

sys.path.append(".")
from dotenv import load_dotenv
import inspect
from negotiationarena.agents import *
from negotiationarena.agents.agent_behaviours import (
    SelfCheckingAgent,
    ReasoningAgent,
)
from negotiationarena.game_objects.resource import Resources
from negotiationarena.game_objects.goal import ResourceGoal
from games.trading_game.game import TradingGame
from games.trading_game.interface import TradingGameDefaultParser
from negotiationarena.constants import *
import traceback

load_dotenv(".env")


if __name__ == "__main__":
    cnt = 0
    agent1_utility = []
    agent2_utility = []
    while cnt < 100:
        try:
            a1 = ChatGPTAgent(
                model="gpt-4-turbo-1106",
                agent_name=AGENT_TWO,
            )
            a2 = ChatGPTAgent(
                model="gpt-4-turbo-1106",
                agent_name=AGENT_TWO,
            )

            c = TradingGame(
                players=[a1, a2],
                iterations=6,
                resources_support_set=Resources({"X": 0, "Y": 0}),
                player_goals=[
                    ResourceGoal({"X": 15, "Y": 15}),
                    ResourceGoal({"X": 15, "Y": 15}),
                ],
                player_initial_resources=[
                    Resources({"X": 25, "Y": 5}),
                    Resources({"X": 5, "Y": 25}),
                ],
                player_social_behaviour=["You are a corporation, and you are negotiating with an individual", 
                                        "You are an individual, and you are negotiating with a corporation."],
                player_roles=[
                    f"You are {AGENT_ONE}, start by making a proposal.",
                    f"You are {AGENT_TWO}, start by responding to a trade.",
                ],
                log_dir="example_logs/trading/",
            )

            c.run()
            agent1_utility.append(c.game_state[-1]["summary"]["player_outcome"][0])
            agent2_utility.append(c.game_state[-1]["summary"]["player_outcome"][1])
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
    plt.hist(data, bins=1, edgecolor='black')
    plt.title('Histogram of negotiation outcome.')
    plt.xlabel('Value')
    plt.ylabel('Frequency')

    output_dir = 'figures/trading'
    os.makedirs(output_dir, exist_ok=True) 
    output_file = os.path.join(output_dir, 'agent1_corporation_agent2_individual.png')
    plt.savefig(output_file)