# -*- coding: utf-8 -*-
import scrapy
import json
from zhihu.spiders import artist
from zhihu.items import Answer, Question


class GeneralSearchSpider(scrapy.Spider):
    name = 'generalsearch'
    allowed_domains = ['www.zhihu.com']
    url_pattern = 'https://www.zhihu.com/api/v4/search_v3?t=general&q=%s&correction=1&offset=0&limit=50'

    authorization = 'Bearer 2|1:0|10:1511855779|4:z_c0|92:Mi4xSkpyY0JBQUFBQUFBRU1DS0lSNmlDU2NBQUFDRUFsVk5vcU5FV2dDQmxDUUEzNjBfZFpCZ3dyRFBTN3hFdmNITmRR|faa803ec5e0cdeb1b1f667cfadae90a408de6ac5c081fafb9e289da778e011e9'

    def start_requests(self):
        for item in artist.all():
            request = scrapy.Request(self.url_pattern % item.artist_name, headers={
                'Authorization': self.authorization},
                                     dont_filter=True)
            request.meta['artist'] = item
            yield request

    def parse(self, response):
        if response.meta['artist'].artist_name not in response.text:
            return

        content = json.loads(response.body.decode('utf-8'))
        for data in content['data']:
            if 'object' not in data:
                pass
            elif data['object']['type'] == 'question':
                self.log(data['object']['id'])
                self.log(data['object']['title'])
            elif data['object']['type'] == 'answer':
                request = scrapy.Request('https://www.zhihu.com/question/' + data['object']['question']['id'],
                                         headers={'Authorization': self.authorization},
                                         callback=self.parse_question)
                request.meta['question'] = data['object']['question']
                request.meta['artist'] = response.meta['artist']
                yield request
            elif data['object']['type'] == 'article':
                self.log(data['object']['type'])
                self.log(data['object']['title'])
                self.log(data['object']['id'])
            else:
                self.log(data['object']['type'])

        if not content['paging']['is_end']:
            request = scrapy.Request(
                content['paging']['next'].replace('http://www.zhihu.com',
                                                  'https://www.zhihu.com/api/v4'),
                headers={'Authorization': self.authorization})
            request.meta['artist'] = response.meta['artist']
            yield request

    def parse_question(self, response):
        yield Question(id=response.meta['question']['id'],
                       artist_id=response.meta['artist'].id,
                       title=response.xpath('//meta[@itemprop="name"]/@content').extract_first(default=''),
                       answer_count=response.xpath('//meta[@itemprop="answerCount"]/@content').extract_first(
                           default='0'),
                       comment_count=response.xpath('//meta[@itemprop="commentCount"]/@content').extract_first(
                           default='0'),
                       follower_count=response.xpath('//meta[@itemprop="zhihu:followerCount"]/@content').extract_first(
                           default='0'),
                       visitor_count=response.xpath(
                           '//div[contains(@class,"QuestionFollowStatus-counts")]//div[@class="NumberBoard-item"]/div[@class="NumberBoard-value"]/text()')[
                           1].extract())

        # yield scrapy.Request(
        #     'https://www.zhihu.com/api/v4/questions/%s/answers?limit=20&offset=0&include=data[*].is_normal,is_sticky,collapsed_by,suggest_edit,comment_count,collapsed_counts,reviewing_comments_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[].author.is_blocking,is_blocked,is_followed,voteup_count,message_thread_token,badge[?(type=best_answerer)].topics' %
        #     response.meta['question']['id'],
        #     headers={'Authorization': self.authorization},
        #     callback=self.parse_answer)

    # def parse_answer(self, response):
    #     content = json.loads(response.body.decode('utf-8'))
    #     for data in content['data']:
    #         yield Answer(id=data['id'],
    #                      question_id=data['question']['id'],
    #                      voteup_count=data['voteup_count'],
    #                      comment_count=data['comment_count'],
    #                      content=data['content'])
    #
    #     if not content['paging']['is_end']:
    #         yield scrapy.Request(
    #             content['paging']['next'].replace('http://', 'https://'),
    #             headers={'Authorization': self.authorization},
    #             callback=self.parse_answer)
