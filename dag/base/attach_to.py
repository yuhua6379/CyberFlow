from abc import abstractmethod

from pydantic import BaseModel

from dag_parser.node import Node


class AttachTo:
    @abstractmethod
    def attach_to(self, to_: Node):
        raise NotImplementedError

    @abstractmethod
    def output(self) -> BaseModel:
        raise NotImplementedError
