from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
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
             Rule(AuthorLinkExtractor(), callback= '_parse_author'))

    def _parse_book(self, response):
        parsed_page = {}
        table_rows = response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        parsed_page['URL'] = response.url

        # Title
        parsed_page['Title'] = response.xpath('string(//h1[@id="firstHeading"])').get()

        # Details from infobox
        for tr in table_rows:
            # Get main image from the article, if it exists
            if (tr.xpath('./td/a[@class="image"]/@href')):
                parsed_page['Image'] = tr.xpath('./td/a[@class="image"]/@href').get()
            else:
                data = tr.xpath('string(./td)').get()
                title = tr.xpath('./th/text()').get()

                parsed_page[title] = data

        # Description from top section in article
        parsed_page['description'] = "".join([
            p.xpath('string()').get()
            for p in response.xpath('//*[@id="toc"]/preceding-sibling::p')
        ])

        yield parsed_page

    def _parse_author(self, response):
        parsed_page = {}
        table_rows = response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        parsed_page['URL'] = response.url

        # Title
        parsed_page['Name'] = response.xpath('string(//h1[@id="firstHeading"])').get()

        # Details from infobox
        for tr in table_rows:
            # Get main image from the article, if it exists
            if (tr.xpath('./td/a[@class="image"]/@href')):
                parsed_page['Image'] = tr.xpath('./td/a[@class="image"]/@href').get()
            else:
                data = tr.xpath('string(./td)').get()
                title = tr.xpath('./th/text()').get()

                parsed_page[title] = data

        # Description from top section in article
        parsed_page['description'] = "".join([
            p.xpath('string()').get()
            for p in response.xpath('//*[@id="toc"]/preceding-sibling::p')
        ])

        yield parsed_page
