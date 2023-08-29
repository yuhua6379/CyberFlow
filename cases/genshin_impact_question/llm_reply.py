from pydantic import BaseModel
from dag.base_components.end_note import EndNode
from model.llm import BaseLLM


class Input(BaseModel):
    weapon_info: str
    character_info: str
    user_demand: str


prompt = """
{weapon_info}
{character_info}
以上是一些知识
请组织语言回答以下问题
{user_demand}
"""


class LLMReply(EndNode):

    @property
    def input(self) -> BaseModel:
        return Input

    def finish(self):
        return True

    def execute(self):
        input_ = Input.model_validate(self.collect_results())
        print(self.llm.chat(prompt.format(**input_.model_dump())))

    def __init__(self, id_: int, label: str, llm: BaseLLM):
        super().__init__(id_, label)
        self.llm = llm
