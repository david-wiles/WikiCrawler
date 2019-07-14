from scrapy import Spider


class WikiPageSpider(Spider):
    """
    Spider to get basic information about a book from a wikipedia article
    """
    name = 'wikipage'

    start_urls = ['file:///home/david/Desktop/Mockingbird%20-%20Wikipedia.html']

    def parse(self, response):
        parsed_page = {}
        table_rows = response.css('table.infobox.vcard').xpath('./tbody/tr')

        # url (For reference and to prevent duplicates)
        parsed_page['url'] = response.url

        # Title
        parsed_page['title'] = response.xpath('//h1[@id="firstHeading"]/i/text()').get()

        # Image from article, if exists
        parsed_page['image'] = table_rows[0].xpath('./td/a/@href').get()

        # Details from infobox
        for tr in table_rows[1:]:
            data = tr.xpath('./td/a/text()').get() or tr.xpath('./td/text()').get()
            parsed_page[tr.xpath('./th/text()').get()] = data

        # Description from top section in article
        parsed_page['description'] = "".join([
            p.xpath('string()').get()
            for p in response.xpath('//*[@id="toc"]/preceding-sibling::p')
        ])

        yield parsed_page
