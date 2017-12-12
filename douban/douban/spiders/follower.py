# -*- coding: utf-8 -*-
import scrapy
from douban.items import User
from douban import db


class FollowerSpider(scrapy.Spider):
    name = 'follower'
    allowed_domains = ['douban.com']
    start_urls = ['http://music.douban.com/']

    url_pattern_musician = 'https://music.douban.com/musician/%s/fans'

    def start_requests(self):
        db.attach(self)
        for artist in self.session.query(db.Artist).all():
            if artist.douban:
                request = scrapy.Request(self.url_pattern_musician % artist.douban)
                request.meta['mid'] = artist.id
                yield request

    def parse(self, response):
        count = int(response.xpath('//h1/text()').re_first('([0-9]{1,})'))
        # musician = Musician(id=response.meta['mid'],
        #                     follower_count=count)
        #
        # response.meta['musician'] = musician
        # yield musician

        for i in range(0, count, 35):
            request = scrapy.Request(response.url + '?start=' + str(i), callback=self.parse_followers)
            request.meta['mid'] = response.meta['mid']
            yield request

    def parse_followers(self, response):
        obu_list = response.xpath('//dl[@class="obu"]')
        for dl in obu_list:
            uid = dl.xpath('dd/a/@href').extract_first(default='')
            uid = uid[len('https://www.douban.com/people/'):(len(uid) - 1)]
            yield User(id=uid, from_musician=response.meta['mid'])
