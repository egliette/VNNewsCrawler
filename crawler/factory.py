from crawler.base_crawler import BaseCrawler
from .vnexpress import VNExpressCrawler


WEBNAMES = {'vnexpress': VNExpressCrawler}

def get_crawler(webname, **kwargs):
    crawler = WEBNAMES[webname](**kwargs)
    return crawler