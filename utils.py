import requests
from bs4 import BeautifulSoup


def read_file(path):
    with open(path, encoding="utf-8") as file:
        for line in file:
            yield line

def extract_content(url):
    content = requests.get(url).content
    soup = BeautifulSoup(content, "html.parser")

    title = soup.find("h1", class_="title-detail").text
    paragraphs = (p.text + "\n" for p in soup.find_all("p", class_="Normal"))
    return title, paragraphs
    
