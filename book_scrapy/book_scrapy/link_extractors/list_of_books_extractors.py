from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link


class ListOfListsExtractor(LinkExtractor):

    def extract_links(self, response):
        lists = response.css('div.div-col.columns.column-width').xpath('./ul/li/a/@href').getall()
        return [Link('https://en.wikipedia.org' + link) for link in lists]


class BookListBookExtractor(LinkExtractor):

    def extract_links(self, response):
        books = response.css('div.mw-parser-output').xpath('./ul/li/i/a/@href').getall()
        return [Link('https://en.wikipedia.org' + link) for link in books]


class BookListAuthorExtractor(LinkExtractor):

    def extract_links(self, response):
        # TODO Need to filter out non-author links
        authors = response.css('div.mw-parser-output').xpath('./ul/li/a/@href').getall()
        return [Link('https://en.wikipedia.org' + link) for link in authors]
