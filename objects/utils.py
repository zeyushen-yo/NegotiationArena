import json
import logging
from dataclasses import dataclass
from collections import defaultdict
from objects.resource import Resources
from objects.goal import Goal

from objects.trade import Trade

def text_to_dict(s):
    return {k: int(v) for k, v in (item.split(": ") for item in s.split(", "))}





class StateTracker:

    def __init__(self, iteration=None, goals=None, resources=None):
        self.iteration = iteration
        self.goals = goals
        self.resources = resources
        self.player_response = None
        self.received_trade = None
        self.received_message = None
        self.proposed_trade = None
        self.message = None
        
        
    def setattrs(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)

    def set_goals(self, goals):
        self.goals = goals

    def set_proposed_trade(self, trade):
        self.proposed_trade = trade

    def set_resources(self, resources):
        self.resources = resources

    def set_player_response(self, response):
        self.player_response = response

    def set_received_trade(self, trade):
        self.received_trade = trade
    
    def set_received_message(self, msg):
        self.received_message = msg

    def __str__(self):
        return f"StateTracker: {self.resources}, {self.proposed_trade}, {self.player_response}"

def get_index_for_tag(tag, response):
    start_index = response.find(f"<{tag}>")
    end_index = response.find(f"</{tag}>")
    return start_index, end_index, len(f"<{tag}>")

def parse_response(response):

    start_index, end_index, tag_len = get_index_for_tag("my resources", response)
    k = response[start_index + tag_len:end_index].strip()
    my_resources = Resources(text_to_dict(k))

    start_index, end_index, tag_len = get_index_for_tag("newly proposed trade", response)
    trade = response[start_index + tag_len:end_index].strip()

    if trade == "WAIT":
        proposed_trade = "WAIT"
    else:
        proposed_trade = Trade(parse_proposed_trade(trade), raw_string=trade)

    start_index, end_index, tag_len = get_index_for_tag("message", response)
    message = response[start_index + tag_len:end_index].strip()

    start_index, end_index, tag_len = get_index_for_tag("my response", response)
    player_response = response[start_index + tag_len:end_index].strip()

        
    return my_resources, player_response, proposed_trade, message

def parse_proposed_trade(s):
    trade = {}
    items = s.split(" Gives")
    for i in range(1, len(items)):
        item = items[i]
        prev_item = items[i - 1]
        player_id = str(prev_item[-2:].strip())
        subitem = item.split(" Player")[0].strip()
        try:
            resources = {k: float(v.replace(",", "").rstrip(".,;")) for k, v in (item.split(": ") for item in subitem.split(", "))}
        except Exception as e:
            print(subitem)
            raise e

        trade[player_id] = resources
    return trade

# print(parse_proposed_trade("Player 1 Gives X: 5, Y: 5; Player 2 Gives X: 0, Y: 0"))