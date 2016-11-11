import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

#c.execute('''CREATE TABLE obj (date text, 
#          description text,  text, quantty real, price real)''')

#c.execute('''CREATE TABLE USER (user text, password text, date date, Obj_Up real, email text)''')
c.execute('''CREATE TABLE OBJ (name text, user USER, 
conn.commit()
conn.close()
