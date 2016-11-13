import sqlite3

conn = sqlite3.connect('real_data.db')

c = conn.cursor()

c.execute('''CREATE TABLE obj (date text, name text, 
          description text, place real, hidden boolean, owner real, id integer primary key autoincrement)''')

c.execute('''CREATE TABLE USER (user text, password text, mail text)''')
c.execute("insert into USER values ('admin', 'admin', 'admin\admin.com')")
conn.commit()
conn.close()
