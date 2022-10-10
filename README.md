# VN Express article crawler
[![Python 3.10.7](https://img.shields.io/badge/python-3.10.7-blue)](https://www.python.org/downloads/release/python-3107/)[![BeautifulSoup 0.0.1](https://img.shields.io/badge/BeautifulSoup-0.0.1-purple)](https://pypi.org/project/bs4/)[![Requests 2.28.1](https://img.shields.io/badge/Requests-2.28.1-black)](https://pypi.org/project/requests/)  
Crawling titles and paragraphs of VN Express articles using URLs

## Installation
Create virtual environment then install required packages:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

```bash
VNECrawler.py [-h] [--input URLS_FPATH] [--output OUTPUT_DPATH]

options:
  -h, --help            show this help message and exit
  --input URLS_FPATH    urls txt file path
  --output OUTPUT_DPATH saved directory path
```

