from typing import Union

from pydantic import BaseModel

from dag.base_components.executable_node import ExecutableNode
from model.llm import BaseLLM


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str


class LLMContentCompressor(ExecutableNode):

    def input(self) -> BaseModel:
        return Input

    def output(self) -> BaseModel:
        return Output

    def __init__(self, id_: int, label: str, llm: BaseLLM):
        super().__init__(id_, label)
        self.prompt_template = "'{input}'\n" \
                               "写一段上面这段话的摘要，且回复我这段摘要，且你只允许回复这段摘要。\n" \
                               "<>"
        self.llm = llm

    def _execute(self, input_: Input) -> dict:
        return Output(output=self.llm.chat(self.prompt_template.format(**input_.model_dump())))

