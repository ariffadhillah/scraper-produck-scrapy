import scrapy

class houzzSpider(scrapy.Spider):
    name = 'houzz'
    start_urls = ['https://www.houzz.com/professionals/interior-designer']

    def parse(self, response):
        for products in response.css('div.hz-pro-search-result'):
            try:
                yield {
                    'Name': products.css('a').find('span.header-5.text-unbold.mlm::text').get(),
                    'Start': products.css('div.hz-pro-search-result__name-rating').find('span.hz-star-rate__rating-number::text').get(),
                    'Reviews': products.css('div.hz-pro-search-result__name-rating').find('span.hz-star-rate__review-string::text').get(),
                    'Call': products.css('div.hz-pro-search-result__right-info__contact-info').find('span.hz-pro-search-result__contact-info__cover::text').get(),

                    # 'price': products.css('span.price::text').get().replace('£',''),
                    'link': products.css('a').attrib['href'],
                }
            except:
                yield {
                    'name': products.css('span.header-5.text-unbold.mlm::text').get(),
                    'start': products.css('span.hz-star-rate__rating-number::text').get(),
                    'Reviews': products.css('span.hz-star-rate__review-string::text').get(),
                    'Call': products.css('span.hz-pro-search-result__contact-info__cover::text').get(),

                    # 'price': 'sold out',
                    'link': products.css('a').attrib['href'],
                }
        next_page = response.css('a.hz-pagination-link.hz-pagination-link--next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

