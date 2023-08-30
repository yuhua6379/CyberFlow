from components.tools.crawler.html import HtmlCrawler


def test_HtmlCrawler():
    crawler = HtmlCrawler()
    crawler.get_page('https://zh.wikipedia.org/wiki/%E5%8C%97%E4%BA%AC%E5%B8%82')
    assert len(crawler.get_content()) > 1000
