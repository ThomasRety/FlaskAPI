#/usr/bin/python3
#coding: utf-8
#IP = 163.5.181.144
#Welcome to the server
#WILKOMMEN

from flask import Flask, request, abort, send_file
from flask_cors import CORS, cross_origin
import os
import sqlite3
from werkzeug.utils import secure_filename
import hashlib
import time
import json


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

def execute_request(f):
    try:
        c.execute(f)
    except sqlite3.OperationalError as E:
        print("REQUETE PLANTE", f)
        print(E)
        return (False)
    row = c.fetchall()
    conn.commit()
    return (row)

def save_document(f, id_owner):
    try:
        a = "insert into image (name, id_owner) values('{}', {})".format(f.filename, str(id_owner))
        if (execute_request(a) == False):
            abort(403)
        a = "select ID from image where name = '{}' and id_owner = {}".format(f.filename, str(id_owner))
        row = execute_request(a)
        if (row == False):
            abort(403)
        try:
            id = row[0][0]
        except IndexError:
            return (False)
        f.save("/home/ubuntu/FlaskAPI/media/{}".format(str(id)))
        print("SAVE EFFECTUE")
        conn.commit()
        return (str(id))
    except Exception as E:
        print(E)
        return (False)

def get_id_with_mail(adresse):
    f = "select id from user where mail = '{}'".format(adresse)
    try:
        c.execute(f)
    except sqlite3.OperationalError as E:
        print("Error on get_id")
        print(E)
    row = c.fetchall()
    if (len(row) == 0):
        return (False)
    try:
        a = row[0][0]
        return (a)
    except IndexError:
        return (False)

def get_script():
    global ADMIN_TEXT
    with open('tout.html', 'r') as f:
        for line in f:
            ADMIN_TEXT += line

def is_id_image_right(id):
    f = "select * from image where id = {}".format(str(id))
    row = execute_request(f)
    if (row == False):
        return (False)
    if (len(row) == 0):
        return (False)
    return (True)
        
            
def do_admin(mail, password):
    if (mail == "thomas.rety57@gmail.com" and password == passwThomas):
        print("Thomas S'est log")
        return (True)
    elif (mail == "amela57290@gmail.com" and password == passwGuillaume):
        print("Guillaume s'est log")
        return (True)
    else:
        return (False)


    
#======================================================================================
#=================================== OBJET PART =======================================
#=====================================================================================

@app.route('/create_objet/', methods=['POST'])
def create_objet():
    if 'file' not in request.files:
        return ("C'EST VIDE LOLLLLLLLLLLLLLLLLLLLLLLL")
    f = request.files['file']
    mail = request.form['adresse']
    token = request.form['token']
    connecte = _login(mail, token)
    if (connecte != True):
        print("Vous n'êtes pas connecté")
        abort(403)
    id_owner = get_id_with_mail(mail)
    id = save_document(f, id_owner) 
    if (id is not False):
        return (id)
    print("Erreur")
    abort(403)

@app.route('/create_obj/', methods=['POST'])
def create_obj():
    if (request.method == 'POST'):
        try:
            adresse = request.form['adresse%mail']
            token = request.form['token']
            categorie = request.form['categorie']
            mature = request.form['mature']
            name = request.form['name']
            description = request.form['description']
            id_image = request.form['id_image']
        except Exception as E:
            print(E)
            print(adresse, token, categorie, mature, name, description, id_image)
            print('Toutes les données ne sont pas fournies')
            abort(403)
        id_owner = get_id_with_mail(adresse)
        print(id_owner)
        if (id_owner == False or _login(adresse, token) is not True):
            print("Adresse mail non valide")
            abort(403)
        f = "insert into objet(categorie, mature, name, description, id_creator, id_image) values ('{}', {}, '{}', '{}', {}, {})".format(categorie, mature, name, description, id_owner, id_image)
        try:
            c.execute(f)
        except sqlite3.OperationalError as E:
            print("REQUETE PLANTE", E)
            print("REQUETE = ", f)
            abort (403)
        return("OK")

@app.route('/get_image_user/<int:id_user>', methods=['GET'])
def get_id_image_with_id_user(id_user):
    f = "select id from image where id_owner = {}".format(str(id_user))
    row  =execute_request(f)
    if (row == False):
        abort (403)
    if (len(row) == 0):
        print("Le créateur {} n'as pas crée d'image".format(str(id_user)))
    return (formatage_row(row))

