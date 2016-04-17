#-*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy import orm
from sqlalchemy import MetaData


class Database(object):

    def __init__(self, table, host="127.0.0.1", user="root", password="000", db="referat", charset='utf8'):
        self.engine = create_engine(
            'mysql://{user}:{password}@{server}/referat'.format(
                user=user,
                password=password,
                server=host
            )
        )

        self.session = orm.Session(bind=self.engine)
        self.meta = MetaData(bind=self.engine, reflect=True)
        self.meta.create_all()


