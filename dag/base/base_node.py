from context.base_context import BaseContext
from dag_parser.node import Node


class BaseNode(Node):
    def __init__(self, id_: int, label: str):
        super().__init__(id_, label)
        self.out_edges_list: list[Node] = []
        self.in_edges_list: list[Node] = []
        self.context = None

    @property
    def out_edges(self) -> list:
        return self.out_edges_list

    @property
    def in_edges(self) -> list:
        return self.in_edges_list

    def register_context(self, context: BaseContext):
        self.context = context

    def get_context(self) -> BaseContext:
        return self.context
