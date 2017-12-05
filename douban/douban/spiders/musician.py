# -*- coding: utf-8 -*-
import scrapy
import json

from douban.items import User
from douban import db


class MusicianSpider(scrapy.Spider):
    name = 'musician'
    allowed_domains = ['douban.com']
    start_urls = ['http://music.douban.com/']

    url_pattern_musician = 'https://music.douban.com/musician/%s/fans'

    musician_ids = ['135690', '127202', '110500', '128691', '104810', '104602', '104549', '104654', '127213', '104118',
                    '134152']

    # musician_ids = ['104810']

    def start_requests(self):
        # for mid in self.musician_ids:
        #     request = scrapy.Request(self.url_pattern_musician % mid, callback=self.parse_musician)
        #     request.meta['mid'] = mid
        #     yield request

        db.attach(self)
        query = self.session.query(db.User)
        for user in query.all():
            if user.name is None:
                yield scrapy.Request(
                    'https://frodo.douban.com/api/v2/user/' + user.id + '?os_rom=flyme4&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Meizu_Market&udid=05ac1c24d6c2fe71c303c65f32b41d915343b987&_sig=vRQoW7znmzvf6mMJpw3jmJUPgpc%3D&_ts=1512110532',
                    headers={
                        'User-Agent': 'api-client/1 com.douban.frodo/5.13.0(116) Android/23 product/meizu_M5s vendor/Meizu model/M5s  rom/flyme4  network/wifi',
                        'referer': None},
                    callback=self.parse_user)

    def parse(self, response):
        content = json.loads(response.body)
        for music in content['musics']:
            if 'author' in music:
                if any(response.meta['key'] == author['name'] for author in music['author']):
                    item = Music()
                    for key in item.fields:
                        item[key] = music[key]
                    yield item

                    request = scrapy.Request(music['alt'] + 'reviews', callback=self.parse_review)
                    request.meta['music'] = item
                    yield request



    def parse_user(self, response):
        content = json.loads(response.body)
        item = User()
        for key in item.fields:
            if key in content:
                item[key] = content[key]

        if 'musician' in response.meta:
            item['from_musician'] = response.meta['musician']['id']
        yield item
        # 0 get all followers from musician ( done )
        # https://music.douban.com/musician/134152/fans?start=35
        # 1 get all songs from musician ( done )
        # 2 get all reviews from song ( done )

        # 要看有没有被豆瓣收录

        # https: // music.douban.com / musician / 134152 /
        # get followers by this
        # https: // music.douban.com / musician / 134152 / fans?start = 35
        # https: // music.douban.com / subject / 27067039 /
        # get song by search
        # we can search single song or author's all songs by this
        # https://api.douban.com/v2/music/search?q\=陈鸿宇
        # https://music.douban.com/subject/27067039/reviews

        # https: // site.douban.com / wpoxs /?s = 570539
        # https: // site.douban.com / wpoxs / widget / playlist / 14891341 / get_song_lyric

        # apikey = 0dad551ec0f84ed02907ff5c42e8ec70
        # did = 05ac1c24d6c2fe71c303c65f32b41d915343b987
        # https://frodo.douban.com/api/v2/user/1312772?os_rom=flyme4&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Meizu_Market&udid=05ac1c24d6c2fe71c303c65f32b41d915343b987&_sig=q%2B%2B7LeqexaCp%2BXXqSPK2yq%2BiUgE%3D&_ts=1512043582

        # android:debuggable="true"

        # com.douban.frodo_116/src_smali/smali/com/douban/frodo/baseproject/util/FrodoUtils.smali  tamper client_secret
        #             const-string/jumbo v0, "9e8bb54dc3288cdf"

        # https://frodo.douban.com/service/auth2/token
        # client_id=0dad551ec0f84ed02907ff5c42e8ec70&client_secret=9e8bb54dc3288cdf&redirect_uri=frodo%3A%2F%2Fapp%2Foauth%2Fcallback%2F&disable_account_create=false&grant_type=password&username=18801951923&password=10100147&os_rom=flyme4&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Meizu_Market&udid=05ac1c24d6c2fe71c303c65f32b41d915343b987&_sig=pT3NWNjSmgnivDSkOuwg%2Fj3B09k%3D&_ts=1512110532
        # api-client/1 com.douban.frodo/5.13.0(116) Android/23 product/meizu_M5s vendor/Meizu model/M5s  rom/flyme4  network/wifi
