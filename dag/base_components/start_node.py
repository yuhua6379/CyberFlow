from abc import ABC, abstractmethod

from common.log.logger import get_logger
from dag.base.attach_to import AttachTo
from dag.base.base_node import BaseNode
from dag.base_components.executable import Executable, Status
from dag.base_components.pipeline import PipeLine


class StartNode(BaseNode, Executable, AttachTo, ABC):

    def __init__(self, id_: int, label: str):
        Executable.__init__(self)
        BaseNode.__init__(self, id_, label)

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

        try:
            out_model = self._get_info()
            out_data = out_model.dict()
            get_logger().debug(f"Node:{self.id}-{self.label} return: {out_data}")

            self.spread_results(out_data)
            self.set_status(Status.SUCCESS)
        except Exception as e:
            import traceback
            get_logger().debug(f"Node:{self.id}-{self.label} fail because of: \n{traceback.format_exc()}")

            self.set_exception(e)
            self.set_status(Status.FAIL)

        get_logger().info(f"Node:{self.id}-{self.label} finish")
        self.set_finish()
