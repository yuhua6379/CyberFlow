from typing import Union

from pydantic import BaseModel
from dag.base_components.start_node import StartNode


class Output(BaseModel):
    info: Union[str, list[str]]


class InfoBox(StartNode):
    """
    消息箱子，仅仅提供消息
    """
    def __init__(self, id_: int, label: str):
        """
        :param info: 记录的消息
        """
        super().__init__(id_, label)

    def _get_info(self):
        return Output(info=self.get_context().get_user_input())

    def output(self):
        return Output

    def finish(self):
        return True
