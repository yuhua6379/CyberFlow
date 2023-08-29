from typing import Union

from pydantic import BaseModel

from dag.base_components.executable_node import ExecutableNode
from model.llm import BaseLLM


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str


class LLMSummarizer(ExecutableNode):

    @property
    def input(self) -> BaseModel:
        return Input

    @property
    def output(self) -> BaseModel:
        return Output

    def __init__(self, id_: int, label: str, prompt_template, llm: BaseLLM):
        super().__init__(id_, label)
        self.prompt_template = prompt_template
        self.llm = llm

    def _execute(self, input_: dict) -> dict:
        return {"output": input_["input"]}
        # input_["input"] = "\n".join(input_["input"])
        # return {"output": input_["input"]}#self.llm.chat(self.prompt_template.format(**input_))
