from typing import List

from dag_parser.edge import Edge
from dag_parser.node import Node
from dag_parser.traveler import DagTraveler


class DagIterator:

    def __init__(self, traveler: DagTraveler):
        self.traveler = traveler
        self.traveled_node = set()
        self.traveled_edge = set()

    def travel_node(self, node: Node):
        if node in self.traveled_node:
            return False
        else:
            self.traveled_node.add(node)
            return self.traveler.travel_node(node)

    def travel_edge(self, edge: Edge):
        if edge in self.traveled_edge:
            return False
        else:
            self.traveled_edge.add(edge)
            self.traveler.travel_edge(edge)
            return True

    def iter(self, node: Node):
        if self.travel_node(node) is False:
            # 节点已经被处理过，或者需要被中断，可以中断了
            return

        edge_list: List[Edge] = node.in_edges

        if edge_list:
            for edge in edge_list:
                from_node = edge.from_node
                assert from_node
                self.travel_edge(edge)
                self.iter(from_node)

        edge_list: List[Edge] = node.out_edges

        if edge_list:
            for edge in edge_list:
                to_node = edge.to_node
                assert to_node
                self.travel_edge(edge)
                self.iter(to_node)

    def iter_upstream(self, node: Node):
        if self.travel_node(node) is False:
            # 节点已经被处理过，可以中断了
            return

        edge_list: List[Edge] = node.in_edges

        if edge_list:
            for edge in edge_list:
                from_node = edge.from_node
                assert from_node
                self.travel_edge(edge)
                self.iter_upstream(from_node)

    def iter_downstream(self, node: Node):
        if self.travel_node(node) is False:
            # 节点已经被处理过，可以中断了
            return

        edge_list: List[Edge] = node.out_edges

        if edge_list:
            for edge in edge_list:
                to_node = edge.to_node
                assert to_node
                self.travel_edge(edge)
                self.iter_downstream(to_node)
