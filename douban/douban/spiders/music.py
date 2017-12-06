# -*- coding: utf-8 -*-
import scrapy
import json
from douban.spiders import artist
from douban.items import Music


class MusicSpider(scrapy.Spider):
    name = 'music'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    url_pattern_search = 'https://api.douban.com/v2/music/search?q=%s'

    def start_requests(self):
        for item in artist.all():
            request = scrapy.Request(self.url_pattern_search % item.artist_name)
            request.meta['artist'] = item
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
