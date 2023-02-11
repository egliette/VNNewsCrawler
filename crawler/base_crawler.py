from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    @abstractmethod
    def crawl_urls(self) -> list[str]:
        pass

    @abstractmethod
    def crawl_types(self) -> list[str]:
        pass
