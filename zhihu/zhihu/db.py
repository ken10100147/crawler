# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Table, Boolean, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

TopicUserAssociation = Table(
    'topic_user_association', Base.metadata,
    Column('topic_id', String(10), ForeignKey('topic.id')),
    Column('user_id', String(32), ForeignKey('user.id')))


class User(Base):
    __tablename__ = 'user'
    id = Column(String(32), primary_key=True)
    name = Column(String(32))
    gender = Column(Integer)
    user_type = Column(String(10))
    url_token = Column(String(32))
    is_org = Column(Boolean)
    locations = Column(String(120))
    business = Column(String(120))
    employments = Column(String(120))
    educations = Column(String(120))
    sina_weibo_name = Column(String(32))
    favorited_count = Column(Integer)
    following_count = Column(Integer)
    follower_count = Column(Integer)
    following_topic_count = Column(Integer)
    following_question_count = Column(Integer)
    voteup_count = Column(Integer)
    answer_count = Column(Integer)
    question_count = Column(Integer)
    articles_count = Column(Integer)
    columns_count = Column(Integer)

    topics = relationship('Topic', secondary=TopicUserAssociation, back_populates='followers')


class Topic(Base):
    __tablename__ = 'topic'
    id = Column(String(10), primary_key=True)
    name = Column(String(150))
    followers_count = Column(Integer)
    questions_count = Column(Integer)

    followers = relationship('User', secondary=TopicUserAssociation, back_populates='topics')


class Question(Base):
    __tablename__ = 'question'
    id = Column(String(10), primary_key=True)
    title = Column(String(150))
    answer_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    follower_count = Column(Integer, default=0)
    visitor_count = Column(Integer, default=0)

    answers = relationship('Answer')


class Answer(Base):
    __tablename__ = 'answer'
    id = Column(String(10), primary_key=True)
    question_id = Column(String(10), ForeignKey('question.id'), nullable=False)
    voteup_count = Column(Integer)
    comment_count = Column(Integer)
    content = Column(String(500))


def attach(target):
    target.engine = create_engine('mysql+pymysql://root:root@192.168.0.13/zhihu?charset=utf8mb4')
    target.session = sessionmaker(bind=target.engine, autoflush=False)()
    Base.metadata.create_all(target.engine)