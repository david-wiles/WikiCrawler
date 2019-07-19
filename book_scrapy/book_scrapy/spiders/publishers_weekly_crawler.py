from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
from ..items import BookItem, AuthorItem
import json
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
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1980s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_2000s",
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_2010s"
    ]

    rules = (Rule(BookLinkExtractor(), callback='_parse_book'),
             Rule(AuthorLinkExtractor(), callback='_parse_author'))

    def _parse_book(self, response):
        item = BookItem()

        table_rows = response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        item['url'] = response.url

        # Title
        item['title'] = response.xpath('string(//h1[@id="firstHeading"])').get()

        # Place unknown values into a list
        other = {}
        unknown = []

        # Details from infobox
        for tr in table_rows:
            # Get main image from the article, if it exists
            if tr.xpath('./td/a[@class="image"]/@href'):
                item['image'] = tr.xpath('./td/a[@class="image"]/@href').get()
            else:
                data = tr.xpath('string(./td)').get()
                title = tr.xpath('./th/text()').get()

                try:
                    if title is not None:
                        new_title = re.sub(r' ', '_', title.lower())
                        item[new_title] = data
                except (KeyError):
                    other[new_title] = data
                except (AttributeError):
                    unknown.append(data)

        # Description from top section in article
        item['description'] = "".join([
            p.xpath('string()').get()
            for p in response.xpath('//*[@id="toc"]/preceding-sibling::p')
        ])

        other['unknown'] = unknown
        item['other'] = json.dumps(other)

        yield item

    def _parse_author(self, response):
        item = AuthorItem()

        table_rows = response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        item['url'] = response.url

        # Title
        item['name'] = response.xpath('string(//h1[@id="firstHeading"])').get()

        # Place unknown values into a list
        other = {}
        unknown = []

        # Details from infobox
        for tr in table_rows:
            # Get main image from the article, if it exists
            if tr.xpath('./td/a[@class="image"]/@href'):
                item['image'] = tr.xpath('./td/a[@class="image"]/@href').get()
            else:
                data = tr.xpath('string(./td)').get()
                title = tr.xpath('./th/text()').get()

                try:
                    if title is not None:
                        new_title = re.sub(r' ', '_', title.lower())
                        item[new_title] = data
                except (KeyError):
                    other[new_title] = data
                except (AttributeError):
                    unknown.append(data)

        # Description from top section in article
        item['description'] = "".join([
            p.xpath('string()').get()
            for p in response.xpath('//*[@id="toc"]/preceding-sibling::p')
        ])

        other['unknown'] = unknown
        item['other'] = json.dumps(other)

        yield item
