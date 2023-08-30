from pydantic import BaseModel

from dag.base_components.end_note import EndNode
from model.llm import BaseLLM


class Input(BaseModel):
    input: str


class SimpleReply(EndNode):

    def input(self) -> BaseModel:
        return Input

    def finish(self):
        return True

    def execute(self):
        input_ = Input.model_validate(self.collect_results())
        print(input_.input)

    def __init__(self, id_: int, label: str, llm: BaseLLM):
        super().__init__(id_, label)
        self.llm = llm
