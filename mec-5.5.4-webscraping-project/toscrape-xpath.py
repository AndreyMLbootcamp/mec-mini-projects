import scrapy


class QuotesSpider(scrapy.Spider):
    name = "toscrape-xpath"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):

        for n_, quote in enumerate(response.xpath("//div[@class='quote']"), 1):
            yield {
                'text': str(quote.xpath(f"//div[@class='quote'][{n_}]/span[@class='text']/text()").extract()).encode("ascii", "ignore").decode(),
                    # .replace('\u201c', '').replace('"', '').replace('\u201d',''),
                'author': quote.xpath(f"//div[@class='quote'][{n_}]/span/small[@class='author']/text()").extract(),
                'tags': quote.xpath(f'//div[@class="quote"][{n_}]/div/a/text()').extract(),
            }

        # next_page = response.xpath('//ul[@class="pager"]/li/a').get()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
