# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class BannerPipeline(object):
#     def process_item(self, item, spider):
#         return item
#
#
# class SongPipeline(object):
#     def process_item(self, item, spider):
#         return item
#
#
# class AlbumPipeline(object):
#     def process_item(self, item, spider):
#         return item
from datetime import datetime
from banner import db
from banner.db import Recom
from banner.db import Banner
from banner.items import Song
from banner.items import Album


class DBPipeline(object):
    def open_spider(self, spider):
        self.recom = Recom(platform=spider.name, time=datetime.now())
        db.attach(self)

    def close_spider(self, spider):
        if len(self.recom.banners) > 0:
            self.session.add(self.recom)

        self.session.flush()
        self.session.commit()

    def process_item(self, item, spider):
        banner = Banner()
        if isinstance(item, Song):
            query = self.session.query(db.Song).filter(db.Song.href == item['href'])
            song = db.Song() if len(query.all()) == 0 else query.first()

            song.name = item['name']
            song.artists = item['artists']
            song.album = item['album']
            song.href = item['href']

            if len(query.all()) == 0:
                self.session.add(song)
                self.session.commit()
                song = self.session.query(db.Song).filter(db.Song.href == item['href']).first()

            banner.table = db.Song.__tablename__
            banner.table_id = song.id
        elif isinstance(item, Album):
            query = self.session.query(db.Album).filter(db.Album.href == item['href'])
            album = db.Album() if len(query.all()) == 0 else query.first()

            album.name = item['name']
            album.artists = item['artists']
            album.href = item['href']

            if len(query.all()) == 0:
                self.session.add(album)
                self.session.commit()
                album = self.session.query(db.Album).filter(db.Album.href == item['href']).first()

            banner.table = db.Album.__tablename__
            banner.table_id = album.id

        query = self.session.query(db.Banner).filter(
            db.Banner.table == banner.table, db.Banner.table_id == banner.table_id)

        if len(query.all()) == 0:
            self.session.add(banner)
            self.session.commit()
            query = self.session.query(db.Banner).filter(db.Banner.table == banner.table,
                                                         db.Banner.table_id == banner.table_id)

        banner = query.first()

        self.recom.banners.append(banner)
        return item
