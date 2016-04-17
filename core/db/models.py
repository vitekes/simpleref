#-*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String

Base = declarative_base()


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String)
    url = Column(String)
    total_count = Column(Integer)
    download_count = Column(Integer)

    def __init__(self, category_name, url, total_count, download_count):
        self.category_name = category_name
        self.url = url
        self.total_count = total_count
        self.download_count = download_count


class Referat(Base):
    __tablename__ = 'referat'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer)
    name = Column(String)
    url = Column(String)
    text = Column(Text)
    download_link = Column(String)
    current_download_link = Column(String)
    preview = Column(Text)

    def __init__(self, category_id, url, name, text, download_link, current_download_link, preview):
        self.category_id = category_id
        self.url = url
        self.name = name
        self.text = text
        self.download_link = download_link
        self.current_download_link = current_download_link
        self.preview = preview


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    rating = Column(Integer)
    status = Column(Integer)
    user_articles_id = Column(Integer)

    def __init__(self, username, password, rating, status, user_articles_id):
        self.username = username
        self.password = password
        self.rating = rating
        self.status = status
        self.articles_id = user_articles_id


class UserArticles(Base):
    __tablename__ = 'userarticles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_articles = Column(Integer)

    def __init__(self, rating, user_articles):
        self.rating = rating
        self.user_articles = user_articles


class Comments(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer)
    user_id = Column(Integer)
    rating = Column(Integer)

    def __init__(self, article_id, url, user_id, rating):
        self.article_id = article_id
        self.user_id = user_id
        self.rating = rating
