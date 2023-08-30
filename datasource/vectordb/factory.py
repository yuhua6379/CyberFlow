from datasource.vectordb.base import VectorDBConf, VectorDBType, VectorDbBase
from datasource.vectordb.chromadb_impl.impl import ChromaDB


class VectorDBFactory:
    def __init__(self, conf: VectorDBConf):
        self.vector_db_instances = {}
        self.conf = conf

    def get_vector_db(self, collection_name: str) -> VectorDbBase:

        if collection_name not in self.vector_db_instances:
            if self.conf.type == VectorDBType.Chromadb:
                self.vector_db_instances[collection_name] = ChromaDB(self.conf, collection_name)
            else:
                raise RuntimeError(f"unsupported vector db: {self.conf.type}")

        return self.vector_db_instances[collection_name]
