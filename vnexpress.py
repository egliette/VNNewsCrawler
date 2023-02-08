import argparse

import tqdm

from utils.utils import read_file, create_dir, article_type_dict
from utils.bs4_utils import write_content, get_urls_of_type


def _init_dirs(output_dpath):
    create_dir(output_dpath)

    urls_dpath = "/".join([output_dpath, "urls"])
    results_dpath = "/".join([output_dpath, "results"])
    create_dir(urls_dpath)
    create_dir(results_dpath)
    
    return urls_dpath, results_dpath


class VNExpressCrawler:
    @classmethod
    def crawl_urls(cls, urls_fpath="urls.txt", output_dpath="data"):
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
    def crawl_types(cls, article_type, all_types=False, total_pages=1, output_dpath="data"):
        urls_dpath, results_dpath = _init_dirs(output_dpath)

        if all_types:
            error_urls = cls. crawl_all_types(total_pages, urls_dpath, results_dpath)
        else:
            error_urls = cls.crawl_type(article_type, 
                                    total_pages, 
                                    urls_dpath, 
                                    results_dpath)
        return error_urls

    @classmethod
    def crawl_type(cls, article_type, total_pages, urls_dpath, results_dpath):
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
        articles_urls = get_urls_of_type(article_type, total_pages)
        articles_urls_fpath = "/".join([urls_dpath, f"{article_type}.txt"])
        with open(articles_urls_fpath, "w") as urls_file:
            urls_file.write("\n".join(articles_urls)) 

        # crawl those urls
        results_type_dpath = "/".join([results_dpath, article_type])
        error_urls = cls.crawl_urls(articles_urls_fpath, results_type_dpath)
        
        return error_urls

    @classmethod
    def crawl_all_types(cls, total_pages, urls_dpath, results_dpath):
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


def parse_args():
    parser = argparse.ArgumentParser(description="VNExpress urls/types crawler")
    subparsers = parser.add_subparsers(title='task', dest='task')

    # Subparser for the "url" task
    parser_url_crawler = subparsers.add_parser('url', help='Craw by urls')
    parser_url_crawler.add_argument("--input", 
                        default="urls.txt", 
                        help="urls txt file path",
                        dest="urls_fpath")
    parser_url_crawler.add_argument("--output", 
                        default="data", 
                        help="saved directory path",
                        dest="output_dpath")

    # Subparser for the "type" task
    parser_type_crawler = subparsers.add_parser('type', help='Craw by types')
    parser_type_crawler.add_argument("--type", 
                        default="du-lich",
                        help="name of articles type",
                        dest="article_type")
    parser_type_crawler.add_argument("--all",
                        default=False,
                        action="store_true",
                        help="crawl all of types",
                        dest="all_types")
    parser_type_crawler.add_argument("--pages",
                        default=1,
                        type=int,
                        help="number of pages to crawl per type",
                        dest="total_pages")
    parser_type_crawler.add_argument("--output", 
                    default="data", 
                    help="saved directory path",
                    dest="output_dpath")
                    
    args = parser.parse_args()

    return args


def main(args):
    if args.task=="url":
        VNExpressCrawler.crawl_urls(args.urls_fpath, args.output_dpath)
    elif args.task=="type":
        VNExpressCrawler.crawl_types(args.article_type, args.all_types, args.total_pages, args.output_dpath)


if __name__ == "__main__":
    args = parse_args()
    main(args)
