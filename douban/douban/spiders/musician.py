# -*- coding: utf-8 -*-
import scrapy
import json
from douban.items import Music
from douban.items import Review
from douban.items import Musician
from douban.items import User
from douban import db


class MusicianSpider(scrapy.Spider):
    name = 'musician'
    allowed_domains = ['douban.com']
    start_urls = ['http://music.douban.com/']

    url_pattern_search = 'https://api.douban.com/v2/music/search?q=%s'
    url_pattern_musician = 'https://music.douban.com/musician/%s/fans'

    keys = [u'王嘉尔', u'赵丽颖', u'张碧晨', u'香香', u'周深', u'郁可唯', u'王铮亮', u'谭维维', u'弦子', u'张磊', u'王晰', u'何洁', u'陈鸿宇', u'马雨阳',
            u'冯佳界', u'栗先达', u'杨猛', u'李晋', u'任灿', u'侯康', u'墙宇飞碟', u'七修远', u'耿鑫', u'寒洛', u'寒洛&鼓润', u'代鑫', u'柳爽', u'倪健',
            u'熊猫眼乐队', u'袁景', u'宁夏', u'草图君', u'戴荃', u'王建房', u'双飞人Veni', u'鹿先森乐队', u'鹿先森', u'ATF', u'阿克江', u'大张伟',
            u'刘昱妤Lexie', u'二本猫']

    musician_ids = ['135690', '127202', '110500', '128691', '104810', '104602', '104549', '104654', '127213', '104118',
                    '134152']

    # musician_ids = ['104810']

    def start_requests(self):
        # for key in self.keys:
        #     request = scrapy.Request(self.url_pattern_search % key)
        #     request.meta['key'] = key
        #     yield request

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

    def parse_review(self, response):
        review_list = response.xpath('//div[@class="review-list  "]/div')
        for review in review_list:
            reply = review.xpath('.//div[@class="action"]/a[@class="reply"]/text()').extract_first(default='')
            reply = reply[0:(len(reply) - 2)]

            yield Review(id=review.xpath('@data-cid').extract_first(),
                         music_id=response.meta['music']['id'],
                         title=review.xpath('.//div[@class="main-bd"]/h2/a/text()').extract_first(default=''),
                         summary=review.xpath('.//div[@class="short-content"]/text()').extract_first(
                             default='').strip(),
                         comments=reply,
                         useful_count=review.xpath(
                             './/div[@class="action"]/a[contains(@class,"up")]/span/text()').extract_first(
                             default='0').strip(),
                         useless_count=review.xpath(
                             './/div[@class="action"]/a[contains(@class,"down")]/span/text()').extract_first(
                             default='0').strip())

        if len(review_list) > 0:
            if 'start=' in response.url:
                idx = response.url.index('?start=')
                request = scrapy.Request(response.url[0:(idx - 1)] + '?start=' + str(
                    int(response.url[(idx + len('?start=')):len(response.url)]) + 35),
                                         callback=self.parse_review)
                request.meta['music'] = response.meta['music']
                yield request
            else:
                request = scrapy.Request(response.url + '?start=35', callback=self.parse_review)
                request.meta['music'] = response.meta['music']
                yield request

    def parse_musician(self, response):
        musician = Musician(id=response.meta['mid'],
                            follower_count=response.xpath('//h1/text()').re_first('([0-9]{1,})'))

        response.meta['musician'] = musician
        yield musician

        for request in self.parse_followers(response):
            yield request

    def parse_followers(self, response):
        obu_list = response.xpath('//dl[@class="obu"]')
        for dl in obu_list:
            uid = dl.xpath('dd/a/@href').extract_first(default='')
            uid = uid[len('https://www.douban.com/people/'):(len(uid) - 1)]
            yield User(id=uid, from_musician=response.meta['musician']['id'])
            request = scrapy.Request(
                'https://frodo.douban.com/api/v2/user/' + uid + '?os_rom=flyme4&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Meizu_Market&udid=05ac1c24d6c2fe71c303c65f32b41d915343b987&_sig=vRQoW7znmzvf6mMJpw3jmJUPgpc%3D&_ts=1512110532',
                headers={
                    'User-Agent': 'api-client/1 com.douban.frodo/5.13.0(116) Android/23 product/meizu_M5s vendor/Meizu model/M5s  rom/flyme4  network/wifi',
                    'referer': None},
                callback=self.parse_user)
            request.meta['musician'] = response.meta['musician']
            yield request

        if len(obu_list) > 0:
            if 'start=' in response.url:
                idx = response.url.index('?start=')
                request = scrapy.Request(response.url[0:idx] + '?start=' + str(
                    int(response.url[(idx + len('?start=')):len(response.url)]) + 35),
                                         callback=self.parse_followers)
                request.meta['musician'] = response.meta['musician']
                yield request
            else:
                request = scrapy.Request(response.url + '?start=35', callback=self.parse_followers)
                request.meta['musician'] = response.meta['musician']
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
