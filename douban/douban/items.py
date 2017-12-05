# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Music(scrapy.Item):
    id = scrapy.Field()
    artist_id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    rating = scrapy.Field()


class Review(scrapy.Item):
    id = scrapy.Field()
    music_id = scrapy.Field()
    title = scrapy.Field()
    summary = scrapy.Field()
    comments = scrapy.Field()
    useful_count = scrapy.Field()
    useless_count = scrapy.Field()


"""
.field public static final TYPE_SITE:Ljava/lang/String; = "site"

.field public static final TYPE_USER:Ljava/lang/String; = "user"

.field public static final VERIFY_TYPE_NONE:I = 0x0

.field public static final VERIFY_TYPE_OFFICIAL:I = 0x1

.field public static final VERIFY_TYPE_PERSONAL:I = 0x3

.field public static final VERIFY_TYPE_THIRD:I = 0x2

.field public static final VERIFY_TYPE_VERIFIED_USER:I = 0x4

"""


class User(scrapy.Item):
    # basic
    id = scrapy.Field()
    name = scrapy.Field()
    gender = scrapy.Field()
    intro = scrapy.Field()
    kind = scrapy.Field()
    uid = scrapy.Field()

    # extra
    ark_published_count = scrapy.Field()
    can_donate = scrapy.Field()
    can_set_original = scrapy.Field()
    collected_subjects_count = scrapy.Field()
    photo_albums_count = scrapy.Field()
    following_doulist_count = scrapy.Field()
    owned_doulist_count = scrapy.Field()
    followers_count = scrapy.Field()
    following_count = scrapy.Field()
    dramas_count = scrapy.Field()
    email = scrapy.Field()
    enable_disturb_free = scrapy.Field()
    user_hot_module_enabled = scrapy.Field()
    enable_wishlist_notification = scrapy.Field()
    group_chat_count = scrapy.Field()
    has_user_hot_module = scrapy.Field()
    in_blacklist = scrapy.Field()
    is_phone_bound = scrapy.Field()
    is_phone_verified = scrapy.Field()
    is_wechat_bound = scrapy.Field()
    joined_group_count = scrapy.Field()
    listeners_count = scrapy.Field()
    loc_name = scrapy.Field()
    loc = scrapy.Field()
    notes_count = scrapy.Field()
    owned_events_count = scrapy.Field()
    readers_count = scrapy.Field()
    show_audience_count = scrapy.Field()
    show_cart = scrapy.Field()
    statuses_count = scrapy.Field()
    tags_count = scrapy.Field()
    total_reviews = scrapy.Field()
    total_wish = scrapy.Field()
    verify_works_count = scrapy.Field()
    viewers_count = scrapy.Field()
    subscribe_niffler_columns_count = scrapy.Field()

    from_musician = scrapy.Field()


class Musician(scrapy.Item):
    id = scrapy.Field()
    follower_count = scrapy.Field()
