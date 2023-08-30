from pydantic import BaseModel

from components.base.base_llm_node import BaseLLMNode
from components.tools.crawler.html import HtmlCrawler
from components.tools.llm_calc.key_extract import KeyExtractCalc
from dag.base_components.executable_node import ExecutableNode


class PageUrl(BaseModel):
    query: str


class Content(BaseModel):
    result: str


class GenshinPageCrawler(BaseLLMNode):
    """
    爬取页面
    """

    def input(self):
        return PageUrl

    def output(self):
        return Content

    def _execute(self, input_: PageUrl) -> dict:
        crawler = HtmlCrawler()
        crawler.get_page(f"https://wiki.biligame.com/ys/{input_.query}")
        content = crawler.get_content()

        prompt_template = (
            f"这是关于{input_.query}的描述，从以下内容提取出关于{input_.query}是什么的内容，如果没有相关内容，回复'无':\n"
            "'{input}'\n"
            "<>")

        self.calc = KeyExtractCalc(self.llm, self.max_tokens, prompt_template)
        content = self.calc.extract(content)

        prompt = "回答以{q}为目的，精简以下面的段落并提取关键信息:\n'{c}'".format(q=self.get_context().get_user_input(),
                                                              c=content)
        content = self.calc.predict(prompt)
        return Content(result=content)
