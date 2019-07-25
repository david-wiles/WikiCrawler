from scrapy.spiders import CrawlSpider, Rule
from ..link_extractors.publishers_weekly_extractors import BookLinkExtractor, AuthorLinkExtractor
from ..parsers.wiki_page_parser import WikiPageParser


class PublishersWeeklyCrawler(CrawlSpider):
    """
    Class to get links to bestselling books, as determined by publisher's weekly
    """
    name = 'PublishersWeeklyCrawler'
    start_urls = [
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1890s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1900s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1910s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1920s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1930s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1940s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1950s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1960s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1970s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1980s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1990s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_2000s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_2010s"
    ]

    rules = (Rule(BookLinkExtractor(), callback='_parse_book'),
             Rule(AuthorLinkExtractor(), callback='_parse_author'))

    def _parse_book(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_book()


    def _parse_author(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_author()
