import argparse

from crawler.factory import get_crawler, WEBNAMES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Vietnamese News crawler (with url/type)")
    parser.add_argument("--webname", 
                        default=list(WEBNAMES.keys())[0],
                        choices=list(WEBNAMES.keys()), 
                        help="Web that want to crawls",
                        dest="webname")
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
    parser_url_crawler.add_argument("--num_workers", 
                                    default=1,
                                    type=int, 
                                    help="number of workers to crawl",
                                    dest="num_workers")

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
    parser_type_crawler.add_argument("--num_workers", 
                                    default=1, 
                                    type=int, 
                                    help="number of workers to crawl",
                                    dest="num_workers")
                                    
    args = parser.parse_args()
    
    return args


def main(args: argparse.Namespace) -> None:
    crawler = get_crawler(args.webname)
    if args.task=="url":
        crawler.crawl_urls(args.urls_fpath, args.output_dpath, args.num_workers)
    elif args.task=="type":
        crawler.crawl_types(args.article_type, args.all_types, args.total_pages, 
                            args.output_dpath, args.num_workers)


if __name__ == "__main__":
    args = parse_args()
    main(args)