from abc import abstractmethod

from pydantic import BaseModel

from dag_parser.node import Node


class AttachFrom:
    @abstractmethod
    def attach_from(self, from_: Node):
        raise NotImplementedError

    @abstractmethod
    def input(self) -> BaseModel:
        raise NotImplementedError
