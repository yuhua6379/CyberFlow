
from selenium import webdriver
from tools.crawler.cx_extractor import CxExtractor
from selenium.webdriver.chrome.options import Options


class HtmlCrawler:
    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            # 设置chrome浏览器无界面模式

            chrome_options.add_argument('--headless')

        self.browser = webdriver.Chrome(options=chrome_options)

        self.cx = CxExtractor()

    def get_page(self, url: str):
        self.browser.get(url)

    def get_content(self):
        content = self.cx.filter_tags(self.browser.page_source)
        return self.cx.getText(content)

