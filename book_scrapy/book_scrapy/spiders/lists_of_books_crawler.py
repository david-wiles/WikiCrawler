from scrapy.spiders import Spider
from ..link_extractors.list_of_books_extractors import \
    ListOfListsExtractor, BookListExtractor
from ..parsers.wiki_page_parser import WikiPageParser
from scrapy.http.request import Request


class ListOfListsCrawler(Spider):
    name = "ListOfListsCrawler"

    # Start from list of lists
    def start_requests(self):
        return [Request("file:///home/david/Desktop/Lists%20of%20books%20-%20Wikipedia.html", callback=self._parse_)]

    def _parse_(self, response):
        extractor = ListOfListsExtractor()
        links = extractor.extract_as_str(response)

        for link in links:
            yield Request(link, callback=self._parse_list)

    # Extract books and authors from each list
    def _parse_list(self, response):
        extractor = BookListExtractor()
        books = extractor.extract_books(response)
        authors = extractor.extract_authors(response)

        for book in books:
            yield Request(book, callback=self._parse_book)

        for author in authors:
            yield Request(author, callback=self._parse_author)

    # Parse each book and author page
    def _parse_book(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_book()

    def _parse_author(self, response):
        parser = WikiPageParser(response)
        yield parser.parse_author()
