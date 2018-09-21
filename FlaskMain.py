from flask import Flask, request, jsonify, render_template
import psycopg2
import re
import urlparse
import ast

import re

app = Flask(__name__)

connection = None


@app.route('/connect')
def connect():
    global connection
    db = request.args.get('db')
    user = request.args.get('user')
    passw = request.args.get('password')
    host = request.args.get('host')
    port = request.args.get('port')

    print 50 * '-'
    print db, user, passw, host, port
    print 50 * '-'

    if passw == '':
        cs = "dbname = %s user = %s host = %s  port = %s" % (db, user, host, port)
    else:
        cs = "dbname = %s user = %s password = %s host = %s  port = %s" % (db, user, passw, host, port)

    try:
        connection = psycopg2.connect(cs)

    except Exception as e:
        return render_template("error.html")

    return render_template("success.html")


@app.route('/loadentry_num')
def load_entry_num():
    try:
        cur_cursor = connection.cursor()
    except Exception:
        return render_template("error.html")
    sql = ("SELECT COUNT(*) FROM eintraege")
    cur_cursor.execute(sql)
    req = str(cur_cursor.fetchone())
    return re.search(r'\d+', req).group()


@app.route('/load_all_entrys')
def load_all_entrys():
    cur_cursor = connection.cursor()

    sql = ("SELECT titel, passwort FROM eintraege")
    cur_cursor.execute(sql)
    return str(cur_cursor.fetchall())


@app.route('/update_content')
def update_content():
    cur_cursor = connection.cursor()
    sql = ("DELETE FROM eintraege")
    cur_cursor.execute(sql)
    connection.commit()
    content = request.args.getlist('content')
    content = ast.literal_eval(content[0])
    for element in content:
        titel = element[0]
        passwort = element[1]
        sql = ("INSERT INTO eintraege (titel, passwort) VALUES (%s, %s)")
        data = (titel, passwort)
        cur_cursor.execute(sql, data)
        connection.commit()


if __name__ == '__main__':
    app.run(debug=True)
