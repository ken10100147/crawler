# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu import db
from zhihu.items import Answer


class AnswerSpider(scrapy.Spider):
    name = 'answer'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    url_pattern = 'https://www.zhihu.com/api/v4/questions/%s/answers?limit=20&offset=0&include=data[*].is_normal,is_sticky,collapsed_by,suggest_edit,comment_count,collapsed_counts,reviewing_comments_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[].author.is_blocking,is_blocked,is_followed,voteup_count,message_thread_token,badge[?(type=best_answerer)].topics'
    authorization = 'Bearer 2|1:0|10:1511855779|4:z_c0|92:Mi4xSkpyY0JBQUFBQUFBRU1DS0lSNmlDU2NBQUFDRUFsVk5vcU5FV2dDQmxDUUEzNjBfZFpCZ3dyRFBTN3hFdmNITmRR|faa803ec5e0cdeb1b1f667cfadae90a408de6ac5c081fafb9e289da778e011e9'

    def start_requests(self):
        db.attach(self)
        query = self.session.query(db.Question)
        for question in query.all():
            yield scrapy.Request(self.url_pattern % question.id,
                                 headers={'Authorization': self.authorization})

    def parse(self, response):
        content = json.loads(response.body.decode('utf-8'))
        for data in content['data']:
            yield Answer(id=data['id'],
                         question_id=data['question']['id'],
                         voteup_count=data['voteup_count'],
                         comment_count=data['comment_count'],
                         content=data['content'])

        if not content['paging']['is_end']:
            yield scrapy.Request(
                content['paging']['next'].replace('http://', 'https://'),
                headers={'Authorization': self.authorization})
