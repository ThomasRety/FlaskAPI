#/usr/bin/python3
#IP = 163.5.181.144
#Welcome to the server

from flask import Flask, request, abort

import os
import sqlite3
app = Flask(__name__)

app.config.from_object(__name__)

db = 'sql/test_login.db'
doc = 'test'

conn = sqlite3.connect(db)
c = conn.cursor()

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'sql/test_login.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
    ))
app.config.from_envvar('FLASK_SETINGS', silent=True)

@app.route('/')
def hello_world():
    return (doc)

@app.route('/img/<name>')
def check_img(name):
    return (name)

@app.route('/create_user/', methods=['POST'])
def create_user():
    if (request.method == 'POST'):
        mail, passw = request.form['adresse%mail'], request.form['password']
        c.execute('''select name from user where user = '{}' '''.format(mail))
        if len(c.fetchall()) != 0:
            return (False)
        else:
            #Il n'y as pas de même nom d'user
            c.execute('''insert into user values ('{}', '{}')''' .format(mail, passw))
            conn.commit()
            return (True)
    else:
        abort(401)

@app.route('/login', methods=['POST'])
def login():
    if (request.method == 'POST'):
        mail, passw = request.form['adresse%mail'], request.form['password']
        c.execute('''select password from user where user = %''' % mail)
        result = c.fetchall()
        if result == passw:
            return (True)
        else:
            return (False)
    else:
        abort(401)


