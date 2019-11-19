from scrapy.spiders import CrawlSpider, Rule
from ..link_extractors.wiki_page_extractor import WikiPostExtractor, WikiTopicExtractor
from ..parsers.wiki_page_parser import WikiPageParser


class EverythingCrawler(CrawlSpider):

    name = "everything"
    start_urls = ["https://en.wikipedia.org/wiki/Distributed_computing"]

    rules = (Rule(WikiPostExtractor(), callback="_parse_as_post"),
             Rule(WikiTopicExtractor(), callback="_parse_as_topic"))

    def _parse_as_post(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_page()


    def _parse_as_topic(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_topic()