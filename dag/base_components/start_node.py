from abc import ABC

from dag.base.attach_to import AttachTo
from dag.base.base_node import BaseNode
from dag.base_components.executable import Executable
from dag.base_components.pipeline import PipeLine


class StartNode(BaseNode, Executable, AttachTo, ABC):

    def attach_to(self, to_: PipeLine):
        self.out_edges.append(to_)
