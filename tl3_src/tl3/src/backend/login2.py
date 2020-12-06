#!/usr/bin/python3
import cgi, cgitb
from http import cookies
import os
from db_handler import Database
import logging


logger = logging.getLogger()

def session_init_render():
    print()
    print("""
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Login</title>
        </head>
        <body>
            <div>                        
                <form action="/cgi-bin/login.py" method="post">
                    <div>
                        <label for="num">Username::</label>
                        <input type="text" name="username"><br><br>
                    </div>
                    <div>
                        <label for="password">Password:</label>
                        <input type="password" name="password"><br><br>
                    </div>
                    <div>
                        <label for=""></label>
                        <input type="submit" value="login">
                    </div>
                </form>
            </div>
        </body>
    </html>
    """)

if __name__ == "__main__" :
    if 'HTTP_COOKIE' in os.environ:        
        cookie = cookies.SimpleCookie(os.environ['HTTP_COOKIE'])
        logger.exception('ESTOY EN LOGGIN')
        logger.exception('ESTOY EN LOGGIN')
        logger.exception('ESTOY EN el if de cookie')
        if cookie is None:
            session_init_render()

        key = cookie.get('session_key').value
        value = cookie.get('session_value').value
        logger.exception('ESTOY EN LOGGIN')
        logger.exception('ESTOY EN LOGGIN')
        logger.exception('ESTOY EN LOGGIN')
        logger.exception('ESTOY EN LOGGIN')
        logger.info(key,value)
        database = Database.instance()
        if not database.exists_cookie(key, value):
            logger.exception('Error cookie not in database')
            session_init_render()
        else:
            cookie = database.get_cookie(key)
            print(cookie)            
            print("Content-Type: application/json")
            print()
            print({'a':'asd'})
    else:
        logger.exception('el environment no tiene la cookie')
        session_init_render()
