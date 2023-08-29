from pydantic import BaseModel

from dag.base_components.executable_node import ExecutableNode


class Query(BaseModel):
    query: str


class Results(BaseModel):
    result: str


class Searcher(ExecutableNode):

    @property
    def input(self) -> BaseModel:
        return Query

    @property
    def output(self) -> BaseModel:
        return Results

    def _execute(self, input_: dict) -> dict:
        if input_["query"].find("夜兰") != -1:
            return {"result": "夜兰是一名生命需求的水系输出弓箭手"}
        elif input_["query"].find("裁叶萃光") != -1:
            return {"result": "裁叶萃光是一把精通需求角色单手剑"}
        elif input_["query"].find("海染") != -1:
            return {"result": "海染套是一套增加治疗量的套装，适合奶妈"}
        else:
            return {"result": "查询不到结果"}
