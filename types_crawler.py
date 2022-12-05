import argparse

from utils import create_dir 
from utils import get_urls_of_type, article_type_dict
from urls_crawler import crawl_urls


def _init_dirs(output_dpath):
    create_dir(output_dpath)

    urls_dpath = "/".join([output_dpath, "urls"])
    results_dpath = "/".join([output_dpath, "results"])
    create_dir(urls_dpath)
    create_dir(results_dpath)
    
    return urls_dpath, results_dpath

def crawl_type(article_type, total_pages, urls_dpath, results_dpath):
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
    error_urls = crawl_urls(articles_urls_fpath, results_type_dpath)
    
    return error_urls

def crawl_all_types(total_pages, urls_dpath, results_dpath):
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
        error_urls = crawl_type(article_type, 
                                total_pages, 
                                urls_dpath, 
                                results_dpath)
        total_error_urls.extend(error_urls)
    
    return total_error_urls

def main(article_type, all_types=False, total_pages=1, output_dpath="data"): 
    urls_dpath, results_dpath = _init_dirs(output_dpath)
    error_urls = list()

    if all_types:
        error_urls = crawl_all_types(total_pages, urls_dpath, results_dpath)
    else:
        error_urls = crawl_type(article_type, 
                                total_pages, 
                                urls_dpath, 
                                results_dpath)
    return error_urls


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VNExpress urls crawler by type")

    parser.add_argument("--type", 
                        default="du-lich",
                        help="name of articles type",
                        dest="article_type")
    parser.add_argument("--all",
                        default=False,
                        action="store_true",
                        help="crawl all of types",
                        dest="all_types")
    parser.add_argument("--pages",
                        default=1,
                        type=int,
                        help="number of pages to crawl per type",
                        dest="total_pages")
    parser.add_argument("--output", 
                        default="data", 
                        help="saved directory path",
                        dest="output_dpath")
    
    args = parser.parse_args()

    main(**vars(args))
