from pydantic import BaseModel
from common.base_thread import get_logger
from components.base.base_llm_node import BaseLLMNode
from components.tools.llm_calc.key_extract import KeyExtractCalc
from dag.base_components.executable_node import ExecutableNode
from model.llm import BaseLLM
import jieba
import re


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str


class LLMKeyExtract(BaseLLMNode):
    """
    关键词提取
    """

    def input(self):
        return Input

    def output(self):
        return Output

    def __init__(self,
                 id_: int,
                 label: str,
                 llm: BaseLLM,
                 key_desc: str,
                 content_desc: str = None,
                 max_tokens: int = 2000):
        """

        :param content_desc: 输入内容的描述，提供这个字段，可以提高准确率
        :param key_desc: 需要提取的关键内容
        :param max_tokens:
        """

        super().__init__(id_, label, llm, max_tokens)
        if content_desc is not None:
            content_desc = f"这是对下面文字的描述[{content_desc}]"
        else:
            content_desc = ""
        self.prompt_template = (f"{content_desc}，从以下内容提取出[{key_desc}]，仅仅回复内容不要加描述:\n"
                                "'{input}'\n"
                                "<>")

        self.calc = KeyExtractCalc(self.llm, max_tokens, self.prompt_template)

    def _execute(self, input_: Input) -> dict:
        return Output(output=self.calc.extract(input_.input))
