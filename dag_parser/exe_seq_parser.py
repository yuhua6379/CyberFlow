from paradag import DAG
from paradag import SequentialProcessor
from paradag import dag_run

from dag_parser.edge import Edge
from dag_parser.node import Node
from dag_parser.traveler import DagTraveler


class ExecutorSimulator:
    def __init__(self):
        self.__level = {}
        self.__sequence = list()

    def param(self, vertex):
        return self.__level.get(vertex, 0)

    def execute(self, param):
        return param + 1

    def report_finish(self, vertices_result):
        vertex_list = list()
        for vertex, result in vertices_result:
            vertex_list.append(vertex)
        self.__sequence.append(vertex_list)

    def deliver(self, vertex, result):
        self.__level[vertex] = result

    def get_executor_sequence(self):
        return self.__sequence


class ExecutorSequenceParser(DagTraveler):

    def travel_node(self, node: Node) -> bool:
        self.add_vertex_from_node(node)

    def travel_edge(self, edge: Edge):
        if edge.id in self.traveled_edge:
            return
        else:
            self.traveled_edge.add(edge.id)

        if edge.from_node and edge.to_node:
            self.add_vertex_from_edge(edge)
            self.dag.add_edge(edge.from_node.id, edge.to_node.id)

    def __init__(self):
        self.dag = DAG()
        self.traveled_edge = set()

    def add_vertex_from_node(self, node: Node):
        if node.id not in self.dag.vertices():
            self.dag.add_vertex(node.id)

    def add_vertex_from_edge(self, edge: Edge):
        self.add_vertex_from_node(edge.from_node)
        self.add_vertex_from_node(edge.to_node)

    def parse(self):
        executor_simulator = ExecutorSimulator()
        dag_run(self.dag, processor=SequentialProcessor(), executor=executor_simulator)
        return executor_simulator.get_executor_sequence()
