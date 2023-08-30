from pydantic import BaseModel

from components.tools.crawler.html import HtmlCrawler
from dag.base_components.executable_node import ExecutableNode


class PageUrl(BaseModel):
    url: str


class Content(BaseModel):
    content: str


class PageCrawler(ExecutableNode):
    """
    爬取页面
    """

    def input(self):
        return PageUrl

    def output(self):
        return Content

    def _execute(self, input_: PageUrl) -> dict:
        crawler = HtmlCrawler(blocks_width=6, threshold=60)
        crawler.get_page(input_.url)
        return Content(content=crawler.get_content())
