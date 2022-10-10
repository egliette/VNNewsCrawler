import argparse

from utils import read_file, extract_content


def main(urls_fpath="urls.txt", output_dpath="data"):
    urls = read_file(urls_fpath)
    for i, url in enumerate(urls):
        title, description, paragraphs = extract_content(url)
        output_fpath = f"{output_dpath}/url_{i}.txt"
        with open(output_fpath, "w", encoding="utf-8") as file:
            file.write(title + "\n")
            for p in description:
                file.write(p + "\n")
            for p in paragraphs:
                file.write(p + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VNExpress Crawler")

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
