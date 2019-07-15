from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
from ..items import BookItem, AuthorItem
import re


class BookLinkExtractor(LinkExtractor):

    def extract_links(self, response):
        # Get each link from the list of books for each year
        links = [
            books.xpath('./li/i/a/@href').getall()
            for books in response.xpath('//*[@id="mw-content-text"]/div/ol')
        ]

        # Flatten, format, and return
        return [Link('https://en.wikipedia.org' + link) for sublist in links for link in sublist]


class AuthorLinkExtractor(LinkExtractor):

    def extract_links(self, response):
        # Get link for each author
        links = [
            authors.xpath('./li/a/@href').getall()
            for authors in response.xpath('//*[@id="mw-content-text"]/div/ol')
        ]

        # Flatten, format, and return
        return [Link('https://en.wikipedia.org' + link) for sublist in links for link in sublist]


class PublishersWeeklyCrawler(CrawlSpider):
    """
    Class to get links to bestselling books, as determined by publisher's weekly
    """
    name = 'PublishersWeeklyCrawler'
    start_urls = [
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1980s"
    ]

    rules = (Rule(BookLinkExtractor(), callback='_parse_book'),
             Rule(AuthorLinkExtractor(), callback='_parse_author'))

    def _parse_book(self, response):
        book = BookItem()

        table_rows = response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        book['url'] = response.url

        # Title
        book['title'] = response.xpath('string(//h1[@id="firstHeading"])').get()

        # Place unknown values into a list
        unknown = []

        # Details from infobox
        for tr in table_rows:
            # Get main image from the article, if it exists
            if tr.xpath('./td/a[@class="image"]/@href'):
                book['image'] = tr.xpath('./td/a[@class="image"]/@href').get()
            else:
                data = tr.xpath('string(./td)').get()
                title = tr.xpath('./th/text()').get()

                try:
                    if title is not None:
                        new_title = re.sub(r' ', '_', title.lower())
                        book[new_title] = data
                except (AttributeError, KeyError):
                    unknown.append(data)

        # Description from top section in article
        book['description'] = "".join([
            p.xpath('string()').get()
            for p in response.xpath('//*[@id="toc"]/preceding-sibling::p')
        ])

        book['unknown'] = unknown

        yield book

    def _parse_author(self, response):
        author = AuthorItem()

        table_rows = response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        author['url'] = response.url

        # Title
        author['name'] = response.xpath('string(//h1[@id="firstHeading"])').get()

        # Place unknown values into a list
        unknown = []

        # Details from infobox
        for tr in table_rows:
            # Get main image from the article, if it exists
            if tr.xpath('./td/a[@class="image"]/@href'):
                author['image'] = tr.xpath('./td/a[@class="image"]/@href').get()
            else:
                data = tr.xpath('string(./td)').get()
                title = tr.xpath('./th/text()').get()

                try:
                    if title is not None:
                        new_title = re.sub(r' ', '_', title.lower())
                        author[new_title] = data
                except (AttributeError, KeyError):
                    unknown.append(data)

        # Description from top section in article
        author['description'] = "".join([
            p.xpath('string()').get()
            for p in response.xpath('//*[@id="toc"]/preceding-sibling::p')
        ])

        author['unknown'] = unknown

        yield author
