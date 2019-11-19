from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link


class BookLinkExtractor(LinkExtractor):
    """
    Extract a book from publisher's weekly list
    """
    def extract_links(self, response):
        # Get each link from the list of books for each year
        links = [
            books.xpath('./li/i/a/@href').getall()
            for books in response.xpath('//*[@id="mw-content-text"]/div/ol')
        ]

        # Flatten, format, and return
        return [Link('https://en.wikipedia.org' + link) for sublist in links for link in sublist]


class AuthorLinkExtractor(LinkExtractor):
    """
    Extract an author from publisher's weekly list
    """
    def extract_links(self, response):
        # Get link for each author
        links = [
            authors.xpath('./li/a/@href').getall()
            for authors in response.xpath('//*[@id="mw-content-text"]/div/ol')
        ]

        # Flatten, format, and return
        return [Link('https://en.wikipedia.org' + link) for sublist in links for link in sublist]
