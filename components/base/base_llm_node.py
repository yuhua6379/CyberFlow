from abc import ABC

from dag.base_components.executable_node import ExecutableNode
from model.llm import BaseLLM
import jieba


class BaseLLMNode(ExecutableNode, ABC):
    def __init__(self, id_: int, label: str, llm: BaseLLM, max_tokens: int):
        super().__init__(id_, label)
        self.max_tokens = max_tokens
        self.llm = llm
