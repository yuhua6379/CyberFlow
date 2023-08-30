from abc import abstractmethod

from datasource.vectordb.base import VectorDbBase
from datasource.vectordb.entities import Response


class KnowledgeBase:

    @abstractmethod
    def _search(self, keyword: str, topn: int = 10) -> list[Response]:
        raise NotImplementedError

    def search(self, keyword: str, topn: int = 10) -> list[Response]:
        results = sorted(self._search(keyword, topn), key=lambda c: c.distance, reverse=True)
        return results[0: topn]


class VectorDBKnowledgeBase(KnowledgeBase):
    def __init__(self, db: VectorDbBase):
        self.db = db

    def _search(self, keyword: str, topn: int = 10) -> list[Response]:
        return self.db.query(keyword, topn)
