import pickle
import subprocess
import time
from abc import ABC, abstractmethod
from copy import deepcopy
from multiprocessing import Process
from typing import Any, Union

from pydantic import BaseModel

from common.base_thread import BaseThread
from common.log.logger import get_logger
from context.base_context import BaseContext
from dag.base_components.end_note import EndNode
from dag.base_components.executable import Status, Executable
from dag.base_components.executable_node import ExecutableNode
from dag.base_components.start_node import StartNode
from dag.dag import Dag
from dag_parser.draw_dag import DrawDag
from dag_parser.edge import Edge
from dag_parser.exe_seq_parser import ExecutorSequenceParser
from dag_parser.iterator import DagIterator
from dag_parser.node import Node
import os
import threading
from dag_parser.traveler import DagTraveler


class Result(BaseModel):
    failed_nodes: list = []
    succeed_nodes: list = []


class DrawResult(DrawDag):
    def draw_node(self, node: Union[StartNode, EndNode, ExecutableNode]):
        self.dot.node(str(node.id), f"{node.id}-{node.label} is {node.status()}", shape="oval", color="blue",
                      fontname='Fangsong',
                      labelfontsize='8.0',
                      fontsize='8.0')

    def draw_edge(self, edge: Edge):
        self.dot.edge(str(edge.from_node.id), str(edge.to_node.id), xlabel=edge.label, color='gray',
                      arrowsize='0.5',
                      labelfontsize='8.0', fontsize='8.0', labelfontcolor="gray", fontcolor="black",
                      fontname='Fangsong')


class BaseDagRun:
    def __init__(self, dag: Dag):
        super().__init__()
        self.dag_ = deepcopy(dag)
        self.root = self.dag_.root

    def draw_result(self, f_name="result.gv"):
        DrawResult.draw_from_root(self.dag_, f_name)

    @classmethod
    def generate_dag_iterator(cls, dag: Dag):
        parser = ExecutorSequenceParser()
        di = DagIterator(parser)
        di.iter_downstream(dag.root)
        return parser.parse()

    @abstractmethod
    def run(self, context: BaseContext):
        raise NotImplementedError

    def get_result(self) -> Result:
        res = Result()
        for _, node_id_set in enumerate(self.generate_dag_iterator(self.dag_)):
            for node_id in node_id_set:
                node = self.dag_.node_dict[node_id]
                if node.status() is Status.SUCCESS:
                    res.succeed_nodes.append(node)
                else:
                    res.failed_nodes.append(node)
        return res


class SequenceDagRun(BaseDagRun):

    def run(self, context: BaseContext):
        get_logger().info(f"start to [[RUN]]...")
        for batch, node_id_set in enumerate(self.generate_dag_iterator(self.dag_)):
            get_logger().info(f"execute sequence -> batch:{batch} nodes:{node_id_set}")
            for node_id in node_id_set:
                node = self.dag_.node_dict[node_id]
                node.register_context(context)
                node.execute_not_finish()


class NodeThread(BaseThread):

    def __init__(self,
                 node: Union[StartNode, EndNode, ExecutableNode],
                 prefix: str):
        log_path = f"{prefix}_Node_{node.id}_{node.label}.log"
        super().__init__(log_path)
        self.node = node

    def run(self):
        self.node.execute_not_finish()


class ParallelDagRun(BaseDagRun):
    def __init__(self, dag: Dag):
        super().__init__(dag)
        self.process_ = None
        self.context = None

    def run(self, context: BaseContext):
        get_logger().info(f"start to [[RUN]]...")

        nodes = []
        for _, node_id_set in enumerate(self.generate_dag_iterator(self.dag_)):
            for node_id in node_id_set:
                node = self.dag_.node_dict[node_id]
                node.register_context(context)
                nodes.append(node)

        # 启动所有的node thread
        threads = []
        max_workers = 20
        cur = 0
        for node in nodes:
            th = NodeThread(node, self.dag_.name)
            threads.append(th)
            th.start()
            cur += 1
            if cur % max_workers == 0:
                for th in threads:
                    th.join()

        for th in threads:
            th.join()



