# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.items import User
from zhihu.items import Topic


class TopicSpider(scrapy.Spider):
    name = 'topic'
    allowed_domains = ['www.zhihu.com']
    url_pattern = 'https://www.zhihu.com/api/v4/search_v3?t=topic&q=%s&correction=1&offset=0&limit=50'

    keys = [u'陈鸿宇', u'王嘉尔']
    authorization = 'Bearer 2|1:0|10:1511855779|4:z_c0|92:Mi4xSkpyY0JBQUFBQUFBRU1DS0lSNmlDU2NBQUFDRUFsVk5vcU5FV2dDQmxDUUEzNjBfZFpCZ3dyRFBTN3hFdmNITmRR|faa803ec5e0cdeb1b1f667cfadae90a408de6ac5c081fafb9e289da778e011e9'

    def start_requests(self):
        for key in self.keys:
            yield scrapy.Request(self.url_pattern % key, headers={
                'Authorization': self.authorization},
                                 dont_filter=True)

    def parse(self, response):
        if not any(key in response.text for key in self.keys):
            return

        content = json.loads(response.body)
        for data in content['data']:
            if data['object']['type'] == 'topic':
                topic = Topic()
                for key in data['object']:
                    if key in topic.fields:
                        topic[key] = data['object'][key]

                topic['name'] = topic['name'].replace('<em>', '').replace('</em>', '')
                yield topic

                request = scrapy.Request(
                    data['object']['url'].replace('https://api.zhihu.com',
                                                  'https://www.zhihu.com/api/v4') + '/followers?limit=20&offset=0',
                    headers={'Authorization': self.authorization},
                    callback=self.parse_follower)
                request.meta['topic'] = data['object']
                yield request

        if not content['paging']['is_end']:
            yield scrapy.Request(
                content['paging']['next'].replace('http://www.zhihu.com',
                                                  'https://www.zhihu.com/api/v4'),
                headers={'Authorization': self.authorization})

    def parse_follower(self, response):
        content = json.loads(response.body)
        for data in content['data']:
            url_pattern = 'https://www.zhihu.com/api/v4/members/%s?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
            request = scrapy.Request(
                url_pattern % data['id'],
                headers={'Authorization': self.authorization},
                callback=self.parse_user)
            request.meta['topic'] = response.meta['topic']
            yield request

        if not content['paging']['is_end']:
            request = scrapy.Request(
                content['paging']['next'].replace('http://',
                                                  'https://'),
                headers={'Authorization': self.authorization},
                callback=self.parse_follower)

            request.meta['topic'] = response.meta['topic']
            yield request

    def parse_user(self, response):
        content = json.loads(response.body)
        user = User()
        for key in content:
            if key in user.fields and key in content:
                user[key] = content[key]

        user['from_topic'] = response.meta['topic']['id']
        return user