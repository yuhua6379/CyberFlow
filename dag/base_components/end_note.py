import time
from abc import ABC, abstractmethod
from functools import wraps

from common.log.logger import get_logger
from dag.base.attach_from import AttachFrom
from dag.base.base_node import BaseNode
from dag.base_components.executable import Executable, Status
from dag.base_components.pipeline import PipeLine


class UpStreamFail(RuntimeError):
    pass


# def retry(times):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             for i in range(times):
#                 _exc = None
#                 try:
#                     return func(*args, **kwargs)
#                 except Exception as e:
#                     _exc = e
#
#                 raise _exc
#
#         return wrapper
#
#     return decorator


class EndNode(BaseNode, Executable, AttachFrom, ABC):
    def __init__(self, id_: int, label: str):
        Executable.__init__(self)
        BaseNode.__init__(self, id_, label)

    def attach_from(self, from_: PipeLine):
        self.in_edges.append(from_)

    @staticmethod
    def has_duplicate_keys(dict1: dict, dict2: dict):
        overlap_keys = set(dict1.keys()) & set(dict2.keys())
        if overlap_keys:
            return overlap_keys
        else:
            return None

    @abstractmethod
    def _execute(self, input_: dict):
        raise NotImplementedError

    def raw_execute(self):

        # 等待上游成功
        self.wait_for_upstream()
        in_data = self.collect_results()

        get_logger().debug(f"Node:{self.id}-{self.label} receive: {in_data}")

        get_logger().info(f"Node:{self.id}-{self.label} executing...")
        in_model = self.input().parse_obj(in_data)

        return self._execute(in_model)

    def execute(self):
        try:
            self.raw_execute()
            self.set_status(Status.SUCCESS)
        except Exception as e:
            import traceback
            get_logger().debug(f"Node:{self.id}-{self.label} fail because of: \n{traceback.format_exc()}")

            self.set_exception(e)
            self.set_status(Status.FAIL)

        get_logger().info(f"Node:{self.id}-{self.label} finish")

        self.set_finish()

    def wait_for_upstream(self):
        while True:
            unfinished_count = 0
            for pipeline in self.in_edges:
                upstream_node: Executable = pipeline.from_
                if upstream_node.finish() is False:
                    unfinished_count += 1

            if unfinished_count > 0:
                time.sleep(0.1)
                continue

            # 到达这里，证明都finish了
            return

    def collect_results(self):
        """
        收集所有上游执行的结果
        :return: key, data
        """

        results = dict()
        for pipeline in self.in_edges:
            upstream_node: Executable = pipeline.from_
            if upstream_node.finish() is False:
                return None
            else:
                data = pipeline.get()
                overlap_keys = self.has_duplicate_keys(results, data)
                if overlap_keys is not None:
                    raise RuntimeError(f"duplicate output: {overlap_keys}")
                results.update(data)

        return results
