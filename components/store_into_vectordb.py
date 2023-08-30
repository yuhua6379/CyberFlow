from uuid import uuid4

from pydantic import BaseModel

from common.base_thread import get_logger
from components.tools.crawler.html import HtmlCrawler
from dag.base_components.end_note import EndNode
from dag.base_components.executable_node import ExecutableNode
from datasource.vectordb.base import VectorDBType, VectorDBConf
from datasource.vectordb.entities import Document
from datasource.vectordb.factory import VectorDBFactory
import time


class Input(BaseModel):
    input: str


class StoreIntoVectorDB(EndNode):
    """
    向量数据库存储组件，把数据存到数据库内
    """

    def __init__(self, id_: int, label: str,
                 collection_name: str,
                 conf: VectorDBConf,
                 distance: float = 1.0,
                 meta_data: dict = None,
                 ):
        """
        :param collection_name: vector_db的集合名
        :param conf: uri+type，提供以创建一个实例
        :param distance: 如果低于这个distance，默认是重复数据，就不再记录
        """
        super().__init__(id_, label)
        self.conf = conf
        self.collection_name = collection_name
        self.factory = VectorDBFactory(conf)
        self.distance = distance
        if meta_data is None:
            meta_data = {}

        self.meta_data = meta_data

    def _execute(self, input_: Input):
        db = self.factory.get_vector_db(self.collection_name)
        response_list = db.query(input_.input, n_results=1)

        summary = input_.input
        if len(summary) > 30:
            summary = summary[:30] + "..."

        if len(response_list) > 0:
            if response_list[0].distance <= self.distance:
                get_logger().info(f"[Skip] content: {summary} "
                                  f"will skip for the min distance is {response_list[0].distance}")
                return

        get_logger().info(f"[Store] content: {summary} will be store into {self.conf} {self.collection_name}")

        doc_id = str(uuid4())
        self.meta_data["doc_id"] = doc_id
        self.meta_data["time"] = time.time()
        db.save(Document(id=doc_id,
                         meta_data=self.meta_data,
                         content=input_.input))

    def input(self):
        return Input
