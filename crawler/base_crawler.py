from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    @abstractmethod
    def crawl_urls(self) -> None:
        pass

    @abstractmethod
    def crawl_types(self) -> None:
        pass