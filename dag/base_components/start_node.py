from abc import ABC, abstractmethod

from common.log.logger import get_logger
from dag.base.attach_to import AttachTo
from dag.base.base_node import BaseNode
from dag.base_components.executable import Executable
from dag.base_components.pipeline import PipeLine


class StartNode(BaseNode, Executable, AttachTo, ABC):
    def __init__(self, id_: int, label: str):
        super().__init__(id_, label)
        self.is_finish = False

    def attach_to(self, to_: PipeLine):
        self.out_edges.append(to_)

    def spread_results(self, data: dict):
        """
        给所有下游发送结果
        :return:
        """
        for pipeline in self.out_edges:
            pipeline: PipeLine
            pipeline.put(data)

    @abstractmethod
    def _get_info(self):
        raise NotImplementedError

    def execute(self):
        """
        执行这个节点，并且把结果散播到下游去
        :return:
        """

        out_model = self._get_info()
        out_data = out_model.dict()
        get_logger().debug(f"Node:{self.id}-{self.label} return: {out_data}")

        self.spread_results(out_data)

        self.is_finish = True

    def finish(self) -> bool:
        return self.is_finish
