import logging

from graphviz import Digraph, Source

from dag.dag import Dag
from dag_parser.edge import Edge
from dag_parser.iterator import DagIterator
from dag_parser.node import Node
from dag_parser.traveler import DagTraveler


class DrawDag(DagTraveler):

    def travel_node(self, node: Node):
        self.draw_node(node)

    def travel_edge(self, edge: Edge):
        self.draw_edge(edge)

    def __init__(self):
        self.dot = Digraph(format="png", encoding='UTF-8')

    def draw_node(self, node: Node):
        self.dot.node(str(node.id), f"{node.id}-{node.label}", shape="oval", color="blue", fontname='Fangsong',
                      labelfontsize='8.0',
                      fontsize='8.0')

    def draw_edge(self, edge: Edge):
        self.dot.edge(str(edge.from_node.id), str(edge.to_node.id), xlabel=edge.label, color='gray',
                      arrowsize='0.5',
                      labelfontsize='8.0', fontsize='8.0', labelfontcolor="gray", fontcolor="black",
                      fontname='Fangsong')

    def to_pic(self, path, show=True):
        self.dot.save(path)  # 保存
        self.dot.render(path)
        # 从保存的文件读取并显示

        s = Source.from_file(path)
        logging.debug(s.source)  # 打印代码
        if show:
            s.view()  # 显示

    @classmethod
    def draw_from_root(cls, dag: Dag, f_name="./dag.gv"):
        draw = cls()
        di = DagIterator(draw)
        di.iter_downstream(dag.root)
        draw.to_pic(f_name, True)