@app.route('/get_image/<int:id>', methods=['GET'])
def get_image(id):
    if (is_id_image_right(id) is not False):
        filename = "/home/ubuntu/FlaskAPI/media/{}".format(str(id))
        try:
            return send_file(filename)
        except Exception as E:
            abort (403)

@app.route('/get_library/<name>' , methods=['POST'])
def get_my_library(name):
    try:
        adresse = request.form['adresse%mail']
        token = request.form['token']
    except Exception as E:
        print(E)
        abort(403)
    _log = _login(adresse, token)
    if (_log is not True):
        print("L'adresse mail {} n'as pas un token valide".format(adresse))
        abort (403)
    f = "select id_image from objet where categorie = '{}'".format(name)
    row = execute_request(f)
    if (len(row) == 0):
        print("ROW EST VIDE", row)
        abort(403)
    s = formatage_row(row)
    print(name, s)
    return (s)
        
#====================================================================================
#===================== USER PART ====================================================
#====================================================================================

@app.route('/')
def hello_world():
    return (doc)

@app.route('/modif_user/', methods=['POST'])
def modif_login():
    if (request.method == 'POST'):
        try:
            mail = request.form['adresse%mail']
            token = request.form['token']
        except:
            print("Une des informations n'est pas valide")
            abort(403)
        f = "select * from user where mail = '{}' and token = '{}'".format(mail, token)
        try:
            c.execute(f)
        except sqlite3.OperationalError as E:
            print(E)
            abort (403)
        row = c.fetchall()
        return (json.dumps(row[0]))
        

@app.route('/create_user/', methods=['POST'])
def create_user():
    if (request.method == 'POST'):
        mail, passw = request.form['adresse%mail'], request.form['password']
        passw = (hashlib.sha512(passw.encode())).hexdigest()
        user_name = request.form['username']
        if (len(mail) == 0 or len(passw) == 0 or len(user_name) == 0):
            print("Un des champs est manquant")
            return("Un des champs est manquant")
        f = '''select pseudo from user where mail = '{}' '''.format(mail)
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
        f = '''select pseudo from user where pseudo = '{}' '''.format(user_name)
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
            f = '''insert into user(password, pseudo, mail, token, date_inscription, date_naissance, question_secrete, reponse_secrete, telephone, ADMIN) values ('{}', '{}', '{}', '10', NULL, NULL, NULL, NULL, NULL, 0 )''' .format(passw, user_name, mail)
            try:
                c.execute(f)
            except sqlite3.OperationalError as E:
                print("Erreur SQL")
                print("REQUETE = '{}'".format(f))
                print(E)
                abort(403)
            conn.commit()
            print("fonctionné")
            f = str(time.time())
            a = "update user set token = '{}' where mail = '{}'".format(f, mail)
            print("L'user {} as été cée avec le token {}".format(mail, f))
            try:
                c.execute(a)
            except sqlite3.OperationalError as E:
                print(E)
                abort (404)
            return (f)
    else:
        abort(401)

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
                f = str(time.time())
                a = "update user set token = '{}' where mail = '{}'".format(f, mail)
                try:
                    c.execute(a)
                except sqlite3.OperationalError as E:
                    print(E)
                print("Tu est log avec le token {}".format(f))
                conn.commit()
                return (f)
            else:
                print("échec")
                return ("echec")
        except IndexError:
            print("échec 4")
            return ("echec")
    else:
        abort(401)

def _login(adresse, token):
    f = "select token from user where mail = '{}'".format(adresse)
    try:
        c.execute(f)
    except sqlite3.OperationalError as E:
        print("REQUETE = '{}'".format(f))
        print('')
        print(E)
        return (False)
    try:
        verif = 0
        result = c.fetchall()
        if result[0][0] == token:
            return (True)
        else:
            return (False)
    except Exception as E:
        print(E)
        return (False)


