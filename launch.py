#/usr/bin/python3
#IP = 163.5.181.144
#Welcome to the server

from flask import Flask, request, abort
from flask_cors import CORS, cross_origin


import os
import sqlite3
from werkzeug.utils import secure_filename
app = Flask(__name__)
cors = CORS(app, ressources={"/*":{"origins": "*"}})

app.config.from_object(__name__)

db = 'sql/real_data.db'
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

@app.route('/<user>/<ide>')
def check_img(user, ide):
    return (name)

@app.route('/modif_user/', methods=['POST'])
def modif_login():
    if (request.method == 'POST'):
        mail = request.form['adresse%mail']
        passw = request.form['password']
        username = request.form['username']
        old_mail = request.form['old%mail']
        old_passw = request.form['old%password']
        old_username = request.form['old%username']
        if (old_mail == mail and passw == old_passw and old_username == username):
            abort(403)
        if (len(mail) == 0 or len(passw) == 0 or len(username) == 0):
            abort(403)
        f = "select mail from user where user.user = '{}' and password = '{}'".format(old_username, old_passw)
        try:
            c.execute(f)
        except sqlite3.OperationalError:
            abort(403)
        row = c.fetchall()
        if (len(row) == 0 or row[0][0] != old_mail):
            abort(403)
        f = "update user set user = '{}', mail = '{}', password = '{}' where mail = '{}' and password = '{}' and user = '{}'".format(username, mail, passw, old_mail, old_passw, old_username)
        try:
            c.execute(f)
        except:
            abort(403)
        return ("201")
        


@app.route('/create_user/', methods=['POST'])
def create_user():
    if (request.method == 'POST'):
        print("Request recu", end=' ')
        mail, passw = request.form['adresse%mail'], request.form['password']
        user_name = request.form['username']
        print(mail, '|', passw, '|', user_name)
        if (len(mail) == 0 or len(passw) == 0 or len(user_name) == 0):
            abort(403)
        f = '''select user from user where mail = '{}' '''.format(mail)
        try:
            c.execute(f)
        except sqlite3.OperationalError:
            abort(403)
        row = c.fetchall()
        if len((row)) != 0:
            print("Le mail existe déjà")
            return ("FAUX")
        f = '''select user from user where user.user = '{}' '''.format(user_name)
        try:
            c.execute(f)
        except sqlite3.OperationalError:
            abort(403)        
        if len(c.fetchall()) != 0:
            print("ça existe déja")
            return ("CA EXISTE DEJA")
        else:
            #Il n'y as pas de même nom d'user
            f = '''insert into user values ('{}', '{}', '{}')''' .format(user_name, passw, mail)
            try:
                c.execute(f)
            except sqlite3.OperationalError:
                abort(403)
            conn.commit()
            print("fonctionné")
            return ("Je dois vous prévenir que cela a fonctionné")
    else:
        abort(401)

@app.route('/create_obj/', methods=['POST'])
def create_obj():
    if (request.method == 'POST'):
        id_owner = int(request.form['id%owner'])
        date = request.form['date']
        description = request.form['description']
        place = int(request.form['place'])
        hidden = request.form['hidden']
        name = request.form['name']
        c.execute('''insert into obj values ('{}', '{}', '{}', {}, {}, {} '''.format(date, name, description, place, hidden, id_owner))
        c.execute('''select id from obj where date = '{}', description = '{}', owner = {}, name = '{}' '''.format(date, description, id_owner, name))
        if len(result = c.fetchall()) == 0:
            return ("ca a planté")
        else:
            ide = result
            try:
                if not os.path.isdir('./var/{}/'.format(id_owner)):
                    os.mkdir('./var/{}/'.format(id_owner))
                f = request.files['the_file']
                f.save('./var/{}'.format(id_owner) + secure_filename(f.filename))
                return ("ca a fontionne")
            except:
                return ("le document n'as pas été créé")
                

@app.route('/login', methods=['POST'])
def login():
    if (request.method == 'POST'):
        mail = request.form['adresse%mail']
        print("mail = ", mail, end=' ')
        passw = request.form['password']
        print("& password = ", passw)
        f = '''select password from user where mail = '{}' '''.format(mail)
        try:
            c.execute(f)
        except sqlite3.OperationalError:
            abort(403)
        try:
            result = c.fetchall()
            if result[0][0] == passw:
                print("Tu EST LOG")
                f = os.urandom(8)
                return (f)
            else:
                return ("echec")
        except IndexError:
            return ("echec")
    else:
        abort(401)


