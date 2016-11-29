#/usr/bin/python3
#coding: utf-8
#IP = 163.5.181.144
#Welcome to the server

from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
import os
import sqlite3
from werkzeug.utils import secure_filename
import hashlib


app = Flask(__name__)
cors = CORS(app, ressources={"/*":{"origins": "*"}})

app.config.from_object(__name__)


passwThomas = '5c92318242c515a45d23be7085ab2e494517a02db4a9d58ceae5e342a844d069a72253635a47ea5f210b662c21f98745261bd7b0a5bd5833c5332f6013f00af7'
passwGuillaume = '9fe7a0518ec34d62fa601a605ccc3cf30a812146ea0e0a61e1d48f1de0cb433253b9ded9ebb83438354989452e42351046d55101304df82d242bce96eef8eadc'
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

ADMIN_TEXT = ""

def get_script():
    global ADMIN_TEXT
    with open('tout.html', 'r') as f:
        for line in f:
            ADMIN_TEXT += line


def do_admin(mail, password):
    if (mail == "thomas.rety57@gmail.com" and password == passwThomas):
        print("Thomas S'est log")
        return (True)
    elif (mail == "amela57290@gmail.com" and password == passwGuillaume):
        print("Guillaume s'est log")
        return (True)
    else:
        return (False)
    

@app.route('/')
def hello_world():
    return (doc)

@app.route('/modif_user/', methods=['POST'])
def modif_login():
    if (request.method == 'POST'):
        print('\n===============================================================\n')
        mail = request.form['adresse%mail']
        passw = request.form['password']
        passw = (hashlib.sha512(passw.encode())).hexdigest()
        username = request.form['username']
        old_mail = request.form['old%mail']
        old_passw = request.form['old%password']
        old_passw = (hashlib.sha512(old_passw.encode())).hexdigest()
        old_username = request.form['old%username']
        if (old_mail == mail and passw == old_passw and old_username == username):
            print("Aucune information n'as été modifiée")
            return ("errnomodif")
        if (len(mail) == 0 or len(passw) == 0 or len(username) == 0):
            print("Un champs est manquant")
            abort(403)
        f = "select mail from user where user.user = '{}' and password = '{}'".format(old_username, old_passw)
        try:
            c.execute(f)
        except sqlite3.OperationalError:
            abort(403)
        row = c.fetchall()
        if (len(row) == 0 or row[0][0] != old_mail):
            print("L'adresse mail ne correspond pas au mot de passe")
            return ("errauth")
        f = "update user set user = '{}', mail = '{}', password = '{}' where mail = '{}' and password = '{}' and user = '{}'".format(username, mail, passw, old_mail, old_passw, old_username)
        try:
            c.execute(f)
        except:
            abort(403)
        return ("201")
        


@app.route('/create_user/', methods=['POST'])
def create_user():
    if (request.method == 'POST'):
        print('\n===============================================================\n')
        print("Request recu", end=' ')
        mail, passw = request.form['adresse%mail'], request.form['password']
        passw = (hashlib.sha512(passw.encode())).hexdigest()
        user_name = request.form['username']
        print(mail, '|', passw, '|', user_name)
        if (len(mail) == 0 or len(passw) == 0 or len(user_name) == 0):
            print("Un des champs est manquant")
            return("Un des champs est manquant")
        f = '''select user from user where mail = '{}' '''.format(mail)
        try:
            c.execute(f)
        except sqlite3.OperationalError as E:
            print("Erreur SQL")
            print("REQUETE = '{}'".format(f))
            print(E)
            abort(403)
        row = c.fetchall()
        if len((row)) != 0:
            print("Le mail existe déjà")
            return ("erremail")
        f = '''select user from user where user.user = '{}' '''.format(user_name)
        try:
            c.execute(f)
        except sqlite3.OperationalError as E:
            print("ERREUR SQL")
            print("REQUETE = '{}'".format(f))
            print(E)
            abort(403)        
        if len(c.fetchall()) != 0:
            print("ça existe déja")
            return ("errpseudo")
        else:
            #Il n'y as pas de même nom d'user
            f = '''insert into user values ('{}', '{}', '{}', 'None')''' .format(user_name, passw, mail)
            try:
                c.execute(f)
            except sqlite3.OperationalError as E:
                print("Erreur SQL")
                print("REQUETE = '{}'".format(f))
                print(E)
                abort(403)
            conn.commit()
            print("fonctionné")
            f = os.urandom(8)
            a = "udpdate user set token = '{}' where mail = '{}'".format(f, mail)
            print("L'user {} as été cée avec le token {}".format(mail, f))
            try:
                c.execute(a)
            except sqlite3.OperationalError:
                pass
            return (f)
    else:
        abort(401)

