# -*- coding: utf-8 -*-
import scrapy
import re
import json
from banner.items import Song

from banner.items import Album


class NeteasepcSpider(scrapy.Spider):
    name = 'neteasepc'
    allowed_domains = ['music.163.com']
    start_urls = ['http://music.163.com/discover']

    def parse(self, response):
        p1 = re.compile(r'window.Gbanners.*?;', re.DOTALL)
        p2 = re.compile(r'\[.*\]', re.DOTALL)

        banners_json_text = p2.findall(p1.findall(response.text)[0])[0]
        banners_json_text = banners_json_text.replace('picUrl', '"picUrl"'). \
            replace('url', '"url"'). \
            replace('targetId', '"targetId"'). \
            replace('backgroundUrl', '"backgroundUrl"'). \
            replace('targetType', '"targetType"'). \
            replace('monitorType', '"monitorType"'). \
            replace('monitorImpress', '"monitorImpress"'). \
            replace('monitorClick', '"monitorClick"')

        # self.log(banners_json_text)
        banners = json.loads(banners_json_text)
        for banner in banners:
            if banner['targetType'] == '1':
                # song
                yield scrapy.Request('http://music.163.com' + banner['url'], self.parse_song)
            elif banner['targetType'] == '10':
                # album
                yield scrapy.Request('http://music.163.com' + banner['url'], self.parse_album)
            elif banner['targetType'] == '1004':
                # mv
                self.log(banner['url'])
            else:
                # topic
                self.log(banner['url'])

    def parse_song(self, response):
        cnt = response.xpath('//div[@class="cnt"]')
        des = cnt.xpath('.//p[contains(@class,"des") and contains(@class,"s-fc4")]')
        return Song(name=cnt.xpath('.//em[@class="f-ff2"]/text()').extract_first(default=''),
                    artists=des.xpath('.//span/@title').extract_first(default=''),
                    album=des.xpath('a/text()').extract_first(default=''),
                    href=response.url)

    def parse_album(self, response):
        cnt = response.xpath('//div[@class="cnt"]')
        return Album(name=cnt.xpath('.//h2[@class="f-ff2"]/text()').extract_first(default=''),
                     artists=cnt.xpath('.//p[@class="intr"]/span/@title').extract_first(default=''),
                     href=response.url)
