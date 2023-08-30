from pydantic import BaseModel


class Document(BaseModel):
    # primary key
    id: str

    # json
    meta_data: dict

    # 内容 -> 向量化
    content: str


class Response(BaseModel):
    document: Document
    distance: float
