# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu import db
from zhihu.items import User


class TopicFollowerSpider(scrapy.Spider):
    name = 'topic_follower'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    authorization = 'Bearer 2|1:0|10:1511855779|4:z_c0|92:Mi4xSkpyY0JBQUFBQUFBRU1DS0lSNmlDU2NBQUFDRUFsVk5vcU5FV2dDQmxDUUEzNjBfZFpCZ3dyRFBTN3hFdmNITmRR|faa803ec5e0cdeb1b1f667cfadae90a408de6ac5c081fafb9e289da778e011e9'

    def start_requests(self):
        db.attach(self)
        query = self.session.query(db.Topic)
        for topic in query.all():
            request = scrapy.Request('https://www.zhihu.com/api/v4/topics/%s/followers?limit=20&offset=0' % topic.id,
                                     headers={'Authorization': self.authorization})
            request.meta['topic'] = topic
            yield request

    def parse(self, response):
        content = json.loads(response.body.decode('utf-8'))
        for data in content['data']:
            user = User()
            for key in data:
                if key in user.fields:
                    user[key] = data[key]

            user['from_topic'] = response.meta['topic'].id
            yield user

        if not content['paging']['is_end']:
            request = scrapy.Request(
                content['paging']['next'].replace('http://',
                                                  'https://'),
                headers={'Authorization': self.authorization})

            request.meta['topic'] = response.meta['topic']
            yield request
