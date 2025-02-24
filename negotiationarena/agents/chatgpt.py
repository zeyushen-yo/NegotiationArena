import copy
from openai import OpenAI
import os

import os
import random
from negotiationarena.agents.agents import Agent
import time
from negotiationarena.constants import AGENT_TWO, AGENT_ONE
from negotiationarena.agents.agent_behaviours import SelfCheckingAgent
from copy import deepcopy


class ChatGPTAgent(Agent):
    def __init__(
        self,
        agent_name: str,
        model="gpt-4-1106-preview",
        temperature=0.7,
        max_tokens=2000,
        seed=None,
    ):
        super().__init__(agent_name)
        self.run_epoch_time_ms = str(round(time.time() * 1000))
        self.model = model
        self.conversation = []
        if self.model in ["o1-mini", "o1", "o3-mini"]:
            self.prompt_entity_initializer = "user"
        else:
            self.prompt_entity_initializer = "system"
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.temperature = temperature
        self.max_tokens = max_tokens

    def init_agent(self, system_prompt, role):
        if AGENT_ONE in self.agent_name:
            # we use the user role to tell the assistant that it has to start.

            self.update_conversation_tracking(
                self.prompt_entity_initializer, system_prompt
            )
            self.update_conversation_tracking("user", role)
        elif AGENT_TWO in self.agent_name:
            system_prompt = system_prompt + role
            self.update_conversation_tracking(
                self.prompt_entity_initializer, system_prompt
            )
        else:
            raise "No Player 1 or Player 2 in role"

    def __deepcopy__(self, memo):
        """
        Deepcopy is needed because we cannot pickle the llama object.
        :param memo:
        :return:
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k == "client" and not isinstance(v, str):
                v = v.__class__.__name__
            setattr(result, k, deepcopy(v, memo))
        return result

    def chat(self):
        while True:
            if self.model == "o3-mini" or self.model == "o1-mini" or self.model == "o1":
                chat = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation,
                    max_completion_tokens=self.max_tokens
                )   
            else:
                chat = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
            response_content = chat.choices[0].message.content
            if response_content.strip():
                print(len(response_content))
                print("GPT's response starts: ", response_content)
                print("GPT's response ends.")
                return response_content

    def update_conversation_tracking(self, role, message):
        self.conversation.append({"role": role, "content": message})


class SelfCheckingChatGPTAgent(ChatGPTAgent, SelfCheckingAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
