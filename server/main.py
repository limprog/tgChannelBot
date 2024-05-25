import json
from flask import Flask, request
import sqlite3
import os

def get_db_connection():
    conn = sqlite3.connect(os.path.join('../data/database.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur


app = Flask(__name__)

@app.route("/new_channel", methods=['POST'])
def new_ch():
    data = request.form

    conn, cur = get_db_connection()
    cur.execute('INSERT INTO channel(id, name, admin) VALUES (?, ?, ?)',
                 (data['id'], data['name'], data["admin"],))
    conn.commit()
    conn.close()
    return ("", 201)


@app.route("/delete_ch", methods=["POST"])
def delete_ch():
    data = request.form
    conn, cur = get_db_connection()
    cur.execute("DELETE FROM channel where id = ?", (data['id'], ))
    conn.commit()
    conn.close()
    return ("", 201)


@app.route("/add_post", methods=["POST"])
def add_post():
    data = request.form
    print(data)
    conn, cur = get_db_connection()
    cur.execute("INSERT INTO post(text, username, channel, images, user_id) VALUES (?, ?, ?, ?, ?)", (data["post_text"], data["user"], data["chanel_id"], json.dumps(data["images"]), data["id"],))
    conn.commit()
    conn.close()
    return ("", 201)


if __name__ == '__main__':
    app.run(debug=True)


