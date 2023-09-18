from abc import abstractmethod
from enum import Enum
from functools import wraps

from pydantic import BaseModel

from common.log.logger import get_logger
from dag.base.attach_to import AttachTo
from dag.base_components.end_note import EndNode, UpStreamFail
from dag.base_components.executable import Status
from dag.base_components.pipeline import PipeLine
from dag.base_components.start_node import StartNode


class ExecutableNode(EndNode, StartNode):

    def _get_info(self):
        # 这个在ExecutableNode里面没有意义
        return None

    def attach_to(self, to_: PipeLine):
        get_logger().debug(f"Node:{self.id}-{self.label} attach to Node:{to_.to_node.id}-{to_.to_node.label}")
        self.out_edges.append(to_)

    def execute(self):
        """
        执行这个节点，并且把结果散播到下游去
        :return:
        """

        try:
            out_data = self.raw_execute().dict()
            get_logger().debug(f"Node:{self.id}-{self.label} return: {out_data}")

            self.spread_results(out_data)
            self.set_status(Status.SUCCESS)
        except Exception as e:
            import traceback
            get_logger().debug(f"Node:{self.id}-{self.label} fail because of: \n{traceback.format_exc()}")

            self.set_exception(e)
            self.set_status(Status.FAIL)

        self.set_finish()

    @abstractmethod
    def _execute(self, input_: dict):
        raise NotImplementedError

