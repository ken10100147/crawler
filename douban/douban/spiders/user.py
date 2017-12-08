# -*- coding: utf-8 -*-
import scrapy
import json
from douban.items import User
from douban import db


class UserSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['douban.com']
    start_urls = ['http://music.douban.com/']

    def start_requests(self):
        db.attach(self)
        query = self.session.query(db.User).filter(db.User.channel == db.CHANNEL)
        for user in query.all():
            if user.name is None:
                yield scrapy.Request(
                    'https://frodo.douban.com/api/v2/user/' + user.id + '?os_rom=flyme4&apikey=0dad551ec0f84ed02907ff5c42e8ec70&channel=Meizu_Market&udid=05ac1c24d6c2fe71c303c65f32b41d915343b987&_sig=vRQoW7znmzvf6mMJpw3jmJUPgpc%3D&_ts=1512110532',
                    headers={
                        'User-Agent': 'api-client/1 com.douban.frodo/5.13.0(116) Android/23 product/meizu_M5s vendor/Meizu model/M5s  rom/flyme4  network/wifi',
                        'referer': None})

    def parse(self, response):
        content = json.loads(response.body.decode('utf-8'))
        item = User()
        for key in item.fields:
            if key in content:
                item[key] = content[key]

        yield item
