# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import create_engine, Table, Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

recom_banner_table = Table(
    'rb_association', Base.metadata,
    Column('recom_id', Integer, ForeignKey('recom.id')),
    Column('banner_id', Integer, ForeignKey('banner.id'))
)


class Song(Base):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    artists = Column(String(40))
    album = Column(String(20))
    href = Column(String(2083))


class Album(Base):
    __tablename__ = 'album'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    artists = Column(String(40))
    href = Column(String(2083))


class Banner(Base):
    __tablename__ = 'banner'
    id = Column(Integer, primary_key=True)
    table = Column(String(10))
    table_id = Column(Integer)
    recoms = relationship('Recom', secondary=recom_banner_table, back_populates='banners')


class Recom(Base):
    __tablename__ = 'recom'
    id = Column(Integer, primary_key=True)
    platform = Column(String(20), nullable=False)
    time = Column(DateTime, default=datetime.datetime.utcnow)
    banners = relationship('Banner', secondary=recom_banner_table, back_populates='recoms')


def attach(target):
    target.engine = create_engine('mysql+pymysql://root:root@192.168.0.13/media_banner?charset=utf8mb4')
    target.session = sessionmaker(bind=target.engine, autoflush=False)()
    Base.metadata.create_all(target.engine)
