# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu import db
from zhihu.items import User


class UserSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    url_pattern = 'https://www.zhihu.com/api/v4/members/%s?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_force_renamed,is_bind_sina,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'
    authorization = 'Bearer 2|1:0|10:1511855779|4:z_c0|92:Mi4xSkpyY0JBQUFBQUFBRU1DS0lSNmlDU2NBQUFDRUFsVk5vcU5FV2dDQmxDUUEzNjBfZFpCZ3dyRFBTN3hFdmNITmRR|faa803ec5e0cdeb1b1f667cfadae90a408de6ac5c081fafb9e289da778e011e9'

    def start_requests(self):
        db.attach(self)
        query = self.session.query(db.User).filter(db.User.channel == db.CHANNEL)
        for user in query.all():
            if not any(user.business is None, user.educations is None, user.employments is None):
                yield scrapy.Request(self.url_pattern % user.id,
                                     headers={'Authorization': self.authorization})

    def parse(self, response):
        content = json.loads(response.body.decode('utf-8'))
        user = User()
        for key in content:
            if key in user.fields:
                user[key] = content[key]

        return user
