# -*- coding: utf-8 -*-
import scrapy


class KuwomSpider(scrapy.Spider):
    name = 'kuwom'
    allowed_domains = ['m.kuwo.cn']
    start_urls = ['http://m.kuwo.cn']

    def parse(self, response):
        for href in response.xpath('//div[@class="banner"]//a/@href').extract():
            # mv
            self.log('href:' + href)