@app.route('/get_pseudo/', methods=['POST'])
def get_pseudo():
    if (request.method == 'POST'):
        try:
            mail = request.form['adresse%mail']
            token = request.form['token']
        except:
            abort(403)
        f = "select pseudo from user where mail = '{}' and token = '{}'".format(mail, token)
        try:
            c.execute(f)
        except sqlite3.OperationalError as E:
            print("ERREUR {}".format(f))
            print(E)
            abort(403)
        result = c.fetchall()
        try:
            pseudo = result[0][0]
        except IndexError:
            print(result)
            return ("echec")
        return (pseudo)
    else:
        abort(405)


@app.route('/get_inventaire/', methods=['POST'])
def get_inventaire():
    try:
        mail = request.form['adresse%mail']
        token = request.form['token']
        name_salle = request.form['name']
        inv_demande = request.form['name_inv']
    except Exception as E:
        print (E)
        abort(403)
    id_salle = get_id_with_name(name_salle)
    id_owner = get_id_with_mail(mail)
    id_inv = get_id_with_mail(inv_demande)
    if (is_in_salle(name_salle, id_owner) == False):
        print('Ce vilain owner n\'est pas dans la salle :\'(', str(id_owner))
        abort(404)
    if (is_in_salle(name_salle, id_inv) == False):
        print('Ce vilain méchant n\'est pas dans la salle :\'(', str(id_inv))
        abort (404)
    f = "select inventaire from user where id = {}".format(str(id_inv))
    row = execute_request(f)
    if (row == False):
        abort (403)
    try:
        result = row[0][0]
    except IndexError as E:
        print(E)
        return ("errvide")
    s = result.split('|')
    ok = False
    for elem in s:
        j = elem.split(':')
        for i in j:
            if ok == True:
                print('i = ', i)
                return (j)
            if i == id_salle:
                ok = True
            

#======================================================================================
#=================================== SALLE PART =======================================
#======================================================================================

def formatage_row(row):
    s = ""
    for element in row:
        for elem in element:
            s = s + str(elem) + ','
        s = s[0:len(s) - 1] + ';'
    return (s)

def get_name_with_id(id):
    f = "select pseudo from user where id = {}".format(str(id))
    row = execute_request(f)
    if (row == False):
        return (False)
    try:
        result = row[0][0]
    except IndexError as E:
        print(E, "get_name_with_id", str(id))
        return (False)
    return (result)

@app.route('/get_all_library/', methods=['POST'])
def get_all_library():
    f = "select distinct categorie from objet"
    row = execute_request(f)
    if (row == False):
        abort(403)
    s = formatage_row(row)
    return (s)

@app.route('/get_list_user/<name_salle>', methods=['POST'])
def get_list_user(name_salle):
    f = "select id_user from salle where name = '{}'".format(str(name_salle))
    row = execute_request(f)
    if (row == False or len(row) == 0):
        print('row vide', row)
        abort (403)
    try:
        row = row[0][0]
        row = row.split(',')
        s = ""
    except IndexError as E:
        print(E, "get_list", row)
        abort (403)
    for elem in row:
        if (s == ""):
            s = get_name_with_id(elem)
            if (s == False):
                abort (403)
        else:
            e = get_name_with_id(elem)
            if (e == False):
                abort (403)
            s = s + ',' + e
    return (s)

@app.route('/get_salle/', methods=['GET'])
def get_the_salle():
    f = "select name, nb_personne from salle"
    row = execute_request(f)
    if (len(row) == 0):
        return ("Il n'y as encore aucune salle crée!! Créez en une")
    row = formatage_row(row)
    return (row)

@app.route('/create_salle', methods=['POST'])
def create_salle():
    try:
        adresse = request.form['adresse%mail']
        token = request.form['token']
        name = request.form['name']
        password = request.form['password']
    except Exception as E:
        print(E)
        print(adresse, token, name, password)
        abort(403)
    log = _login(adresse, token)
    if (log == False):
        print("Tu n'est pas log")
        abort(403)
    id_owner = get_id_with_mail(adresse)
    f = "select name from salle where name = '{}'".format(name)
    row = execute_request(f)
    if (row == False):
        print("Row = False, f = ", f)
        abort (403)
    if (len(row) != 0):
        return ("errsalledejaexistante")
    f = "insert into salle(name, password, id_owner, nb_personne, id_user) values('{}', '{}', {}, 0, '')".format(name, password, str(id_owner))
    row = execute_request(f)
    if (row == False):
        print("Row = False, f = ", f)
        abort(403)
    id_salle = get_id_with_name(name)
    row = connexion_id_with_salle(id_owner, id_salle)
    if (row == False):
        print("Row = False, connexion_id_with_salle" )
        abort (403)
    print("Salle crée")
    return ("OK")

