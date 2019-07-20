from scrapy.spiders import Spider
from ..items import BookItem, AuthorItem
import json
import re


class WikiBookSpider(Spider):
    """
    Spider to get basic information about a book from a wikipedia article
    """
    name = 'WikiBookSpider'

    start_urls = ["file:///home/david/Desktop/Twelve%20Sharp%20-%20Wikipedia.html"]

    def parse(self, response):
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
                title = tr.xpath('string(./th)').get()

                try:
                    if title is not None:
                        sanitized_title = re.sub(u'[ \u00a0]','_', title.lower())
                        sanitized_data = re.sub(u'\u00a0', ' ', data.strip())

                        if sanitized_title == 'genres': sanitized_title = 'genre'
                        if sanitized_title == 'publication_date': sanitized_title = 'published'

                        item[sanitized_title] = sanitized_data

                except (KeyError):
                    other[sanitized_title] = sanitized_data
                except (AttributeError):
                    unknown.append(sanitized_data)

        # Description from top section in article
        item['description'] = "".join([
            p.xpath('string()').get()
            for index in range(10)
            for p in response
                .css('div.mw-parser-output')
                .xpath(f'./p[{index}]')
        ])

        other['unknown'] = unknown
        item['other'] = json.dumps(other)

        yield item


class WikiAuthorSpider(Spider):
    """
    Spider to get basic information about a book from a wikipedia article
    """
    name = 'WikiAuthorSpider'

    start_urls = ["file:///home/david/Desktop/James%20A.%20Michener%20-%20Wikipedia.html"]

    def parse(self, response):
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
                title = tr.xpath('string(./th)').get()

                try:
                    if title is not None:
                        sanitized_title = re.sub(u'[ \u00a0]','_', title.lower())
                        sanitized_data = re.sub(u'\u00a0', ' ', data.strip())

                        if sanitized_title == 'genres': sanitized_title = 'genre'

                        item[sanitized_title] = sanitized_data

                except (KeyError):
                    other[sanitized_title] = sanitized_data
                except (AttributeError):
                    # What caused this error?
                    unknown.append(sanitized_data)

        # Description from top section in article
        item['description'] = "".join([
            p.xpath('string()').get()
            for index in range(10)
            for p in response
                .css('div.mw-parser-output')
                .xpath(f'./p[{index}]')
        ])

        other['unknown'] = unknown
        item['other'] = json.dumps(other)

        yield item
