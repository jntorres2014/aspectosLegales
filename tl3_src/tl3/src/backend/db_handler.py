#!/usr/bin/python3
import os
import cgi
from http import cookies
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, String, Integer, MetaData, DateTime, ForeignKey, tuple_
import logging
import datetime


logger = logging.getLogger()

class Database:

    __instance = None

    @staticmethod
    def instance():
        if (Database.__instance == None):
            Database.__instance = Database()
        return Database.__instance

    def __init__(self):
        if (Database.__instance is not None):
            return Database.__instance
        db_string = "postgres://admin:admin@tl3_db:5432/tl3"
        self.db = create_engine(db_string, echo=False)
        self.meta = MetaData(self.db)

        self.cookies = Table(
                        'cookies', 
                        self.meta, 
                        Column('key', String, primary_key=True),
                        Column('value', String),
                        Column('usuario', Integer),
                       )
        self.users= Table(
                    'users',
                    self.meta,
                    Column('id',Integer, primary_key=True),
                    Column('name',String),
                    Column('username',String),
                    Column('age',Integer),
                    Column('password',String),)

        self.jobs= Table(
                    'jobs',
                    self.meta,
                    Column('id',Integer, primary_key=True),
                    Column('id_user',Integer),
                    Column('lugar_trabajo',String),
                    Column('cargo',String),
                    Column('observacion',String),)

    def exits_user(self,user,password):
        result = self.meta.tables["users"]
        user_row = result.select().where(result.c.username==user) 
        user2_row=result.select().where(result.c.password==password)
        user_rs = self.db.execute(user_row)
        logger.error(user_rs.rowcount)
        user2_rs = self.db.execute(user2_row)
        logger.error(user2_rs.rowcount)
        return user_rs.rowcount >= 1 and user2_rs.rowcount == 1

    def get_id(self,username,password):
        result = self.meta.tables["users"]
        user_row = result.select().where(result.c.username==username) 
        user2_row=result.select().where(result.c.password==password)
        user2_rs = self.db.execute(user_row)
        id=(user2_rs.fetchone()[0])
        return id

    def exists_cookie(self, key, value):
        result = self.meta.tables["cookies"]
        cookie_row = result.select().where(result.c.key==key)
        cookies_rs = self.db.execute(cookie_row)
        return cookies_rs.rowcount == 1

    def get_cookie(self, key):
        result = self.meta.tables["cookies"]
        logger.error('Llegue a get cookie')
        logger.error(result.c.key)
        cookie_row = result.select().where(result.c.key==key)
        logger.error(cookie_row)
        
        cookie_rs = self.db.execute(cookie_row)
        if (cookie_rs.rowcount != 0):
            cookie = cookie_rs.first()
            return [cookie[0],cookie[1]]
        else:
            return []

    def insert_cookie(self, key, value):
        statement = self.cookies.insert().values(key=key, value=value,usuario=0)
        self.db.execute(statement)
