from crawler.base_crawler import BaseCrawler
from .vnexpress import VNExpressCrawler


def get_crawler(webname: str):
    crawler = {
        'vnexpress': VNExpressCrawler,
    }[webname]

    return crawler