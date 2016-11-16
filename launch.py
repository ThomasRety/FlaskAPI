#/usr/bin/python3
#IP = 163.5.181.144
#Welcome to the server

from flask import Flask, request, abort



import os
import sqlite3
from werkzeug.utils import secure_filename
app = Flask(__name__)

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

@app.route('/create_user/', methods=['POST'])
def create_user():
    if (request.method == 'POST'):
        mail, passw = request.form['adresse%mail'], request.form['password']
        user_name = request.form['username']
        c.execute('''select user from user where mail = '{}' '''.format(mail))
#        if len((row = c.fetchall())) != 0:
#            print(row)
#            return ("FAUX")
        c.execute('''select user from user where user.user = '{}' '''.format(user_name))
        if len(c.fetchall()) != 0:
            return ("CA EXISTE DEJA")
        else:
            #Il n'y as pas de même nom d'user
            c.execute('''insert into user values ('{}', '{}', '{}')''' .format(user_name, passw, mail))
            conn.commit()
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
        mail, passw = request.form['adresse%mail'], request.form['password']
        c.execute('''select password from user where mail = '{}' '''.format(mail))
        try:
            print("mail = ", mail)
            print("password = ", passw)
            result = c.fetchall()
            print(result)
            if result[0][0] == passw:
                return ("valid")
            else:
                return ("not valide")
        except IndexError:
            return ("not valid")
    else:
        abort(401)


