from scrapy.spiders import Spider


class LinkExtractorSpider(Spider):
    name = "LinkExtractor"

    start_urls =[
        'file:///home/david/Desktop/Publishers%20Weekly%20list%20of%20bestselling%20novels%20in%20the%20United%20States%20in%20the%201980s%20-%20Wikipedia.html'
    ]

    def parse(self, response):
        # Get link for each author
        links = [
            authors.xpath('./li/a/@href').getall()
            for authors in response.xpath('//*[@id="mw-content-text"]/div/ol')
        ]

        # Flatten, format, and return
        yield {'links' : [('https://en.wikipedia.org' + link) for sublist in links for link in sublist]}
