# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Table, MEDIUMTEXT, Column, String, Integer, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# MusicianUserAssociation = Table(
#     'musician_user_association',
#     Column('artist_id', String(10), ForeignKey('artists.id'), nullable=False),
#     Column('user_id', Integer, ForeignKey('user_info.id'), nullable=False))

CHANNEL = 9


class ArtistFansRelationship(Base):
    __tablename__ = 'artist_fans_relationship'
    id = Column(Integer, primary_key=True)
    channel = Column(String(8))
    artist_id = Column(Integer)
    fans_id = Column(String(64))


class User(Base):
    __tablename__ = 'user_info'
    # # basic
    # id = Column(String(32), primary_key=True)
    # name = Column(String(32))
    # gender = Column(String(12))
    # intro = Column(String(150))
    # kind = Column(String(12))
    # uid = Column(String(32))
    #
    # # extra
    # ark_published_count = Column(Integer)
    # can_donate = Column(Boolean)
    # can_set_original = Column(Boolean)
    # collected_subjects_count = Column(Integer)
    # photo_albums_count = Column(Integer)
    # following_doulist_count = Column(Integer)
    # owned_doulist_count = Column(Integer)
    # followers_count = Column(Integer)
    # following_count = Column(Integer)
    # dramas_count = Column(Integer)
    # email = Column(String(32))
    # enable_disturb_free = Column(Boolean)
    # user_hot_module_enabled = Column(Boolean)
    # enable_wishlist_notification = Column(Boolean)
    # group_chat_count = Column(Integer)
    # has_user_hot_module = Column(Boolean)
    # in_blacklist = Column(Boolean)
    # is_phone_bound = Column(Boolean)
    # is_phone_verified = Column(Boolean)
    # is_wechat_bound = Column(Boolean)
    # joined_group_count = Column(Integer)
    # listeners_count = Column(Integer)
    # loc_name = Column(String(32))
    # loc = Column(String(64))
    # notes_count = Column(Integer)
    # owned_events_count = Column(Integer)
    # readers_count = Column(Integer)
    # show_audience_count = Column(Integer)
    # show_cart = Column(Boolean)
    # statuses_count = Column(Integer)
    # tags_count = Column(Integer)
    # total_reviews = Column(Integer)
    # total_wish = Column(Integer)
    # verify_works_count = Column(Integer)
    # viewers_count = Column(Integer)
    # subscribe_niffler_columns_count = Column(Integer)


    id = Column(Integer, primary_key=True, nullable=False)
    nick = Column(String(32))
    user_id = Column(String(32))
    channel = Column(Integer)
    desc = Column(MEDIUMTEXT)
    location = Column(String(24))
    gender = Column(SmallInteger)

    # age = Column(String(8))

    follow_count = Column(Integer)
    fans_count = Column(Integer)
    business = Column(String(128))
    educations = Column(String(128))
    employments = Column(String(128))

    following_topic_count = Column(Integer)
    following_question_count = Column(Integer)
    voteup_count = Column(Integer)
    answer_count = Column(Integer)
    question_count = Column(Integer)
    articles_count = Column(Integer)
    columns_count = Column(Integer)

    # followings = relationship('Musician', secondary=MusicianUserAssociation, back_populates='followers')


class Artists(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    artist_name = Column(String(256))
    douban = Column(String(32))
    # follower_count = Column(Integer, default=0)

    # followers = relationship('User', secondary=MusicianUserAssociation, back_populates='followings')


class Music(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    channel_song_id = Column(String(32))
    channel_song_name = Column(String(128))
    channel_artist_id = Column(String(32))
    channel_album_id = Column(String(32))
    channel = Column(String(8))
    artist_id = Column(Integer)
    # album_id = Column(Integer)
    # channel_digit_song_id = Column(String(32))
    # created_at = Column(DateTime, default=datetime.datetime.now)



    # title = Column(String(32))
    # author = Column(String(32))
    # rating = Column(String(32))
    # rater_number = Column(Integer)


class Review(Base):
    __tablename__ = 'review'
    id = Column(String(12), primary_key=True)
    music_id = Column(Integer, ForeignKey(Music.__tablename__ + '.id'), nullable=False)
    title = Column(String(150))
    summary = Column(String(300))
    comments = Column(Integer, default=0)
    useful_count = Column(Integer, default=0)
    useless_count = Column(Integer, default=0)


ENGINE = None
SESSION = None


def attach(target):
    global ENGINE
    global SESSION
    if ENGINE is None:
        ENGINE = create_engine('mysql+pymysql://root:root@192.168.0.13/douban?charset=utf8mb4')
        SESSION = sessionmaker(bind=ENGINE, autoflush=False)()
        Base.metadata.create_all(ENGINE)

    target.engine = ENGINE
    target.session = SESSION
