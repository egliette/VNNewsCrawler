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
Modifying your crawler configuration file (default is `crawler_config.yml`) to customize your crawling progress. Then simply run:
```
python VNNewsCrawler.py [-h] [--config CONFIG_FPATH]

options:
  -h, --help              show this help message and exit
  --config CONFIG_FPATH   path to config file
```
### Crawl by URL
To crawl by URLs, you need to set `task: "url"` in configuration file and ignore fields below `# if task == "type"` line.

### Crawl by category name
To crawl by URLs, you need to set `task: "type"` in configuration file.  
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
To crawl article in a single type, you must set `all_types: False` and give the specific type in `article_type`. Setting number of pages you want to crawl in `total_pages`.  
For example if you run below command:  
```yaml
# if task == "type"
article_type: "khoa-hoc"
all_types: False
total_pages: 3
```  
It will crawl articles from
```
https://vnexpress.net/khoa-hoc-p1
https://vnexpress.net/khoa-hoc-p2
https://vnexpress.net/khoa-hoc-p3
```
To crawl article in all categories, you just need to set  `all_types: True`, the program will ignore the `article_type` field. 

## Appendix
I've crawled all categories of articles with 20 pages each that you can download [here](https://drive.google.com/file/d/1zgS3nldOGW90QKgumNtbarScqtycTLsz/view?usp=sharing).
## Todo
- [x] Speed up crawling progress with multithreading
- [x] Add logging module
- [x] Use yml config file instead of argparse
- [ ] Crawl in other news websites
