from dag_parser.edge import Edge
from dag_parser.node import Node


class BaseEdge(Edge):
    def __init__(self, id_: int, label: str, from_: Node, to_: Node):
        super().__init__(id_, label)
        self.from_ = from_
        self.to_ = to_

    @property
    def from_node(self) -> Node:
        return self.from_

    @property
    def to_node(self) -> Node:
        return self.to_
