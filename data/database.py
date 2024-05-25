import os
import sqlite3

conn = sqlite3.connect(os.path.join("database.db"))
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS channel(
   id INTEGER PRIMARY KEY,
   name TEXT,
   admin TEXT);""")

cur.execute("""CREATE TABLE IF NOT EXISTS post(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    text TEXT, 
    username TEXT, 
    channel INT, 
    images TEXT,
    user_id INT, 
    FOREIGN KEY (channel) REFERENCES channel(id));""")

cur.execute("""CREATE TABLE IF NOT EXISTS form(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    questions text, 
    channel INT, 
    FOREIGN KEY (channel) REFERENCES channel(id));""")

cur.execute("""CREATE TABLE IF NOT EXISTS answer_form(
     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
     user_id INT,
     channel_id INT,
     answer TEXT,
     FOREIGN KEY (channel_id) REFERENCES channel(id));""")


conn.commit()
cur.execute("SELECT *  FROM channel")
print(cur.fetchall(), "channel")
cur.execute("SELECT * FROM form")
print(cur.fetchall(), "form")
cur.execute("SELECT * FROM answer_form")
print(cur.fetchall(), "answer_form")
cur.execute("SELECT * FROM post")
print(cur.fetchall(), "post")
conn.close()