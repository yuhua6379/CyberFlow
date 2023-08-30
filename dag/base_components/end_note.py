from abc import ABC, abstractmethod

from common.log.logger import get_logger
from dag.base.attach_from import AttachFrom
from dag.base.base_node import BaseNode
from dag.base_components.executable import Executable
from dag.base_components.pipeline import PipeLine


class EndNode(BaseNode, Executable, AttachFrom, ABC):
    def __init__(self, id_: int, label: str):
        super().__init__(id_, label)
        self.is_finish = False

    def attach_from(self, from_: PipeLine):
        self.in_edges.append(from_)

    @staticmethod
    def has_duplicate_keys(dict1: dict, dict2: dict):
        overlap_keys = set(dict1.keys()) & set(dict2.keys())
        if overlap_keys:
            return overlap_keys
        else:
            return None

    def finish(self):
        return self.is_finish

    @abstractmethod
    def _execute(self, input_: dict):
        raise NotImplementedError

    def execute(self):
        """
        执行这个节点，并且把结果散播到下游去
        :return:
        """

        in_data = self.collect_results()

        get_logger().debug(f"Node:{self.id}-{self.label} receive: {in_data}")

        get_logger().info(f"Node:{self.id}-{self.label} executing...")
        in_model = self.input().parse_obj(in_data)
        self._execute(in_model)
        self.is_finish = True

    def collect_results(self):
        """
        收集所有上游执行的结果
        :return: key, data
        """

        results = dict()
        for pipeline in self.in_edges:
            upstream_node: Executable = pipeline.from_
            if upstream_node.finish() is False:
                # 仍有未完成的节点，且要求严格校验，返回空
                return None
            else:
                data = pipeline.get()
                overlap_keys = self.has_duplicate_keys(results, data)
                if overlap_keys is not None:
                    raise RuntimeError(f"duplicate output: {overlap_keys}")
                results.update(data)

        return results
