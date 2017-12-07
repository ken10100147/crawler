# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from zhihu import db
from zhihu import items
from zhihu.spiders.topic_follower import TopicFollowerSpider


class DBPipeline(object):
    def open_spider(self, spider):
        db.attach(self)

        if isinstance(spider, TopicFollowerSpider) and db.TopicUserAssociation.exists(bind=self.engine):
            db.TopicUserAssociation.drop(bind=self.engine)
            db.TopicUserAssociation.create(bind=self.engine)
            self.session.flush()

    def close_spider(self, spider):
        self.session.commit()

    def process_item(self, item, spider):
        if isinstance(item, items.User):
            self.process_user(item)
        elif isinstance(item, items.Topic):
            self.process_topic(item)
        elif isinstance(item, items.Question):
            self.process_question(item)
        elif isinstance(item, items.Answer):
            self.process_answer(item)
        return item

    def process_question(self, item):
        query = self.session.query(db.Question).filter(db.Question.id == item['id'])
        question = db.Question() if query.count() == 0 else query.one()

        for key in item:
            setattr(question, key, item[key])

        if query.count() == 0:
            self.session.add(question)
            # can delay crawl frequency
            self.session.commit()

    def process_answer(self, item):
        query = self.session.query(db.Answer).filter(db.Answer.id == item['id'])
        answer = db.Answer() if query.count() == 0 else query.one()

        for key in item:
            setattr(answer, key, item[key])

        if query.count() == 0:
            self.session.add(answer)
            # can delay crawl frequency
            self.session.commit()

    def process_user(self, item):
        query = self.session.query(db.User).filter(db.User.channel == db.CHANNEL, db.User.user_id == item['id'])
        user = db.User() if query.count() == 0 else query.one()

        for key in item:
            if key == 'locations':
                user.location = ''
                for location in item['locations']:
                    user.location = user.location + ',' + location['name']

                user.location = user.location.replace(',', '', 1)
            elif key == 'business':
                user.business = item['business']['name']
            elif key == 'employments':
                user.employments = ''
                for employment in item['employments']:
                    company = employment['company'] if 'company' in employment else None
                    job = employment['job'] if 'job' in employment else None
                    user.employments = user.employments + ',' + self.json_value(json=company,
                                                                                key='name') + ':' + \
                                       self.json_value(json=job, key='name')

                user.employments = user.employments.replace(',', '', 1)
            elif key == 'educations':
                user.educations = ''
                for education in item['educations']:
                    school = education['school'] if 'school' in education else None
                    major = education['major'] if 'major' in education else None
                    user.educations = user.educations + ',' + self.json_value(json=school,
                                                                              key='name') + ':' + \
                                      self.json_value(json=major, key='name')

                user.educations = user.educations.replace(',', '', 1)
            elif key == 'id':
                user.user_id = item['id']
            elif key == 'name':
                user.nick = item['name']
            elif key == 'following_count':
                user.follow_count = item['following_count']
            elif key == 'follower_count':
                user.fans_count = item['follower_count']
            elif hasattr(user, key):
                setattr(user, key, item[key])

        user.channel = db.CHANNEL

        if query.count() == 0:
            self.session.add(user)
            # can delay crawl frequency
            self.session.commit()

        if 'from_topic' in item.keys():
            topic = self.session.query(db.Topic).filter(db.Topic.id == item['from_topic']).one()
            if not any(user.user_id == follower.user_id for follower in topic.followers):
                topic.followers.append(user)

    def process_topic(self, item):
        query = self.session.query(db.Topic).filter(db.Topic.id == item['id'])
        topic = db.Topic() if query.count() == 0 else query.one()

        for key in item:
            setattr(topic, key, item[key])

        if query.count() == 0:
            self.session.add(topic)
            # can delay crawl frequency
            self.session.commit()

    def json_value(self, json, key, default=''):
        if json is None:
            return ''

        if key in json:
            return json[key]
        else:
            return default
