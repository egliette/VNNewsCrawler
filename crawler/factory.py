from .vnexpress import VNExpressCrawler
from .dantri import DanTriCrawler


WEBNAMES = {'vnexpress': VNExpressCrawler,
            'dantri': DanTriCrawler}

def get_crawler(webname, **kwargs):
    crawler = WEBNAMES[webname](**kwargs)
    return crawler