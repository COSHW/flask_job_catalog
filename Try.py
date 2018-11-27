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


@app.route("/tools/db/<string:name>", methods=['OPTIONS'])
def make_table(name):
    cur.execute("create table IF NOT EXISTS " + name + " (id serial primary key, column_1 text, column_2 text)")
    conn.commit()
    return "Done! Table {} was created.".format(name)



@app.route("/tools/db/<string:name>", methods=['HEAD'])
def delete_table(name):
    cur.execute("drop table "+name)
    conn.commit()
    return "Done! Table {} was deleted.".format(name)


@app.route("/tools/db", methods=['HEAD'])
def show_tables():
    cur.execute("SELECT * FROM pg_catalog.pg_tables")
    result = cur.fetchall()
    return str(result[0])


if __name__ == "__main__":
    app.run()
