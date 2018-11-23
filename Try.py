import flask
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

app = flask.Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome!"


@app.route("/<int:id>", methods=["GET"])
def index(id):
    cur.execute("select * from testing where id = " + str(id))
    result = cur.fetchall()
    return str(result[0])


@app.route("/makeatable")
def index2():
    cur.execute("create table IF NOT EXISTS testing (id serial primary key, column_1 text, column_2 text)")
    conn.commit()
    return "Done!"


@app.route("/insert")
def index3():
    cur.execute("insert into testing (column_1, column_2) values ('qwe', 'rty')")
    conn.commit()
    cur.execute("select * from testing)
    result = cur.fetchall()
    return str(result[0])


if __name__ == "__main__":
    app.run()
