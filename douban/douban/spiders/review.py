# -*- coding: utf-8 -*-
import scrapy
from douban import db
from douban.items import Review


class ReviewSpider(scrapy.Spider):
    name = 'review'
    allowed_domains = ['douban.com']
    start_urls = ['http://music.douban.com/']

    url_pattern = 'https://music.douban.com/subject/%s/reviews'

    def start_requests(self):
        db.attach(self)
        query = self.session.query(db.Music)
        for music in query.all():
            request = scrapy.Request(self.url_pattern % music.id)
            request.meta['music'] = music
            yield request

    def parse(self, response):
        # review_list = response.xpath('//div[@class="review-list  "]/div')
        # for review in review_list:
        #     reply = review.xpath('.//div[@class="action"]/a[@class="reply"]/text()').extract_first(default='')
        #     reply = reply[0:(len(reply) - 2)]
        #
        #     yield Review(id=review.xpath('@data-cid').extract_first(),
        #                  music_id=response.meta['music'].id,
        #                  title=review.xpath('.//div[@class="main-bd"]/h2/a/text()').extract_first(default=''),
        #                  summary=review.xpath('.//div[@class="short-content"]/text()').extract_first(
        #                      default='').strip(),
        #                  comments=reply,
        #                  useful_count=review.xpath(
        #                      './/div[@class="action"]/a[contains(@class,"up")]/span/text()').extract_first(
        #                      default='0').strip(),
        #                  useless_count=review.xpath(
        #                      './/div[@class="action"]/a[contains(@class,"down")]/span/text()').extract_first(
        #                      default='0').strip())
        #
        count = int(response.xpath('//h1/text()').re_first('([0-9]{1,})'))
        for i in range(0, count, 35):
            request = scrapy.Request(response.url + '?start=' + str(i), callback=self.parse_review)
            request.meta['music'] = response.meta['music']
            yield request

    def parse_review(self, response):
        review_list = response.xpath('//div[@class="review-list  "]/div')
        for review in review_list:
            reply = review.xpath('.//div[@class="action"]/a[@class="reply"]/text()').extract_first(default='')
            reply = reply[0:(len(reply) - 2)]

            yield Review(id=review.xpath('@data-cid').extract_first(),
                         music_id=response.meta['music'].id,
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

            # def parse_review(self, response):
            #     review_list = response.xpath('//div[@class="review-list  "]/div')
            #     for review in review_list:
            #         reply = review.xpath('.//div[@class="action"]/a[@class="reply"]/text()').extract_first(default='')
            #         reply = reply[0:(len(reply) - 2)]
            #
            #         yield Review(id=review.xpath('@data-cid').extract_first(),
            #                      music_id=response.meta['music']['id'],
            #                      title=review.xpath('.//div[@class="main-bd"]/h2/a/text()').extract_first(default=''),
            #                      summary=review.xpath('.//div[@class="short-content"]/text()').extract_first(
            #                          default='').strip(),
            #                      comments=reply,
            #                      useful_count=review.xpath(
            #                          './/div[@class="action"]/a[contains(@class,"up")]/span/text()').extract_first(
            #                          default='0').strip(),
            #                      useless_count=review.xpath(
            #                          './/div[@class="action"]/a[contains(@class,"down")]/span/text()').extract_first(
            #                          default='0').strip())
            #
            #     count = int(response.xpath('//h1/text()').re_first('([0-9]{1,})'))
            #     for i in range(0, count, 35):
            #         request = scrapy.Request(response.url + '?start=' + str(i), callback=self.parse_review)
            #         request.meta['music'] = response.meta['music']
            #         yield request
