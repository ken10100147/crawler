# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from douban import db
from douban import items
from douban.spiders.follower import FollowerSpider


class DBPipeline(object):
    def open_spider(self, spider):
        db.attach(self)

        if isinstance(spider, FollowerSpider) and db.MusicianUserAssociation.exists(bind=self.engine):
            db.MusicianUserAssociation.drop(bind=self.engine)
            db.MusicianUserAssociation.create(bind=self.engine)
            self.session.flush()

    def close_spider(self, spider):
        self.session.commit()

    def process_item(self, item, spider):
        if isinstance(item, items.User):
            self.process_user(item)
        elif isinstance(item, items.Music):
            self.process_music(item)
        elif isinstance(item, items.Review):
            self.process_review(item)
        elif isinstance(item, items.Musician):
            self.process_musician(item)

        return item

    # def process_musician(self, item):
    #     query = self.session.query(db.Musician).filter(db.Musician.id == item['id'])
    #     musician = db.Musician() if query.count() == 0 else query.one()
    #
    #     musician.id = item['id']
    #     musician.follower_count = item['follower_count']
    #
    #     if query.count() == 0:
    #         self.session.add(musician)
    #         # can delay crawl frequency
    #         self.session.commit()

    def process_user(self, item):
        query = self.session.query(db.User).filter(db.User.id == item['id'])
        user = db.User() if query.count() == 0 else query.one()

        for key in item:
            if key == 'loc':
                if item[key]:
                    user.loc = item[key]['name']
            else:
                setattr(user, key, item[key])

        if query.count() == 0:
            self.session.add(user)
            # can delay crawl frequency
            self.session.commit()

        if 'from_musician' in item.keys():
            query = self.session.query(db.ArtistFansRelationship).filter(
                db.ArtistFansRelationship.channel == db.CHANNEL,
                db.ArtistFansRelationship.artist_id == item['from_musician'],
                db.ArtistFansRelationship.fans_id == item['id'])

            if query.count() == 0:
                self.session.add(
                    db.ArtistFansRelationship(channel=db.CHANNEL, artist_id=item['from_musician'], fans_id=item['id']))
                self.session.commit()

    def process_music(self, item):
        query = self.session.query(db.Music).filter(db.Music.id == item['id'])
        music = db.Music() if query.count() == 0 else query.one()

        music.channel_song_id = item['id']
        music.artist_id = item['artist_id']
        music.channel_song_name = item['title']
        music.channel = db.CHANNEL
        # music.author = ''
        # for author in item['author']:
        #     music.author = music.author + ',' + author['name']
        # music.author = music.author.replace(',', '', 1)
        # music.rating = item['rating']['average']
        # music.rater_number = item['rating']['numRaters']

        if query.count() == 0:
            self.session.add(music)
            # can delay crawl frequency
            self.session.commit()

    def process_review(self, item):
        query = self.session.query(db.Review).filter(db.Review.id == item['id'])
        review = db.Review() if query.count() == 0 else query.one()

        for key in item:
            setattr(review, key, item[key])

        if query.count() == 0:
            self.session.add(review)
            # can delay crawl frequency
            self.session.commit()
