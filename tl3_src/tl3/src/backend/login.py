#!/usr/bin/python3
import os
import cgi
import cgitb
import json
import sqlalchemy
from db_handler import Database
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from http import cookies

cgitb.enable()
logger= logging.getLogger()
print("Content-Type: application/json;charset=utf-8")
print()



def validarUser ():
    
    if 'HTTP_COOKIE' in os.environ:        
        cookie = cookies.SimpleCookie(os.environ['HTTP_COOKIE'])        
        if cookie is None:
            return {'error': True}
        key = cookie.get('session_key').value
        value = cookie.get('session_value').value
        logger.info(key,value)
        database = Database.instance()
        if not database.exists_cookie(key, value):
            logger.error('no existe la cookie busco el login')
            form = cgi.FieldStorage()
            user=form.getvalue('user') 
            passw = form.getvalue('pass')
            if database.exits_user(user,passw):
                #if (u.username.strip() == user) and (u.password.strip() == passw):
                logger.exception ("EXISTEEEE ")
                database.insert_cookie(key,value)
                return {'error': False}
            logger.error('no existe Login')
            #if validarUsuario():
            logger.exception('Error cookie not in database')
            return {'error': True}
        else:
            logger.error('Entre porque existia la cookie')
            cookie = database.get_cookie(key)
            logger.error(cookie)
            return {'error': False}
    else:
        logger.exception('el environment no tiene la cookie')
        return {'error': False}
        #session_init_render()


if os.environ['REQUEST_METHOD'] == 'GET':
    logger.exception ("GET")
    response = validarUser()
if os.environ['REQUEST_METHOD'] == 'POST':
    logger.exception ("POST")
    response = validarUser()
    logger.error('volvi')
    logger.error(response)  

print(json.JSONEncoder().encode(response))
