from common.log.logger import get_logger
from dag_parser.exe_seq_parser import ExecutorSequenceParser
from dag_parser.iterator import DagIterator
from dag_parser.node import Node


class DagRun(ExecutorSequenceParser):

    def __init__(self, root: Node):
        super().__init__()
        self.node_dict = dict()
        self.root = root

        di = DagIterator(self)
        di.iter_downstream(root)

    def add_vertex_from_node(self, node: Node):

        super().add_vertex_from_node(node)
        self.node_dict[node.id] = node

    def run(self, context):
        get_logger().info(f"start to [[RUN]]...")
        for _, node_id_set in enumerate(self.parse()):
            for node_id in node_id_set:
                node = self.node_dict[node_id]
                node.register_context(context)
                node.execute()
