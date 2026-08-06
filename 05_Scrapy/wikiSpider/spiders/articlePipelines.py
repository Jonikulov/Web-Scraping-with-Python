from typing import ClassVar

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from wikiSpider.items import Article


class ArticleSpider(CrawlSpider):
    name = "articlePipelines"
    allowed_domains: ClassVar[list[str]] = ["wikipedia.org"]
    start_urls: ClassVar[list[str]] = [
        "https://en.wikipedia.org/wiki/Benevolent_dictator_for_life"
    ]
    rules: ClassVar[list[Rule]] = [
        Rule(
            LinkExtractor(allow=r"^(https?://en\.wikipedia\.org)?(/wiki/)[^:]+$"),
            callback="parse_items",
            follow=True,
        )
    ]

    def parse_items(self, response):
        article = Article()
        article["url"] = response.url
        article["title"] = response.xpath("//h1//text()").get()
        article["text"] = response.xpath(
            "//div[@id='mw-content-text']//text()"
        ).getall()
        article["last_updated"] = response.xpath(
            "//li[@id='footer-info-lastmod']/text()"
        ).get()
        yield article
