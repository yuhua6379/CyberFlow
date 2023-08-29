import copy
from abc import abstractmethod

import openai


class BaseLLM:

    @abstractmethod
    def chat(self, prompt: str) -> str:
        pass


class ChatGPT(BaseLLM):

    def __init__(self, **openai_params):
        self.openai_params = openai_params
        if "model" not in self.openai_params:
            self.openai_params["model"] = "gpt-3.5-turbo-0613"

        if "temperature" not in self.openai_params:
            self.openai_params['temperature'] = 0

    def _complete(self, prompt):
        messages = [
            {"role": "user", "content": prompt},
        ]
        params = copy.deepcopy(self.openai_params)
        params["messages"] = messages
        response = openai.ChatCompletion.create(**params)

        if response['choices'][0]['message']:
            return response['choices'][0]['message']['content'].strip()
        else:
            return ''

    def chat(self, prompt: str) -> str:
        return self._complete(prompt)
