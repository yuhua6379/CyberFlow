from abc import abstractmethod

from pydantic import BaseModel


class Node:
    def __init__(self, id_: int, label: str):
        self.id = id_
        self.label = label

    @property
    @abstractmethod
    def out_edges(self) -> list:
        raise NotImplementedError

    @property
    @abstractmethod
    def in_edges(self) -> list:
        raise NotImplementedError
