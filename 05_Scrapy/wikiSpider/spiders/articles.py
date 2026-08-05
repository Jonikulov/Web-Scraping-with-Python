from typing import ClassVar

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ArticleSpider(CrawlSpider):
    name = "articles"
    allowed_domains: ClassVar[list[str]] = ["wikipedia.org"]
    start_urls: ClassVar[list[str]] = [
        "https://en.wikipedia.org/wiki/Benevolent_dictator_for_life"
    ]
    rules: ClassVar[list[Rule]] = [
        Rule(
            LinkExtractor(allow=r"https?://en\.wikipedia\.org/.+"),
            callback="parse_items",
            follow=True,
        )
    ]

    def parse_items(self, response):
        title = response.xpath("//h1//text()").get()
        text = response.xpath('//div[@id="mw-content-text"]//text()').getall()
        last_updated = response.xpath('//li[@id="footer-info-lastmod"]/text()').get()
        last_updated = last_updated.replace("This page was last edited on ", "")
        print(f"URL is: {response.url}")
        print(f"Title is: {title} ")
        print(f"Text is: {text}")
        print(f"Last updated: {last_updated}")

        yield {
            "title": title,
            "url": response.url,
            "lastUpdated": last_updated,
            "text": text,
        }
