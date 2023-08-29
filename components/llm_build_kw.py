from pydantic import BaseModel

from dag.base_components.executable_node import ExecutableNode
from model.llm import BaseLLM


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str


class LLMBuildKW(ExecutableNode):

    def _execute(self, input_: dict) -> dict:
        prompt = self.prompt_template.format(**input_)
        res = self.llm.chat(prompt)
        return {"output": res}

    def __init__(self, id_: int, label: str, prompt_template: str, llm: BaseLLM):

        super().__init__(id_, label)
        self.prompt_template = prompt_template
        self.llm = llm

    @property
    def input(self) -> BaseModel:
        return Input

    @property
    def output(self) -> BaseModel:
        return Output

