from abc import abstractmethod

from dag_parser.node import Node

FIRST_GROUP_ID = 1


class Edge:
    def __init__(self, id_: int, label: str):
        self.id = id_
        self.label = label

    @property
    @abstractmethod
    def from_node(self) -> Node:
        raise NotImplementedError

    @property
    @abstractmethod
    def to_node(self) -> Node:
        raise NotImplementedError
