import sys
from dotenv import load_dotenv

from negotiationarena.agents.chatgpt import ChatGPTAgent
from negotiationarena.game_objects.resource import Resources
from negotiationarena.game_objects.goal import BuyerGoal, SellerGoal
from negotiationarena.game_objects.valuation import Valuation
from negotiationarena.constants import *
import traceback
from games.buy_sell_game.game import BuySellGame

import matplotlib.pyplot as plt
import os

load_dotenv(".env")


if __name__ == "__main__":
    cnt = 0
    seller_utility = []
    buyer_utility = []
    while cnt < 100:
        try:
            a1 = ChatGPTAgent(agent_name=AGENT_ONE, model="gpt-4-1106-preview")
            a2 = ChatGPTAgent(agent_name=AGENT_TWO, model="gpt-4-1106-preview")

            c = BuySellGame(
                players=[a1, a2],
                iterations=10,
                player_goals=[
                    SellerGoal(cost_of_production=Valuation({"X": 40})),
                    BuyerGoal(willingness_to_pay=Valuation({"X": 60})),
                ],
                player_starting_resources=[
                    Resources({"X": 1}),
                    Resources({MONEY_TOKEN: 1000}),
                ],
                player_conversation_roles=[
                    f"You are {AGENT_ONE}.",
                    f"You are {AGENT_TWO}.",
                ],
                player_social_behaviour=[
                    "You are an individual, and you are negotiating with a corporation.",
                    "You are a corporation, and you are negotiating with an individual.",
                ],
                log_dir="example_logs/buysell",
            )

            c.run()
            seller_utility.append(c.game_state[-1]["summary"]["player_outcome"][0])
            buyer_utility.append(c.game_state[-1]["summary"]["player_outcome"][1])
            cnt += 1
        except Exception as e:
            exception_type = type(e).__name__
            exception_message = str(e)
            stack_trace = traceback.format_exc()

            # Print or use the information as needed
            print(f"Exception Type: {exception_type}")
            print(f"Exception Message: {exception_message}")
            print(f"Stack Trace:\n{stack_trace}")

    print("seller utility: ", sum(seller_utility) / 100)
    print("buyer utility: ", sum(buyer_utility) / 100)
    plt.hist(seller_utility, bins=1, edgecolor='black')
    plt.title('a1_utility.')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.show()