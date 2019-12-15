# -*- coding: utf-8 -*-
import scrapy


class DealsSpider(scrapy.Spider):
    name = 'deals'
    allowed_domains = ['flipkart.com']
    start_urls = ['https://www.flipkart.com']

    def parse(self, response):
         deals=response.xpath('//*[@class="_2Umlwf"]//a/@href').extract_first() #get view_all link
         return scrapy.Request(deals,callback = self.parse_deals)

    def parse_deals(self,response):                                             #get product list url
        product_list=response.xpath('//*[@class="_1B6Okp"]//a/@href').extract()
        for product in product_list:
            absolute_product_url = response.urljoin(product)
            #yield{'url':absolute_product_url}
            yield scrapy.Request(absolute_product_url,
                    callback=self.parse_deals_details)

    def parse_deals_details(self,response):
        details=response.xpath('//*[@class="_3O0U0u"]//a/@href').extract()
        for detail in details:
            detail_url=response.urljoin(detail)
            yield scrapy.Request(detail_url,
                    callback=self.parse_product_details,
                    meta={'Link':detail_url})

    def parse_product_details(self,response):
        name=response.xpath('//*[@class="_35KyD6"]/text()').extract_first()
        ratings= response.xpath('//*[@class="hGSR34"]/text() |'
                    '//*[@class="hGSR34 bqXGTW"]/text()').extract_first()
        price=response.xpath('//*[@class="_1vC4OE _3qQ9m1"]/text()').extract_first()
        detail_url = response.meta['Link']

        #price=price.replace('?',' ')

        yield{'Name of Product':name,
                'Ratings':ratings,
                'Price':price,
                'Link':detail_url}
