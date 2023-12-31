from pydantic import BaseModel

from dag.base_components.end_note import EndNode
from model.llm import BaseLLM


class Input(BaseModel):
    weapon_info: str
    character_info: str


prompt = """
{weapon_info}
{character_info}
以上是一些知识
请组织语言回答以下问题
{user_demand}
"""


class LLMReply(EndNode):

    def _execute(self, input_: Input):

        kw = input_.dict()
        kw["user_demand"] = self.get_context().get_user_input()
        print(self.llm.chat(prompt.format(**kw)))

    def input(self):
        return Input


    def __init__(self, id_: int, label: str, llm: BaseLLM):
        super().__init__(id_, label)
        self.llm = llm