def is_in_salle(name_salle, id_owner):
    f = "select id_user from salle where name = '{}'".format(name_salle)
    row = execute_request(f)
    if (row == False):
        print("False")
        return (False)
    try:
        result = row[0][0]
    except IndexError as E:
        print(E)
        return (False)
    s = result.split(',')
    for elem in s:
        if elem == str(id_owner):
            return (True)
    return (False)

@app.route('/delete_salle', methods=['POST'])
def delete_salle():
    try:
        adresse = request.form['adresse%mail']
        token = request.form['token']
        name = request.form['name']
        password = request.form['password']
    except Exception as E:
        print(E)
        abort(403)
    _log = _login(adresse, token)
    if (log == False):
        abort (403)
    id_owner = get_id_with_mail(adresse)
    f = "select id_owner from salle where name = '{}' and password = '{}'".format(name, password)
    row = execute_request(f)
    if (row == False):
        abort(403)
    try:
        result = row[0][0]
    except IndexError as E:
        print(E)
        abort (403)
    if (id_owner != result):
        print("Tu n'es pas le proprio de la salle")
        return ("errproprio")
    f = "select id from salle where name = '{}' and password = '{}'".format(name, password)
    row = execute_request(f)
    if (row == False):
        abort(403)
    try:
        result = row[0][0]
    except IndexError as E:
        print(E)
        abort (403)
    f = "update user set salle_id = None where salle_id = {}".format(str(result))
    row = execute_request(f)
    return ("OK")

@app.route('/get_my_salle/', methods=['POST'])
def get_the_last_salle():
    try:
        adresse = request.form['adresse%mail']
        token = request.form['token']
    except Exception as E:
        print(E)
        abort(403)
    log = _login(adresse, token)
    if (log == False):
        abort (403)
    id_owner = get_id_with_mail(adresse)
    f = "select salle_id from user where mail = '{}'".format(adresse)
    row = execute_request(f)
    if (row == False):
        abort(403)
    if (len(row) == 0):
        return ("None")
    else:
        try:
            result = row[0][0]
        except IndexError:
            print('VIDE')
            abort (404)
    f = "select name from salle where id = {}".format(str(result))
    row = execute_request(f)
    if (row == False):
        return ("None")
    if (len(row) == 0):
        return ("None")
    else:
        try:
            result = row[0][0]
        except IndexError:
            print('VIDE')
            abort (404)
        return (str(result))
        
@app.route('/connexion_with_salle', methods=['POST'])
def connexion_with_salle():
    try:
        adresse = request.form['adresse%mail']
        token = request.form['token']
        name = request.form['name']
        password = request.form['password']
    except:
        print("Toutes les données ne sont pas completes")
        print(adresse, token, name, password)
        abort(403)
    log = _login(adresse, token)
    if (log == False):
        abort (403)
    id_owner = get_id_with_mail(adresse)
    #vérification des mdp
    f = "select password from salle where name = '{}'".format(name)
    row = execute_request(f)
    if (row == False or len(row) == 0):
        abort (403)
    try:
        result = row[0][0]
    except IndexError as E:
        print(E)
        abort (403)
    if (result != password):
        print("Mauvais mot de passe")
        return ("errpassword")
    id_salle = get_id_with_name(name)
    if (id_salle == False):
        abort (403)
    result = connexion_id_with_salle(id_owner, id_salle)
    if (result):
        return ("OK")
    abort (403)

@app.route('/connexion_tmp', methods=['POST'])
def connexion_tmp():
    try:
        name = request.form['name']
        adresse = request.form['adresse%mail']
        token = request.form['token']
    except Exception as E:
        print(E)
        abort (403)
    log = _login(adresse, token)
    if (log == False):
        print("L'adresse mail {} n'as pas un token valide".format(name))
        abort (403)
    id_owner = get_id_with_mail(adresse)
    id_salle = get_id_with_name(name)
    if (id_salle == False):
        print("La salle {} n'existe pas".format(str(id_salle)))
        abort (403)
    result = connexion_id_with_salle(id_owner, id_salle)
    if (result):
        return ("OK")
    print("L'user {} n'as pas réussi à se connecter a la salle {}".format(str(id_owner), str(id_salle)))
    abort (403)

