from dag.base.base_edge import BaseEdge
from dag.base.mapper import Mapper
from dag_parser.node import Node


class PipeLine(BaseEdge):

    def __init__(self, id_: int, label: str, from_: Node, to_: Node, mapper: Mapper):
        super().__init__(id_, label, from_, to_)

        self.data = None
        self.mapper = mapper

    def put(self, data: str):
        self.data = data

    def get(self):
        # 按要求改名
        output_data = dict()
        if self.data is None:
            # 上游出异常了，所以抛弃这个输入，但返回空值，如果是optional选项则下游不受影响
            return output_data

        for k, v in self.data.items():
            output_data[k] = v

        for k1, k2 in self.mapper.map_.items():
            temp = output_data[k1]
            del output_data[k1]
            output_data[k2] = temp

        return output_data
