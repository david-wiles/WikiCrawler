from scrapy.spiders import Spider
from ..parsers.wiki_page_parser import WikiPageParser


class WikiBookSpider(Spider):
    """
    Get basic information about a book from a wikipedia article using WikiPageParser
    """
    name = 'WikiBookSpider'

    start_urls = ["file:///home/david/Desktop/Twelve%20Sharp%20-%20Wikipedia.html"]

    def parse(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_book()


class WikiAuthorSpider(Spider):
    """
    Get basic information about a author from a wikipedia article using WikiPageParser
    """
    name = 'WikiAuthorSpider'

    start_urls = ["file:///home/david/Desktop/James%20A.%20Michener%20-%20Wikipedia.html"]

    def parse(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_author()


class WikiPageSpider(Spider):
    """
    Get information from any Wikipedia article using WikiPageParser
    """
    name = "WikiPageSpider"

    start_urls = ["file:///home/david/Documents/scrapes/Supercomputer%20-%20Wikipedia.html"]

    def parse(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_page()