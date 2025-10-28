
import sqlite3
import os

db_file = os.path.join('api', 'monitor_ping.db')
sql_file = 'esquema_v2.sql'

if os.path.exists(db_file):
    os.remove(db_file)

with open(sql_file, 'r') as f:
    sql_schema = f.read()

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.executescript(sql_schema)
conn.commit()
conn.close()

print(f"Database '{db_file}' created successfully.")
