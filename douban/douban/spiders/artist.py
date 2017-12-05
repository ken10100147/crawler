# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True)
    artist_name = Column(String(256))
    douban = Column(String(32))


def all():
    engine = create_engine('mysql+pymysql://root:root@192.168.0.13/beatles?charset=utf8mb4')
    session = sessionmaker(bind=engine, autoflush=False)()
    Base.metadata.create_all(engine)
    return session.query(Artist).all()
