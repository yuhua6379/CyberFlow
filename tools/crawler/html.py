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


if __name__ == '__main__':
    crawler = HtmlCrawler()
    crawler.get_page('https://zh.wikipedia.org/wiki/%E5%8C%97%E4%BA%AC%E5%B8%82')
    print(crawler.get_content())
