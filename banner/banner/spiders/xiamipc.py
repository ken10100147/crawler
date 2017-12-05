# -*- coding: utf-8 -*-
import scrapy
from banner.items import Song

from banner.items import Album


class XiamipcSpider(scrapy.Spider):
    name = 'xiamipc'
    allowed_domains = ['www.xiami.com']
    start_urls = ['http://www.xiami.com/']

    def parse(self, response):
        for href in response.xpath('//div[@id="slider"]/div[@class="content"]/div[@class="item"]/a/@href').extract():
            if 'song' in href:
                yield scrapy.Request(href, self.parse_song)
            elif 'album' in href:
                yield scrapy.Request(href, self.parse_album)
            elif 'mv' in href:
                self.log('href:' + href)
            else:
                self.log('href:' + href)

    def parse_song(self, response):
        return Song(name=response.xpath('//meta[@property="og:title"]/@content').extract_first(default=''),
                    artists=response.xpath('//meta[@property="og:music:artist"]/@content').extract_first(default=''),
                    album=response.xpath('//meta[@property="og:music:album"]/@content').extract_first(default=''),
                    href=response.url)

    def parse_album(self, response):
        return Album(name=response.xpath('//div[@id="page"]//div[@id="title"]/h1/text()').extract_first(default=''),
                     artists=response.xpath('//meta[@property="og:music:artist"]/@content').extract_first(default=''),
                     href=response.url)
