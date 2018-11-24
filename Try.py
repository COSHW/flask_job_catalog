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


@app.route("/tools/db/select+<int:id>", methods=["GET"])
def index(id):
    cur.execute("select * from testing where id = " + str(id))
    result = cur.fetchall()
    return str(result[0])


@app.route("/tools/db/makeatable+<string:name>")
def index2(name):
    cur.execute("create table IF NOT EXISTS "+ name+ " (id serial primary key, column_1 text, column_2 text)")
    conn.commit()
    return "Done!"


@app.route("/tools/db/insertinto+<string:name>+vlaues+<string:what>")
def index3(name, what):
    what = what.split(":")
    cur.execute("insert into " + name + " (column_1, column_2) values ('"+what[0]+"', '"+what[1]+"')")
    conn.commit()
    cur.execute("select * from testing")
    result = cur.fetchall()
    info = ""
    for item in result[0]:
        info = info + str(item) + ", "
    return info[:-2]


@app.route("/tools/db/delete+table+<string:name>")
def index4(name):
    cur.execute("drop table "+name)
    conn.commit()
    return "Done!"


@app.route("/tools/db/showalltables")
def index5():
    cur.execute("SELECT * FROM pg_catalog.pg_tables")
    result = cur.fetchall()
    return str(result[0])


if __name__ == "__main__":
    app.run()
