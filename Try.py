import flask
import psycopg2
import subprocess

proc = subprocess.Popen('heroku config:get DATABASE_URL -a romanrestplz', stdout=subprocess.PIPE, shell=True)
db_url = proc.stdout.read().decode('utf-8').strip() + '?sslmode=require'

conn = psycopg2.connect(db_url)
cur = conn.cursor()

app = flask.Flask(__name__)


@app.route("/")
def welcome():
    return "Welcome!"


@app.route("/<int:id>", methods=["GET"])
def index(id):
    cur.execute("select * from testing where id = " + id)
    result = cur.fetchall()
    return result


@app.route("/makeatable")
def index2():
    cur.execute("create table IF NOT EXISTS testing (id serial primary key, column_1 text, column_2 text)")
    conn.commit()
    cur.execute("insert into testing (column_1, column_2) values ('qwe', 'rty')")
    conn.commit()
    cur.execute("select * from testing")
    result = cur.fetchall()
    return result


if __name__ == "__main__":
    app.run()
