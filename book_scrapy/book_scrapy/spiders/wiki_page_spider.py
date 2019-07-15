from scrapy.spiders import Spider
import re


class WikiPageSpider(Spider):
    """
    Spider to get basic information about a book from a wikipedia article
    """
    name = 'WikiPageSpider'

    start_urls = ["file:///home/david/Desktop/James%20A.%20Michener%20-%20Wikipedia.html",
                  'file:///home/david/Desktop/Mockingbird%20-%20Wikipedia.html']

    def parse(self, response):
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
