from pydantic import BaseModel

from components.tools.crawler.html import HtmlCrawler
from dag.base_components.executable_node import ExecutableNode


class PageUrl(BaseModel):
    urls: list[str]


class Content(BaseModel):
    contents: list[str]


class BatchPageCrawler(ExecutableNode):
    """
    批量爬取页面
    """

    def input(self):
        return PageUrl

    def output(self):
        return Content

    def _execute(self, input_: PageUrl) -> dict:

        res = list()
        for url in input_.urls:
            crawler = HtmlCrawler(blocks_width=6, threshold=60)
            crawler.get_page(url)
            res.append(crawler.get_content())
        return Content(contents=res)
