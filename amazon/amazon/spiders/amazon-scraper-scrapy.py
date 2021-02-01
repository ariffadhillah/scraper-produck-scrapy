import scrapy

class whiskeySpider(scrapy.Spider):
    name = 'amazon'
    start_urls = ['https://www.amazon.com/s?k=amazonbasics']

    def parse(self, response):
        for products in response.css('div.product-item-info'):
            try:
                yield {
                    'name': products.css('a.product-item-link::text').get(),
                    'price': products.css('span.price::text').get().replace('£',''),
                    'link': products.css('a.product-item-link').attrib['href'],
                }
            except:
                yield {
                    'name': products.css('a.product-item-link::text').get(),
                    'price': 'sold out',
                    'link': products.css('a.product-item-link').attrib['href'],
                }
        next_page = response.css('a.action.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


