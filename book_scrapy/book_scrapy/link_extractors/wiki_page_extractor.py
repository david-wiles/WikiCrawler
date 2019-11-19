from scrapy.link import Link
from scrapy.linkextractors import LinkExtractor


class WikiPostExtractor(LinkExtractor):

    def extract_links(self, response):
        wiki_pages = []

        links = response.xpath("//a/@href").getall()
        for link in links:
            if link[:6] == "/wiki/" and ":" not in link:
                wiki_pages.append(Link('https://en.wikipedia.org' + link))

        return wiki_pages


class WikiTopicExtractor(LinkExtractor):

    def extract_links(self, response):
        wiki_categories = []

        links = response.xpath("//a/@href").getall()
        for link in links:
            if link[:15] == "/wiki/Category:":
                wiki_categories.append(Link('https://en.wikipedia.org' + link))

        return wiki_categories