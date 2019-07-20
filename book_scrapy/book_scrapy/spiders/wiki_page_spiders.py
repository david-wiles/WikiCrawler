from scrapy.spiders import Spider
from ..parsers.wiki_page_parser import WikiPageParser


class WikiBookSpider(Spider):
    """
    Spider to get basic information about a book from a wikipedia article
    """
    name = 'WikiBookSpider'

    start_urls = ["file:///home/david/Desktop/Twelve%20Sharp%20-%20Wikipedia.html"]

    def parse(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_book()


class WikiAuthorSpider(Spider):
    """
    Spider to get basic information about a book from a wikipedia article
    """
    name = 'WikiAuthorSpider'

    start_urls = ["file:///home/david/Desktop/James%20A.%20Michener%20-%20Wikipedia.html"]

    def parse(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_author()
