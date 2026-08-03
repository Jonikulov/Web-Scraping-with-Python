import scrapy

class ArticleSpider(scrapy.Spider):
    name="article"
    # allowed_domains = ["en.wikipedia.org"]

    async def start(self):
        urls = [
            "https://en.wikipedia.org/wiki/Python_(programming_language)",
            "https://en.wikipedia.org/wiki/Functional_programming",
            "https://en.wikipedia.org/wiki/Monty_Python",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        title = response.css("h1 ::text").extract_first()
        print(f"URL is: {response.url}")
        print(f"Title is: {title}")

        yield {"title": title, "url": response.url}
