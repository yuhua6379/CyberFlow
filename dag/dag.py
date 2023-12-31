from typing import Type

from dag.base.attach_from import AttachFrom
from dag.base.attach_to import AttachTo
from dag.base.mapper import Mapper
from dag.base_components.pipeline import PipeLine


class Dag:

    def __init__(self, name):
        self.name = name
        self.root = None
        self.id_ = -1
        self.node_dict = {}

    def connect(self, from_: AttachTo, to_: AttachFrom, mapper: Mapper, label: str = ""):
        new_edge_id = self.new_id()
        pipeline = PipeLine(new_edge_id, label, from_, to_, mapper)
        from_.attach_to(pipeline)
        to_.attach_from(pipeline)

    def allocate(self, type_: Type, *args, **kwargs):
        node_id = self.new_id()
        kwargs['id_'] = node_id
        node = type_(*args, **kwargs)
        self.node_dict[node_id] = node
        return node

    def new_id(self):
        self.id_ += 1
        return self.id_
