from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple

from pydantic import BaseModel

from datasource.vectordb.entities import Document, Response


class VectorDBType(Enum):
    Chromadb = "chromadb"


class VectorDBConf(BaseModel):
    uri: str
    type: VectorDBType


class VectorDbBase(ABC):

    def __init__(self, conf: VectorDBConf):
        self.conf = conf

    @abstractmethod
    def batch_query(self, query_texts: List[str], n_results: int = 10) -> List[Tuple[str, List[Response]]]:
        pass

    def query(self, query_text, n_results: int = 10) -> List[Response]:
        return self.batch_query([query_text], n_results=n_results)[0][1]

    @abstractmethod
    def batch_save(self, doc_list: List[Document]):
        pass

    def save(self, doc: Document):
        self.batch_save([doc])

    @abstractmethod
    def batch_get(self, ids: List[str]) -> List[Document]:
        pass

    def get(self, id_: str):
        ret = self.batch_get([id_])
        if len(ret) == 0:
            return None
        return ret[0]
