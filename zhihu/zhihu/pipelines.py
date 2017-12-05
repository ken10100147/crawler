# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import db
import items
from spiders.topic import TopicSpider


class DBPipeline(object):
    def open_spider(self, spider):
        db.attach(self)

        if isinstance(spider, TopicSpider) and db.TopicUserAssociation.exists(bind=self.engine):
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
        query = self.session.query(db.User).filter(db.User.id == item['id'])
        user = db.User() if query.count() == 0 else query.one()

        for key in item:
            if key == 'locations':
                user.locations = ''
                for location in item['locations']:
                    user.locations = user.locations + ',' + location['name']

                user.locations = user.locations.replace(',', '', 1)
            elif key == 'business':
                user.business = item['business']['name']
            elif key == 'employments':
                user.employments = ''
                for employment in item['employments']:
                    user.employments = user.employments + ',' + self.json_value(json=employment['company'],
                                                                                key='name') + ':' + \
                                       self.json_value(json=employment['job'], key='name')

                user.employments = user.employments.replace(',', '', 1)
            elif key == 'educations':
                user.educations = ''
                for education in item['educations']:
                    user.educations = user.educations + ',' + self.json_value(json=education['school'],
                                                                              key='name') + ':' + \
                                      self.json_value(json=education['major'], key='name')

                user.educations = user.educations.replace(',', '', 1)
            else:
                setattr(user, key, item[key])

        if query.count() == 0:
            self.session.add(user)
            # can delay crawl frequency
            self.session.commit()

        query = self.session.query(db.Topic).filter(db.Topic.id == item['from_topic'])
        topic = db.Topic(id=item['from_topic']) if query.count() == 0 else query.one()
        if query.count() == 0:
            self.session.add(topic)
            # can delay crawl frequency
            self.session.commit()
            topic = self.session.query(db.Topic).filter(db.Topic.id == item['from_topic']).one()

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
        if key in json:
            return json[key]
        else:
            return default
