from scrapy import Spider


class WikiBookSpider(Spider):
    """
    Spider to get basic information about a book from a wikipedia article
    """
    name = 'wikibook'

    start_urls = ['file:///home/david/Desktop/Mockingbird%20-%20Wikipedia.html']

    def parse(self, response):
        table_rows = response.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr')

        parsed_page = {}
        parsed_page['image'] = table_rows[0].xpath('./td/a/@href').get()

        for tr in table_rows[1:]:
            data = tr.xpath('./td/a/text()').get() or tr.xpath('./td/text()').get()
            parsed_page[tr.xpath('./th/text()').get()] = data

        yield parsed_page
