from typing import Union

from pydantic import BaseModel

from dag.base_components.end_note import EndNode
from model.llm import BaseLLM


class Input(BaseModel):
    weapon: str
    artifact: str
    character: str


class SimpleReply(EndNode):

    def _execute(self, input_: Input):
        print("武器：")
        print(input_.weapon)
        print("----------------------------------------")

        print("装备：")
        print(input_.artifact)
        print("----------------------------------------")

        print("角色：")
        print(input_.character)
        print("----------------------------------------")

    def input(self):
        return Input

    def finish(self):
        return True

