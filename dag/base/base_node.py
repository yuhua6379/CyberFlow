from abc import abstractmethod

from dag.base_components.pipeline import PipeLine
from dag_parser.node import Node


class BaseNode(Node):

    @property
    def out_edges(self) -> list:
        return self.out_edges_list

    @property
    def in_edges(self) -> list:
        return self.in_edges_list

    def __init__(self, id_: int, label: str):
        super().__init__(id_, label)
        self.out_edges_list: list[Node] = []
        self.in_edges_list: list[Node] = []
