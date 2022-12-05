import argparse

import tqdm

from utils import read_file, create_dir 
from utils import write_content


def crawl_urls(urls_fpath="urls.txt", output_dpath="data"):
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

def main(urls_fpath, output_dpath):
    crawl_urls(urls_fpath, output_dpath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VNExpress urls crawler")

    parser.add_argument("--input", 
                        default="urls.txt", 
                        help="urls txt file path",
                        dest="urls_fpath")
    parser.add_argument("--output", 
                        default="data", 
                        help="saved directory path",
                        dest="output_dpath")
    
    args = parser.parse_args()

    main(**vars(args))
