from pydantic import BaseModel

from components.base.base_llm_node import BaseLLMNode
from components.tools.llm_calc.base import BaseCalc
from dag.base_components.executable_node import ExecutableNode
from model.llm import BaseLLM


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str


class LLMBuildKW(BaseLLMNode):
    """
    提权文本内的关键词
    """

    def __init__(self,
                 id_: int,
                 label: str,
                 llm: BaseLLM,
                 key_desc: str,
                 content_desc: str = None,
                 max_tokens: int = 3000):
        """

        :param content_desc: 输入内容的描述，提供这个字段，可以提高准确率
        :param key_desc: 需要提取的关键内容
        :param max_tokens:
        """

        super().__init__(id_, label, llm, max_tokens)
        if content_desc is not None:
            content_desc = f"这是对下面文字的描述 {content_desc}"
        else:
            content_desc = ""
        self.key_desc = key_desc
        self.prompt_template = (f"这是关于{key_desc}的知识:\n"
                                "{key_knowledge}\n\n"
                                f"{content_desc}，从以下内容提取出最可能是{key_desc}的一个关键词，注意是一个，仅仅回复内容不要加描述:\n"
                                "'{input}'\n"
                                "<>")

        self.calc = BaseCalc(self.llm, max_tokens)

    def _execute(self, input_: Input) -> dict:
        context = self.get_context()
        # key_knowledge = context.get_knowledge_base().search(self.key_desc)
        kw = input_.dict()
        kw["key_knowledge"] = context.get(self.key_desc)
        prompt = self.prompt_template.format(**kw)
        res = self.calc.predict(prompt)
        return Output(output=res)

    def input(self):
        return Input

    def output(self):
        return Output
