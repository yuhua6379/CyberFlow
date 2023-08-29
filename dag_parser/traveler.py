from abc import abstractmethod

from dag_parser.edge import Edge
from dag_parser.node import Node


class DagTraveler:

    @abstractmethod
    def travel_node(self, node: Node) -> bool:
        raise NotImplementedError

    @abstractmethod
    def travel_edge(self, edge: Edge):
        raise NotImplementedError