@app.route('/create_obj/', methods=['POST'])
def create_obj():
    if (request.method == 'POST'):
        try:
            adresse = request.form['adresse%mail']
            token = request.form['token']
            categorie = int(request.form['categorie'])
        except:
            pass
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
        print('\n===============================================================\n')
        mail = request.form['adresse%mail']
        print("mail = ", mail, end=' ')
        try:
            passw = request.form['password']
            passw = (hashlib.sha512(passw.encode())).hexdigest()
            print("& password = ", passw)
            t = 0
        except:
            token = request.form['token']
            print("& token = ", token)
            t = 1
        if (do_admin(mail, passw) == True):
            return ("admin")
        if (t == 0):
            f = '''select password from user where mail = '{}' '''.format(mail)
        else:
            f = "select token from user where mail = '{}'".format(mail)
        try:
            c.execute(f)
        except sqlite3.OperationalError as E:
            print("REQUETE = '{}'".format(f))
            print('')
            print(E)
            abort(403)
        try:
            verif = 0
            result = c.fetchall()
            if (t == 0):
                if result[0][0] == passw:
                    verif = 1
                else:
                    verif = 0
            else:
                if result[0][0] == token:
                    verif = 1
                else:
                    verif = 0
            if verif == 1:
                f = os.urandom(8)
                a = "udpdate user set token = '{}' where mail = '{}'".format(f, mail)
                try:
                    c.execute(a)
                except sqlite3.OperationalError:
                    pass
                print("Tu est log avec le token {}".format(f))
                return (f)
            else:
                print("échec")
                return ("echec")
        except IndexError:
            print("échec 4")
            return ("echec")
    else:
        abort(401)


@app.route('/get_pseudo/', methods=['POST'])
def get_pseudo():
    if (request.method == 'POST'):
        try:
            mail = request.form['adresse%mail']
            token = request.form['token']
        except:
            abort(403)
        
        
#=================================================================================================
#====================================== ADMIN PART ===============================================
#=================================================================================================

@app.route('/db', methods=['POST'])
def get_the_db():
    print('===============================================================\n')
    mail, passw = request.form['adresse%mail'], request.form['password']
    passw = (hashlib.sha512(passw.encode())).hexdigest()
    if (do_admin(mail, passw) == False):
        abort(403)
    f = "select * from user"
    c.execute(f)
    row = c.fetchall()
    s = str(row)
    a = "<p>" + s
    s = a.replace('),', ')<br />')
    s = s + "</p>"
    return (s)

@app.route('/get_html', methods=['POST'])
def get_the_html():
    mail, passw = request.form['adresse%mail'], request.form['password']
    passw = (hashlib.sha512(passw.encode())).hexdigest()
    if (do_admin(mail, passw) == False):
        abort(403)
    print("J'envoie le html")
    return (ADMIN_TEXT)

@app.route('/delete/<maile>', methods=['POST'])
def delete_user(maile):
    mail, passw = request.form['adresse%mail'], request.form['password']
    passw = (hashlib.sha512(passw.encode())).hexdigest()
    if (do_admin(mail, passw) == False):
        abort(403)
    f = "delete from user where mail = '{}'".format(maile)
    try:
        c.execute(f)
    except sqlite3.OperationalError as E:
        print("Erreur SQL, f = ", f)
        print("Erreur SQL = ", E)
        return ("Erreur SQL")
    conn.commit()
    return ("Utilisateur % delete" % maile)

@app.route('/sql/', methods=['POST'])
def get_request():
    mail, passw = request.form['adresse%mail'], request.form['password']
    passw = (hashlib.sha512(passw.encode())).hexdigest()
    if (do_admin(mail, passw) == False):
        abort(403)
    f = request.form['sql']
    try:
        c.execute(f)
    except sqlite3.OperationalError as E:
        return (E)
    row = c.fetchall()
    s = str(row)
    return (row)

@app.route('/delete/sql', methods=['POST'])
def delete_the_sql():
    mail, passw = request.form['adresse%mail'], request.form['password']
    passw = (hashlib.sha512(passw.encode())).hexdigest()
    if (do_admin(mail, passw) == False):
        abort(403)
    f = "delete from user"
    c.execute(f)
    conn.commit()
    return ("done")

@app.route('/filter/0/<user>/', methods=['POST'])
def get_the_user_with_mail(user):
    mail, passw = request.form['adresse%mail'], request.form['password']
    passw = (hashlib.sha512(passw.encode())).hexdigest()
    if (do_admin(mail, passw) == False):
        abort(403)
    f = "select * from user where mail = '{}'".format(user)
    try:
        c.execute(f)
    except sqlite3.OperationalError as E:
        return (E)
    row = c.fetchall()
    s = str(row)
    return (row)

@app.route('/filter/1/<user>', methods=['POST'])
def get_the_user_with_user(user):
    mail, passw = request.form['adresse%mail'], request.form['password']
    passw = (hashlib.sha512(passw.encode())).hexdigest()
    if (do_admin(mail, passw) == False):
        abort(403)
    f = "select * from user where user = '{}'".format(user)
    try:
        c.execute(f)
    except sqlite3.OperationalError as E:
        return (E)
    row = c.fetchall()
    s = str(row)
    return (row)

@app.route('/')
def passe():
    return ("J'aime la grosse bite")

if __name__ == "__main__":
    get_script()
    app.run("0.0.0.0")
