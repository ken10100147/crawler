# -*- coding: utf-8 -*-
import scrapy
import json
import artist
from douban.items import Music
from douban.items import Review


class ReviewSpider(scrapy.Spider):
    name = 'review'
    allowed_domains = ['douban.com']
    start_urls = ['http://music.douban.com/']

    url_pattern_search = 'https://api.douban.com/v2/music/search?q=%s'

    def start_requests(self):
        for item in artist.all():
            request = scrapy.Request(self.url_pattern_search % item.artist_name)
            request.meta['artist'] = item
            yield request

    def parse(self, response):
        content = json.loads(response.body)
        for music in content['musics']:
            if 'author' in music:
                if any(response.meta['artist'].artist_name == author['name'] for author in music['author']):
                    item = Music()
                    for key in item.fields:
                        if key in music:
                            item[key] = music[key]
                    item['artist_id'] = response.meta['artist'].id
                    yield item

                    request = scrapy.Request(music['alt'] + 'reviews', callback=self.parse_review)
                    request.meta['music'] = item
                    yield request

    def parse_review(self, response):
        review_list = response.xpath('//div[@class="review-list  "]/div')
        for review in review_list:
            reply = review.xpath('.//div[@class="action"]/a[@class="reply"]/text()').extract_first(default='')
            reply = reply[0:(len(reply) - 2)]

            yield Review(id=review.xpath('@data-cid').extract_first(),
                         music_id=response.meta['music']['id'],
                         title=review.xpath('.//div[@class="main-bd"]/h2/a/text()').extract_first(default=''),
                         summary=review.xpath('.//div[@class="short-content"]/text()').extract_first(
                             default='').strip(),
                         comments=reply,
                         useful_count=review.xpath(
                             './/div[@class="action"]/a[contains(@class,"up")]/span/text()').extract_first(
                             default='0').strip(),
                         useless_count=review.xpath(
                             './/div[@class="action"]/a[contains(@class,"down")]/span/text()').extract_first(
                             default='0').strip())

        count = int(response.xpath('//h1/text()').re_first('([0-9]{1,})'))
        for i in range(0, count, 35):
            request = scrapy.Request(response.url + '?start=' + str(i), callback=self.parse_review)
            request.meta['music'] = response.meta['music']
            yield request

        # if len(review_list) > 0:
        #     if 'start=' in response.url:
        #         idx = response.url.index('?start=')
        #         request = scrapy.Request(response.url[0:(idx - 1)] + '?start=' + str(
        #             int(response.url[(idx + len('?start=')):len(response.url)]) + 35),
        #                                  callback=self.parse_review)
        #         request.meta['music'] = response.meta['music']
        #         yield request
        #     else:
        #         request = scrapy.Request(response.url + '?start=35', callback=self.parse_review)
        #         request.meta['music'] = response.meta['music']
        #         yield request
