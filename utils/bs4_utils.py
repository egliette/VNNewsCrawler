import requests

from bs4 import BeautifulSoup, NavigableString


def get_text_from_tag(tag):
    if isinstance(tag, NavigableString):
        return tag
                    
    # else if isinstance(tag, Tag):
    return tag.text