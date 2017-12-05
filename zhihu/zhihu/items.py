# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class Question(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    answer_count = scrapy.Field()
    comment_count = scrapy.Field()
    follower_count = scrapy.Field()
    visitor_count = scrapy.Field()


class Answer(scrapy.Item):
    id = scrapy.Field()
    question_id = scrapy.Field()
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()
    content = scrapy.Field()


class Topic(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    followers_count = scrapy.Field()
    questions_count = scrapy.Field()


class User(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    user_type = scrapy.Field()
    url_token = scrapy.Field()
    is_org = scrapy.Field()

    locations = scrapy.Field()
    business = scrapy.Field()
    employments = scrapy.Field()
    educations = scrapy.Field()

    sina_weibo_name = scrapy.Field()

    favorited_count = scrapy.Field()
    following_count = scrapy.Field()
    follower_count = scrapy.Field()
    following_topic_count = scrapy.Field()
    following_question_count = scrapy.Field()
    voteup_count = scrapy.Field()
    answer_count = scrapy.Field()
    question_count = scrapy.Field()
    articles_count = scrapy.Field()
    columns_count = scrapy.Field()

    from_topic = scrapy.Field()
