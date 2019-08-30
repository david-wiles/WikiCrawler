from scrapy.spiders import Spider


class TestSpider(Spider):

    name = "TestSpider"

    start_urls = ["file:///home/david/Documents/scrapes/Supercomputer%20-%20Wikipedia.html"]

    def parse(self, response):
        lists = response.css('div.mw-parser-output').xpath('./ul/li/a/@href').getall()
        yield {'list': [('https://en.wikipedia.org' + link) for link in lists]}
