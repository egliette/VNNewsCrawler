# Vietnamese news crawler
[![Python 3.10.7](https://img.shields.io/badge/python-3.10.7-blue)](https://www.python.org/downloads/release/python-3107/)[![BeautifulSoup 0.0.1](https://img.shields.io/badge/BeautifulSoup-0.0.1-purple)](https://pypi.org/project/bs4/)[![Requests 2.28.1](https://img.shields.io/badge/Requests-2.28.1-black)](https://pypi.org/project/requests/)[![tqdm 4.64.1](https://img.shields.io/badge/tqdm-4.64.1-orange)](https://pypi.org/project/tqdm/)   
Crawling titles and paragraphs of VN Express articles using their URLs or categories names 

## Installation
Create virtual environment then install required packages:
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage
### Crawl by URL
To crawl by URLs, you need to provide them in a text file and then give their path inside the `--input` flag (default is `urls.txt`)  
```yaml
python VNNewsCrawler.py --webname vnexpress url [-h] [--input URLS_FPATH] [--output OUTPUT_DPATH] [--num_workers NUM_WORKERS]

options:
  -h, --help                  show this help message and exit
  --input URLS_FPATH          urls txt file path
  --output OUTPUT_DPATH       saved directory path
  --num_workers NUM_WORKERS   number of workers to crawl
```

### Crawl by category name
You can crawl a number of articles by one type or all types based on the flags you use. Currently, my program only supports the following categories:
```
thoi-su
du-lich
the-gioi
kinh-doanh
khoa-hoc
giai-tri
the-thao
phap-luat
giao-duc
suc-khoe
doi-song
```  
To crawl article in a single type, you must provide type name in `--type` flag and number of pages you want to crawl in `--pages` flag.  
For example if you run below command:  
```yaml
python VNNewsCrawler.py --webname vnexpress type --type khoa-hoc --pages 3
```  
It will crawl articles from
```
https://vnexpress.net/khoa-hoc-p1
https://vnexpress.net/khoa-hoc-p2
https://vnexpress.net/khoa-hoc-p3
```
To crawl article in all categories, you need to provide `--all` flag and number of pages `--pages` instead.  
```yaml
python VNNewsCrawler.py --webname vnexpress type [-h] [--type ARTICLE_TYPE] [--all] [--pages TOTAL_PAGES] [--output OUTPUT_DPATH] [--num_workers NUM_WORKERS]

optional arguments:
  -h, --help                  show this help message and exit
  --type ARTICLE_TYPE         name of articles type
  --all                       crawl all of types
  --pages TOTAL_PAGES         number of pages to crawl per type
  --output OUTPUT_DPATH       saved directory path
  --num_workers NUM_WORKERS   number of workers to crawl
```

## Appendix
I've crawled all categories of articles with 20 pages each that you can download [here](https://drive.google.com/file/d/1zgS3nldOGW90QKgumNtbarScqtycTLsz/view?usp=sharing).
## Todo
- [x] Speed up crawling progress with multithreading
- [ ] Add logging module
- [ ] Crawl in other news websites
