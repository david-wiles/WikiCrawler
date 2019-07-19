from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
from ..items import BookItem, AuthorItem
import re


class Lists_Extractor(LinkExtractor):
    pass