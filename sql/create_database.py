import sqlite3

conn = sqlite3.connect('test_login.db')

c = conn.cursor()

#c.execute('''CREATE TABLE obj (date text, 
#          description text,  text, quantty real, price real)''')

#c.execute('''CREATE TABLE USER (user text, password text)''')
c.execute("insert into USER values ('admin', 'admin')")
conn.commit()
conn.close()
