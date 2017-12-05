# -*- coding: utf-8 -*-
import scrapy
from banner.items import Album


class KugoupcSpider(scrapy.Spider):
    name = 'kugoupc'
    allowed_domains = ['www.kugou.com']
    start_urls = ['http://www.kugou.com/']

    def parse(self, response):
        for href in response.xpath('//div[@class="banner"]//a/@href').extract():
            if 'album' in href:
                yield scrapy.Request(href, self.parse_album)
            else:
                # mv
                self.log('href:' + href)

    def parse_album(self, response):
        details = response.xpath('//p[@class="detail"]').re(r'/span>(.*?)<br')
        return Album(name=details[0],
                     artists=details[1],

                     href=response.url)
