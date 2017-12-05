# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Song(scrapy.Item):
    href = scrapy.Field()
    name = scrapy.Field()
    artists = scrapy.Field()
    album = scrapy.Field()


class Album(scrapy.Item):
    href = scrapy.Field()
    name = scrapy.Field()
    artists = scrapy.Field()
