from pydantic import BaseModel

from dag.base_components.pipeline import PipeLine
from dag.base_components.start_node import StartNode


class Output(BaseModel):
    info: str


class InfoBox(StartNode):

    @property
    def output(self) -> BaseModel:
        return Output

    def __init__(self, id_: int, label: str, info: str):
        super().__init__(id_, label)
        self.info = info

    def finish(self):
        return True

    def execute(self):
        """
        给所有下游传递本节点存储的信息
        :return:
        """
        for pipeline in self.out_edges:
            pipeline: PipeLine
            pipeline.put({"info": self.info})
