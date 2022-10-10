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
    # some sport news have location-stamp child tag inside description tag
    description = (p.text for p in soup.find("p", class_="description").contents)
    paragraphs = (p.text for p in soup.find_all("p", class_="Normal"))
    return title, description, paragraphs
    
