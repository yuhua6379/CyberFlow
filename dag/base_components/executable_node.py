from abc import abstractmethod

from common.log.logger import get_logger
from dag.base.attach_to import AttachTo
from dag.base_components.end_note import EndNode
from dag.base_components.pipeline import PipeLine


class ExecutableNode(EndNode, AttachTo):

    def __init__(self, id_: int, label: str):
        super().__init__(id_, label)
        self.is_finish = False

    def attach_to(self, to_: PipeLine):
        get_logger().debug(f"Node:{self.id}-{self.label} attach to Node:{to_.to_node.id}-{to_.to_node.label}")
        self.out_edges.append(to_)

    def execute(self):
        """
        执行这个节点，并且把结果散播到下游去
        :return:
        """

        in_data = self.collect_results()

        get_logger().debug(f"Node:{self.id}-{self.label} receive: {in_data}")

        get_logger().info(f"Node:{self.id}-{self.label} executing...")
        out_data = self._execute(in_data)
        get_logger().debug(f"Node:{self.id}-{self.label} return: {out_data}")

        self.spread_results(out_data)

        self.is_finish = True

    @abstractmethod
    def _execute(self, input_: dict) -> dict:
        raise NotImplementedError

    def finish(self) -> bool:
        return self.is_finish

    def spread_results(self, data: dict):
        """
        给所有下游发送结果
        :return:
        """
        for pipeline in self.out_edges:
            pipeline: PipeLine
            pipeline.put(data)
