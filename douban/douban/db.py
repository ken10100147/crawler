# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import create_engine, Table, Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

MusicianUserAssociation = Table(
    'musician_user_association_' + datetime.now().strftime('%Y_%m_%d'), Base.metadata,
    Column('musician_id', String(10), ForeignKey('musician_' + datetime.now().strftime('%Y_%m_%d') + '.id'),
           nullable=False),
    Column('user_id', String(32), ForeignKey('user' + datetime.now().strftime('%Y_%m_%d') + '.id'), nullable=False))


class User(Base):
    __tablename__ = 'user_' + datetime.now().strftime('%Y_%m_%d')
    # basic
    id = Column(String(32), primary_key=True)
    name = Column(String(32))
    gender = Column(String(12))
    intro = Column(String(150))
    kind = Column(String(12))
    uid = Column(String(32))

    # extra
    ark_published_count = Column(Integer)
    can_donate = Column(Boolean)
    can_set_original = Column(Boolean)
    collected_subjects_count = Column(Integer)
    photo_albums_count = Column(Integer)
    following_doulist_count = Column(Integer)
    owned_doulist_count = Column(Integer)
    followers_count = Column(Integer)
    following_count = Column(Integer)
    dramas_count = Column(Integer)
    email = Column(String(32))
    enable_disturb_free = Column(Boolean)
    user_hot_module_enabled = Column(Boolean)
    enable_wishlist_notification = Column(Boolean)
    group_chat_count = Column(Integer)
    has_user_hot_module = Column(Boolean)
    in_blacklist = Column(Boolean)
    is_phone_bound = Column(Boolean)
    is_phone_verified = Column(Boolean)
    is_wechat_bound = Column(Boolean)
    joined_group_count = Column(Integer)
    listeners_count = Column(Integer)
    loc_name = Column(String(32))
    loc = Column(String(64))
    notes_count = Column(Integer)
    owned_events_count = Column(Integer)
    readers_count = Column(Integer)
    show_audience_count = Column(Integer)
    show_cart = Column(Boolean)
    statuses_count = Column(Integer)
    tags_count = Column(Integer)
    total_reviews = Column(Integer)
    total_wish = Column(Integer)
    verify_works_count = Column(Integer)
    viewers_count = Column(Integer)
    subscribe_niffler_columns_count = Column(Integer)

    followings = relationship('Musician', secondary=MusicianUserAssociation, back_populates='followers')


class Musician(Base):
    __tablename__ = 'musician_' + datetime.now().strftime('%Y_%m_%d')
    id = Column(String(12), primary_key=True)
    follower_count = Column(Integer, default=0)

    followers = relationship('User', secondary=MusicianUserAssociation, back_populates='followings')


class Music(Base):
    __tablename__ = 'music_' + datetime.now().strftime('%Y_%m_%d')
    id = Column(String(12), primary_key=True)
    artist_id = Column(Integer, nullable=False)
    title = Column(String(32))
    author = Column(String(32))
    rating = Column(String(32))
    rater_number = Column(Integer)


class Review(Base):
    __tablename__ = 'review_' + datetime.now().strftime('%Y_%m_%d')
    id = Column(String(12), primary_key=True)
    music_id = Column(String(12), ForeignKey(Music.__tablename__ + '.id'), nullable=False)
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
