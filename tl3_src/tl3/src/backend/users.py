#!/usr/bin/python3
import os
import cgi
import cgitb
import json
import logging
import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

cgitb.enable()
logger= logging.getLogger()
print("Content-Type: application/json;charset=utf-8")
print()

db_string = "postgres://admin:admin@tl3_db:5432/tl3"
engine = create_engine(db_string, echo=False)

metadata = MetaData()

users_table = Table('users', metadata,
     Column('id', Integer, primary_key=True),
     Column('name', String),
     Column('username', String),
     Column('age', Integer),
     Column('password', String),
)

metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
session = Session()


class User(declarative_base()):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    age = Column(Integer)
    password = Column(String)

    def __init__(self, name, age, username, password):
        self.name = name
        self.age = age
        self.username = username
        self.password = password

def query_users():
    users = []
    for u in session.query(User).all():
        user = u.__dict__
        user.pop('_sa_instance_state', None)    
        users.append(user)
        
    return users

def update_user():
    #Tomo lo que viene del formulario
    form = cgi.FieldStorage()
    user=query_users()
    session.update(user)
    #session.del(user)


def delete_user():
    form= cgi.FieldStorage()
    logger.exception(form)
    user = form.getvalue('username')
    for u in session.query(User).all():
        if (u.username.strip() == user):
            logger.exception ("EXISTEEEE ")
            session.delete(u)
            logger.exception("pase el delete")
            session.commit()
    #session.delete(u)
    #session.commit()

def update_user(id,upd):
    #Tomo lo que viene del formulario
    logger.error('LLEGOOOO')
    logger.error(upd)
    users=session.query(User).filter(User.id == int(id)).update({'name': upd.name})
    users=session.query(User).filter(User.id == int(id)).update({'age': upd.age})
    users=session.query(User).filter(User.id == int(id)).update({'username': upd.username})
    users=session.query(User).filter(User.id == int(id)).update({'password': upd.password})

    session.commit()

def create_user2():
    try:
        form = cgi.FieldStorage()
        logger.error(form)
        user = User(
            form.getvalue('name'),
            form.getvalue('age'),
            form.getvalue('username'),
            form.getvalue('password'),
            )
        val=form.getvalue('id_user')
        logger.error(val)
        if val == '#':  
            logger.error('LLEGO al add user')    
            session.add(user)
            session.commit()
        else:
            logger.error('LLEGO al update user')
            update_user(val,user)
        return {'error': False}
    except:
        return {'error': True}

def create_user():
    try:
        form = cgi.FieldStorage()
        user = User(
            form.getvalue('name'),
            form.getvalue('age'),
            form.getvalue('username'),
            form.getvalue('password')
            )
        session.add(user)
        session.commit()
        return {'error': False}
    except:
        return {'error': True}


if os.environ['REQUEST_METHOD'] == 'GET':
    response = query_users()    
if os.environ['REQUEST_METHOD'] == 'POST':
    response = create_user2()
if os.environ['REQUEST_METHOD'] == 'PUT':
    response = update_user()
if os.environ['REQUEST_METHOD'] == 'DELETE':
    logger.exception('Entro a DELETE')
    response = delete_user()
if not response:
    response = {}

print(json.JSONEncoder().encode(response))

