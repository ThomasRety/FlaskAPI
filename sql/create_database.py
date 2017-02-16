import sqlite3

conn = sqlite3.connect('real_data.db')

c = conn.cursor()

c.execute('''CREATE TABLE objet (date text, name text, 
          description text, place real, hidden boolean, owner real, id integer primary key autoincrement, date%inscription varchar(255) NULL")''')

c.execute("CREATE TABLE user (user text, pseudo text, mail text, date_inscription varchar(255) NULL, date_naissance varchar(255) NULL, question_secrete varchar(255) NULL, reponse_secrete varhar(255) NULL, telephone integer NULL, id integer primary key autoincrement)")
  


conn.commit()
conn.close()
