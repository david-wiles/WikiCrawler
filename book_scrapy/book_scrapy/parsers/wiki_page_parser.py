from ..items import BookItem, AuthorItem
import json
import re


class WikiPageParser(object):

    def __init__(self, response):
        self.response = response

    def parse_book(self):
        item = BookItem()

        table_rows = self.response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        item['url'] = self.response.url

        # Title
        item['title'] = self.response.xpath('string(//h1[@id="firstHeading"])').get()

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
            for p in self.response
                .css('div.mw-parser-output')
                .xpath(f'./p[{index}]')
        ])

        other['unknown'] = unknown
        item['other'] = json.dumps(other)

        return item

    def parse_author(self):
        item = AuthorItem()

        table_rows = self.response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        item['url'] = self.response.url

        # Title
        item['name'] = self.response.xpath('string(//h1[@id="firstHeading"])').get()

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
            for p in self.response
                .css('div.mw-parser-output')
                .xpath(f'./p[{index}]')
        ])

        other['unknown'] = unknown
        item['other'] = json.dumps(other)

        return item
