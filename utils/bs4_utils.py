import tqdm
import requests
from bs4 import BeautifulSoup, NavigableString


def get_text_from_tag(tag):
    if isinstance(tag, NavigableString):
        return tag
                    
    # else if isinstance(tag, Tag):
    return tag.text


def extract_content(url):
    """
    Extract title, description and paragraphs from url
    @param url (str): url to crawl
    @return title (str)
    @return description (generator)
    @return paragraphs (generator)
    """
    content = requests.get(url).content
    soup = BeautifulSoup(content, "html.parser")

    title = soup.find("h1", class_="title-detail") 
    if title == None:
        return None, None, None
    title = title.text

    # some sport news have location-stamp child tag inside description tag
    description = (get_text_from_tag(p) for p in soup.find("p", class_="description").contents)
    paragraphs = (get_text_from_tag(p) for p in soup.find_all("p", class_="Normal"))

    return title, description, paragraphs


def write_content(url, output_fpath):
    """
    From url, extract title, description and paragraphs then write in output_fpath
    @param url (str): url to crawl
    @param output_fpath (str): file path to save crawled result
    @return (bool): True if crawl successfully and otherwise
    """
    title, description, paragraphs = extract_content(url)
                
    if title == None:
        return False

    with open(output_fpath, "w", encoding="utf-8") as file:
        file.write(title + "\n")
        for p in description:
            file.write(p + "\n")
        for p in paragraphs:                     
            file.write(p + "\n")

    return True


def get_urls_of_type(article_type, total_pages=1):
    """"
    Get urls of articles in specific type 
    @param article_type (str): type of articles to get urls
    @param total_pages (int): number of pages to get urls
    @return articles_urls (list(str)): list of urls
    """
    articles_urls = list()
    for i in tqdm.tqdm(range(1, total_pages+1)):
        content = requests.get(f"https://vnexpress.net/{article_type}-p{i}").content
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.find_all(class_="title-news")

        if (len(titles) == 0):
            # print(f"Couldn't find any news in the category {article_type} on page {i}")
            continue

        for title in titles:
            link = title.find_all("a")[0]
            articles_urls.append(link.get("href"))
    
    return articles_urls

