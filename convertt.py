import sqlite3
import json
connection = sqlite3.connect("db/OCEL_Simple_Database.db")
c = connection.cursor()
c.execute("SELECT name from sqlite_master Where type = 'table'")
alltables = c.fetchall()
file = open("dump.json","a")

for e in alltables:
    c.execute(f"SELECT * FROM {e[0]}")
    rows = c.fetchall()
    col = [i[0] for i in c.description]
    data=[dict(zip(col,row)) for row in rows]
    jsonn = json.dumps(data,indent=2)
    file.write(f"'{e[0]}':{jsonn}")

