from scrapy.spiders import CrawlSpider, Rule
from ..link_extractors.list_of_books_extractors import \
    ListOfListsExtractor, BookListAuthorExtractor, BookListBookExtractor
from ..parsers.wiki_page_parser import WikiPageParser


class ListOfListsCrawler(CrawlSpider):
    name = "ListOfListsCrawler"
    start_urls = [
        "https://en.wikipedia.org/wiki/Lists_of_books"
    ]

    rules = (
        Rule(ListOfListsExtractor(), callback='_parse_list'),
    )

    def _parse_list(self):
        pass
