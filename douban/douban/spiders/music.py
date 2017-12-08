# -*- coding: utf-8 -*-
import scrapy
import json
from douban.items import Music
from douban import db


class MusicSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    url_pattern_search = 'https://api.douban.com/v2/music/search?q=%s'

    def start_requests(self):
        db.attach(self)
        for artist in self.session.query(db.Artists).all():
            request = scrapy.Request(self.url_pattern_search % artist.artist_name)
            request.meta['artist'] = artist
            yield request

    def parse(self, response):
        content = json.loads(response.body.decode('utf-8'))
        for music in content['musics']:
            if 'author' in music:
                if any(response.meta['artist'].artist_name == author['name'] for author in music['author']):
                    item = Music()
                    for key in item.fields:
                        if key in music:
                            item[key] = music[key]
                    item['artist_id'] = response.meta['artist'].id
                    yield item
