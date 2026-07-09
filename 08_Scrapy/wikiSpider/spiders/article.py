import scrapy

class ArticleSpider(scrapy.Spider):
    name = "article"
    allowed_domains = ["en.wikipedia.org"]

    def start_requests(self):
        # If this doesn't print, Scrapy is NOT running this file.
        print("\n" + "="*50)
        print("🚨 START_REQUESTS IS ACTUALLY RUNNING! 🚨")
        print("="*50 + "\n")
        
        urls = ["https://en.wikipedia.org/wiki/Programming_language"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print("\n" + "="*50)
        print(f"✅ SUCCESS! REACHED PARSE METHOD: {response.url}")
        print("="*50 + "\n")
        
        title = response.css("h1::text").get()
        yield {"title": title, "url": response.url}
