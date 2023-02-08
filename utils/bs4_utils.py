import requests

from bs4 import BeautifulSoup, NavigableString


def get_text_from_tag(tag):
    if isinstance(tag, NavigableString):
        return tag
                    
    # else if isinstance(tag, Tag):
    return tag.text


def extract_content(url: str) -> tuple:
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


def write_content(url: str, output_fpath: str) -> bool:
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


