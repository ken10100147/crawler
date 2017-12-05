# -*- coding: utf-8 -*-
import scrapy
import artist
from douban.items import Musician
from douban.items import User


class FollowerSpider(scrapy.Spider):
    name = 'follower'
    allowed_domains = ['douban.com']
    start_urls = ['http://music.douban.com/']

    url_pattern_musician = 'https://music.douban.com/musician/%s/fans'

    def start_requests(self):
        for item in artist.all():
            if item.douban:
                request = scrapy.Request(self.url_pattern_musician % item.douban)
                request.meta['mid'] = item.douban
                yield request

    def parse(self, response):
        musician = Musician(id=response.meta['mid'],
                            follower_count=response.xpath('//h1/text()').re_first('([0-9]{1,})'))

        response.meta['musician'] = musician
        yield musician

        for request in self.parse_followers(response):
            yield request

    def parse_followers(self, response):
        obu_list = response.xpath('//dl[@class="obu"]')
        for dl in obu_list:
            uid = dl.xpath('dd/a/@href').extract_first(default='')
            uid = uid[len('https://www.douban.com/people/'):(len(uid) - 1)]
            yield User(id=uid, from_musician=response.meta['musician']['id'])

        if len(obu_list) > 0:
            if 'start=' in response.url:
                idx = response.url.index('?start=')
                request = scrapy.Request(response.url[0:idx] + '?start=' + str(
                    int(response.url[(idx + len('?start=')):len(response.url)]) + 35),
                                         callback=self.parse_followers)
                request.meta['musician'] = response.meta['musician']
                yield request
            else:
                request = scrapy.Request(response.url + '?start=35', callback=self.parse_followers)
                request.meta['musician'] = response.meta['musician']
                yield request
