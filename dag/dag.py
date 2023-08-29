from typing import Type

from common.log.logger import get_logger
from dag.base.attach_from import AttachFrom
from dag.base.attach_to import AttachTo
from dag.base.base_edge import BaseEdge
from dag.base.base_node import BaseNode
from dag.base.mapper import Mapper
from dag.base_components.end_note import EndNode
from dag.base_components.executable import Executable
from dag.base_components.executable_node import ExecutableNode
from dag.base_components.pipeline import PipeLine
from dag_parser.exe_seq_parser import ExecutorSequenceParser


class Dag:

    def __init__(self):
        self.id_ = -1

    def connect(self, from_: AttachTo, to_: AttachFrom, mapper: Mapper, label: str = ""):
        new_edge_id = self.new_id()
        pipeline = PipeLine(new_edge_id, label, from_, to_, mapper)
        from_.attach_to(pipeline)
        to_.attach_from(pipeline)

    def allocate(self, type_: Type, *args, **kwargs):
        kwargs['id_'] = self.new_id()
        return type_(*args, **kwargs)

    def new_id(self):
        self.id_ += 1
        return self.id_


class DagRun(ExecutorSequenceParser):

    def __init__(self):
        super().__init__()
        self.node_dict = dict()

    def add_vertex_from_node(self, node: BaseNode):

        super().add_vertex_from_node(node)
        self.node_dict[node.id] = node

    def run(self):
        get_logger().info(f"start to [[RUN]]...")
        for _, node_id_set in enumerate(self.parse()):
            for node_id in node_id_set:
                node = self.node_dict[node_id]

                # if isinstance(node, EndNode):
                #     print(f"running: {node_id}: {node.label} params: {node.collect_results()}")
                # else:
                #     print(f"running: {node_id}: {node.label}")

                node.execute()

