import requests
import sys
from pathlib import Path

import tqdm
from bs4 import BeautifulSoup

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

from crawler.base_crawler import BaseCrawler
from utils.bs4_utils import write_content
from utils.utils import init_output_dirs, create_dir, read_file


article_type_dict = {
    0: "thoi-su",
    1: "du-lich",
    2: "the-gioi",
    3: "kinh-doanh",
    4: "khoa-hoc",
    5: "giai-tri",
    6: "the-thao",
    7: "phap-luat",
    8: "giao-duc",
    9: "suc-khoe",
    10: "doi-song"
}   


class VNExpressCrawler(BaseCrawler):
    @classmethod
    def crawl_urls(cls, urls_fpath: str = "urls.txt", output_dpath: str = "data") -> list[str]:
        create_dir(output_dpath)
        urls = list(read_file(urls_fpath))
        # length of digits in an integer
        index_len = len(str(len(urls)))
                        
        error_urls = list()
        with tqdm.tqdm(total=len(urls)) as pbar:
            for i, url in enumerate(urls):
                file_index = str(i+1).zfill(index_len)
                output_fpath = "".join([output_dpath, "/url_", file_index, ".txt"])
                is_success = write_content(url, output_fpath)
                if (not is_success):
                    error_urls.append(url)
                pbar.update(1)

        return error_urls

    @classmethod
    def crawl_types(cls, article_type: str, all_types: bool = False, total_pages: int = 1, output_dpath: str = "data") -> list[str]:
        urls_dpath, results_dpath = init_output_dirs(output_dpath)

        if all_types:
            error_urls = cls. crawl_all_types(total_pages, urls_dpath, results_dpath)
        else:
            error_urls = cls.crawl_type(article_type, 
                                    total_pages, 
                                    urls_dpath, 
                                    results_dpath)
        return error_urls

    @staticmethod
    def get_urls_of_type(article_type: str, total_pages: int = 1) -> list[str]:
        """"
        Get urls of articles in specific type 
        @param article_type (str): type of articles to get urls
        @param total_pages (int): number of pages to get urls
        @return articles_urls (list(str)): list of urls
        """
        articles_urls = list()
        for i in tqdm.tqdm(range(1, total_pages+1)):
            content = requests.get(f"https://vnexpress.net/{article_type}-p{i}").content
            soup = BeautifulSoup(content, "html.parser")
            titles = soup.find_all(class_="title-news")

            if (len(titles) == 0):
                # print(f"Couldn't find any news in the category {article_type} on page {i}")
                continue

            for title in titles:
                link = title.find_all("a")[0]
                articles_urls.append(link.get("href"))
    
        return articles_urls
    
    @classmethod
    def crawl_type(cls, article_type: str, total_pages: int, urls_dpath: str, results_dpath: str) -> list[str]:
        """"
        Crawl total_pages of articles in specific type 
        @param article_type (str): type of articles to crawl
        @param total_pages (int): number of pages to crawl
        @param urls_dpath (str): path to urls directory
        @param results_dpath (str): path to results directory
        @return error_urls (list(str)): list of error urls
        """
        print(f"Crawl articles type {article_type}")
        error_urls = list()
        
        # get urls
        articles_urls = cls.get_urls_of_type(article_type, total_pages)
        articles_urls_fpath = "/".join([urls_dpath, f"{article_type}.txt"])
        with open(articles_urls_fpath, "w") as urls_file:
            urls_file.write("\n".join(articles_urls)) 

        # crawl those urls
        results_type_dpath = "/".join([results_dpath, article_type])
        error_urls = cls.crawl_urls(articles_urls_fpath, results_type_dpath)
        
        return error_urls

    @classmethod
    def crawl_all_types(cls, total_pages: int, urls_dpath: str, results_dpath: str) -> list[str]:
        """"
        Crawl articles from all categories with total_pages per category
        @param total_pages (int): number of pages to crawl
        @param urls_dpath (str): path to urls directory
        @param results_dpath (str): path to results directory
        @return total_error_urls (list(str)): list of error urls
        """
        total_error_urls = list()
        
        num_types = len(article_type_dict) 
        for i in range(num_types):
            article_type = article_type_dict[i]
            error_urls = cls.crawl_type(article_type, 
                                    total_pages, 
                                    urls_dpath, 
                                    results_dpath)
            total_error_urls.extend(error_urls)
        
        return total_error_urls