def get_id_with_name(name):
    f = "select id from salle where name = '{}'".format(name)
    row = execute_request(f)
    if (row == False or len(row) == 0):
        return (False)
    try:
        result = row[0][0]
    except IndexError as E:
        print(E)
        return (False)
    return (result)

def get_nb_personne(id_salle):
    f = "select nb_personne from salle where id = {}".format(str(id_salle))
    row = execute_request(f)
    print(row)
    try:
        nb = row[0][0]
    except IndexError as E:
        print(E, "GET NB PERSONNE, ROW = ", row)
        print(f)
        return (-84)
    return (nb)

def remove(id_owner, s):
    s = s.split(',')
    s = list(set(s))
    return (','.join(s))

def connexion_id_with_salle(id_owner, id_salle):
    f = "select salle_id from user where id = {}".format(str(id_owner))
    row = execute_request(f)
    if (row == False):
        print("row = False, f = ", f)
        return (False)
    try:
        #On get la salle de l'user
        id_salle2 = row[0][0]
    except IndexError as E:
        print(E, "ID_salle2, row = ", row)
    if (id_salle2 != None):
        #SI l'uttilisateur s'est deja connecté on update son ancienne salle
        nb = get_nb_personne(id_salle2)
        if (nb == -84):
            print("Impossible de get le nombre de personne de ancienne salle")
            return (False)
        f = "update salle set nb_personne = {} where id = {}".format(str(nb - 1), str(id_salle2))
        row = execute_request(f)
        if (row == False):
            print("Update ancienne salle set nb_personne = nb -1, row = False")
            return (False)
    #On set la salle_id de l'user pour la prochaine fois
    f = "update user set salle_id = {} where id = {}".format(str(id_salle), str(id_owner))
    row = execute_request(f)
    if (row == False):
        print("row = False, f = ", f)
        return (False)
    nb = get_nb_personne(id_salle)
    if (nb == -84):
        print("nb = False, get_nb_personne(", str(id_salle), ")")
        return (False)
    #on incrémente le nb de personne de la salle
    f = "update salle set nb_personne = {} where id = {}".format(str(nb + 1), str(id_salle))
    row = execute_request(f)
    if (row == False):
        print("row = False, f = ", f)
        return (False)
    #On incrémente les users présent dans la salle
    f = "select id_user from salle where id = {}".format(str(id_salle))
    row = execute_request(f)
    if (row == False or len(row) == 0):
        print("row = False, f = ", f)
        return (False)
    try:
        s = row[0][0]
    except IndexError as E:
        print(E, "select des id_user de la salle , row = ", row)
        abort (403)
    if s == "":
        s = s + str(id_owner)
    else:
        s = remove(id_owner, s)
        s = s + ',' + str(id_owner)
    f = "update salle set id_user = '{}' where id = {}".format(str(s), str(id_salle))
    row = execute_request(f)
    if (row == False):
        print("row = False, f = ", f)
        return (False)
    conn.commit()
    return (True)

@app.route('/get_the_image_back/', methods=['GET'])
def get_the_back_image():
    filename = "/home/ubuntu/FlaskAPI/image_back.jpg"
    try:
        return send_file(filename)
    except Exception as E:
        abort (403)
    
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
    s = s + "================================================================ <br />"
    f = "select * from image"
    c.execute(f)
    row = c.fetchall()
    s = s + str(row)
    a = "<p>" + s
    s = a.replace('),', ')<br />')
    s = s + "</p>"
    s = s + "================================================================ <br />"
    f = "select * from objet"
    c.execute(f)
    row = c.fetchall()
    s = s + str(row)
    a = "<p>" + s
    s = a.replace('),', ')<br />')
    s = s + "</p>"
    s = s + "================================================================ <br />"
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
        return (str(E))
    row = c.fetchall()
    s = str(row)
    conn.commit()
    return (s)

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

if __name__ == "__main__":
    get_script()
    app.run("0.0.0.0")
