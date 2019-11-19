from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link


class ListOfListsExtractor(LinkExtractor):
    """
    Extract a generic link from a list of lists
    """

    # Get links as link objects
    def extract_links(self, response):
        lists = response.css('div.div-col.columns.column-width').xpath('./ul/li/a/@href').getall()
        return [Link('https://en.wikipedia.org' + link) for link in lists]

    # Get links as strings
    def extract_as_str(self, response):
        lists = response.css('div.div-col.columns.column-width').xpath('./ul/li/a/@href').getall()
        return ['https://en.wikipedia.org' + link for link in lists]


class BookListExtractor(object):
    """
    Extract books and authors from a list of books
    """

    # Get book links
    def extract_books(self, response):
        books = response.css('div.mw-parser-output').xpath('./ul/li/i/a/@href').getall()
        return [('https://en.wikipedia.org' + link) for link in books]

    # Get author links
    def extract_authors(self, response):
        # TODO Need to filter out non-author links
        authors = response.css('div.mw-parser-output').xpath('./ul/li/a/@href').getall()
        return [('https://en.wikipedia.org' + link) for link in authors]
