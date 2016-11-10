#/usr/bin/python3
#IP = 163.5.181.144
#Welcome to the server

from flask import Flask, request, abort

import os
import sqlite3
app = Flask(__name__)

app.config.from_object(__name__)

doc = "ID interdit = 404, img interdite = patate, /id/<int:ide>/?img=patate"

def connect_database(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    return (cursor)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
    ))
app.config.from_envvar('FLASK_SETINGS', silent=True)

def check(id):
    if id == 404:
        return (None)
    else:
        return (43)

def check_img(ide, img):
    if (img == "patate"):
        return (None)
    else:
        return (42)

    
@app.route('/')
def hello_world():
    return (doc)

@app.route('/img/<name>')
def check_img(name):
    return (name)


@app.route('/user/', methods=['POST', 'GET'])
def login():
    if (request.method == 'POST'):
        return ('{} + {}'.format(request.form['username'], request.form['password']))
    elif (request.method == 'GET'):
        key = request.args.get('key', '')
        value = request.args.get('value', '')
        return (key + ' TESTE ' + value)
    else:
        return ('wtf')


@app.route('/id/<int:ide>/', methods=['GET'])
def check_if_this_id(ide):
    if not check(ide):
        abort(401)
    else:
        img_search = request.args.get('img', '')
        return (type(img_search))
        if not check_img(ide, img_search):
            abort(404)
        else:
            return ('C\'est valide!')
