import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):

        for n_, quote in enumerate(response.css('div.quote'), 1):
            yield {
                'text': str(quote.css('span.text::text').get()).encode("ascii", "ignore").decode(),
                'author': quote.css('span small::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)