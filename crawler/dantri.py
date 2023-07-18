import requests
import sys
from pathlib import Path
import concurrent.futures


from tqdm import tqdm
from bs4 import BeautifulSoup

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

from logger import log
from crawler.base_crawler import BaseCrawler
from utils.bs4_utils import write_content
from utils.utils import init_output_dirs, create_dir, read_file


article_type_dict = {
    0: "xa-hoi",
    1: "the-gioi",
    2: "kinh-doanh",
    3: "bat-dong-san",
    4: "the-thao",
    5: "lao-dong-viec-lam",
    6: "tam-long-nhan-ai",
    7: "suc-khoe",
    8: "van-hoa",
    9: "giai-tri",
    10: "suc-manh-so",
    11: "giao-duc",
    12: "an-sinh",
    13: "phap-luat"
}   


class DanTriCrawler(BaseCrawler):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.logger = log.get_logger(name=__name__)
        
    def start_crawling(self):
        error_urls = list()
        if self.task=="url":
            error_urls = self.crawl_urls(self.urls_fpath, self.output_dpath)
        elif self.task=="type":
            error_urls = self.crawl_types()

        self.logger.info(f"The number of failed URL: {len(error_urls)}")
        
    def crawl_urls(self, urls_fpath, output_dpath):
        """
        Crawling contents from a list of urls
        Returns:
            list of failed urls
        """
        self.logger.info(f"Start crawling urls from {urls_fpath} file...")
        create_dir(output_dpath)
        urls = list(read_file(urls_fpath))
        num_urls = len(urls)
        # number of digits in an integer
        self.index_len = len(str(num_urls))

        args = ([output_dpath]*num_urls, urls, range(num_urls))
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            results = list(tqdm(executor.map(self.crawl_url_thread, *args), total=num_urls))
    
        return [result for result in results if result is not None]
        self.logger.info(f"Saving crawling result into {output_dpath} directory...")

    def crawl_url_thread(self, output_dpath, url, index):
        """ Crawling content of the specific url """
        file_index = str(index + 1).zfill(self.index_len)
        output_fpath = "".join([output_dpath, "/url_", file_index, ".txt"])
        is_success = write_content(url, output_fpath)
        if (not is_success):
            self.logger.debug(f"Crawling unsuccessfully: {url}")
            return url
        else:
            return None

    def crawl_types(self):
        """ Crawling contents of a specific type or all types """
        urls_dpath, results_dpath = init_output_dirs(self.output_dpath)

        if self.all_types:
            error_urls = self.crawl_all_types(urls_dpath, results_dpath)
        else:
            error_urls = self.crawl_type(self.article_type, urls_dpath, results_dpath)
        return error_urls

    def crawl_type(self, article_type, urls_dpath, results_dpath):
        """" Crawl total_pages of articles in specific type """
        self.logger.info(f"Crawl articles type {article_type}")
        error_urls = list()
        
        # getting urls
        self.logger.info(f"Getting urls of {article_type}...")
        articles_urls = self.get_urls_of_type(article_type)
        articles_urls_fpath = "/".join([urls_dpath, f"{article_type}.txt"])
        with open(articles_urls_fpath, "w") as urls_file:
            urls_file.write("\n".join(articles_urls)) 

        # crawling urls
        self.logger.info(f"Crawling from urls of {article_type}...")
        results_type_dpath = "/".join([results_dpath, article_type])
        error_urls = self.crawl_urls(articles_urls_fpath, results_type_dpath)
        
        return error_urls

    def crawl_all_types(self, urls_dpath, results_dpath):
        """" Crawl articles from all categories with total_pages per category """
        total_error_urls = list()
        
        num_types = len(article_type_dict) 
        for i in range(num_types):
            article_type = article_type_dict[i]
            error_urls = self.crawl_type(article_type, urls_dpath, results_dpath)
            self.logger.info(f"The number of failed {article_type} URL: {len(error_urls)}")
            total_error_urls.extend(error_urls)
        
        return total_error_urls

    def get_urls_of_type(self, article_type):
        """" Get urls of articles in a specific type """
        articles_urls = list()
        args = ([article_type]*self.total_pages, range(1, self.total_pages+1))
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            results = list(tqdm(executor.map(self.get_urls_of_type_thread, *args), total=self.total_pages))

        articles_urls = sum(results, [])
    
        return articles_urls

    def get_urls_of_type_thread(self, article_type, page_number):
        """" Get urls of articles in a specific type in a page"""
        page_url = f"https://dantri.com.vn/{article_type}/trang-{page_number}.htm"
        content = requests.get(page_url).content
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.find_all(class_="article-title")

        if (len(titles) == 0):
            self.logger.info(f"Couldn't find any news in {page_url}")

        articles_urls = list()

        for title in titles:
            link = title.find_all("a")[0]
            articles_urls.append(link.get("href"))
    
        return articles_urls