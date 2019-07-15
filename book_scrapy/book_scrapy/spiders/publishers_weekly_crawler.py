from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link


class BookLinkExtractor(LinkExtractor):

    def extract_links(self, response):
        # Get each link from the list of books for each year
        links = [
            year.xpath('./li/i/a/@href').getall()
            for year in response.xpath('//*[@id="mw-content-text"]/div/ol')
        ]

        # Flatten, format, and return
        return [Link('https://en.wikipedia.org' + link) for sublist in links for link in sublist]


class PublishersWeeklyCrawler(CrawlSpider):
    """
    Class to get links to bestselling books, as determined by publisher's weekly
    """
    name = 'publishers_weekly'
    start_urls = [
        "https://en.wikipedia.org/wiki/Publishers_Weekly_list_of_bestselling_novels_in_the_United_States_in_the_1980s"
    ]

    rules = (Rule(BookLinkExtractor(), callback='_parse_book'),)

    def _parse_book(self, response):
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
