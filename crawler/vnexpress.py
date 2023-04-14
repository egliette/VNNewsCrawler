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
    def crawl_urls(cls, urls_fpath="urls.txt", output_dpath="data", num_workers=1):
        """
        Crawling contents from a list of urls
        Returns:
            list of failed urls
        """
        create_dir(output_dpath)
        urls = list(read_file(urls_fpath))
        num_urls = len(urls)
        # number of digits in an integer
        index_len = len(str(num_urls))

        args = (urls, [output_dpath]*num_urls, range(num_urls), [index_len]*num_urls)
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            results = list(tqdm(executor.map(cls.crawl_url_thread, *args), total=num_urls))
    
        return [result for result in results if result is not None]

    @classmethod
    def crawl_url_thread(cls, url, output_dpath, index, index_len):
        """ Crawling content of the specific url """
        file_index = str(index + 1).zfill(index_len)
        output_fpath = "".join([output_dpath, "/url_", file_index, ".txt"])
        is_success = write_content(url, output_fpath)
        if (not is_success):
            return url
        else:
            return None

    @classmethod
    def crawl_types(cls, article_type, all_types=False, total_pages=1, 
                    output_dpath="data", num_workers=1):
        """ Crawling contents of a specific type or all types """
        urls_dpath, results_dpath = init_output_dirs(output_dpath)

        if all_types:
            error_urls = cls.crawl_all_types(total_pages, urls_dpath, 
                                             results_dpath, num_workers)
        else:
            error_urls = cls.crawl_type(article_type, total_pages, urls_dpath, 
                                        results_dpath, num_workers)
        return error_urls

    @classmethod
    def crawl_type(cls, article_type, total_pages, urls_dpath, results_dpath, num_workers=1):
        """" Crawl total_pages of articles in specific type """
        print(f"Crawl articles type {article_type}")
        error_urls = list()
        
        # getting urls
        print(f"Getting urls of {article_type}...")
        articles_urls = cls.get_urls_of_type(article_type, total_pages, num_workers)
        articles_urls_fpath = "/".join([urls_dpath, f"{article_type}.txt"])
        with open(articles_urls_fpath, "w") as urls_file:
            urls_file.write("\n".join(articles_urls)) 

        # crawling urls
        print(f"Crawling from urls of {article_type}...")
        results_type_dpath = "/".join([results_dpath, article_type])
        error_urls = cls.crawl_urls(articles_urls_fpath, results_type_dpath, num_workers)
        
        return error_urls

    @classmethod
    def crawl_all_types(cls, total_pages, urls_dpath, results_dpath, num_workers=1):
        """" Crawl articles from all categories with total_pages per category """
        total_error_urls = list()
        
        num_types = len(article_type_dict) 
        for i in range(num_types):
            article_type = article_type_dict[i]
            error_urls = cls.crawl_type(article_type, 
                                        total_pages, 
                                        urls_dpath, 
                                        results_dpath,
                                        num_workers)
            total_error_urls.extend(error_urls)
        
        return total_error_urls

    @classmethod
    def get_urls_of_type(cls, article_type, total_pages=1, num_workers=1):
        """" Get urls of articles in a specific type """
        articles_urls = list()
        args = ([article_type]*total_pages, range(1, total_pages+1))
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            results = list(tqdm(executor.map(cls.get_urls_of_type_thread, *args), total=total_pages))

        articles_urls = sum(results, [])
    
        return articles_urls

    @staticmethod
    def get_urls_of_type_thread(article_type, page_number):
        """" Get urls of articles in a specific type in a page"""
        content = requests.get(f"https://vnexpress.net/{article_type}-p{page_number}").content
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.find_all(class_="title-news")

        if (len(titles) == 0):
            # print(f"Couldn't find any news in https://vnexpress.net/{article_type}-p{page_number}")
            pass

        articles_urls = list()

        for title in titles:
            link = title.find_all("a")[0]
            articles_urls.append(link.get("href"))
    
        return articles_urls