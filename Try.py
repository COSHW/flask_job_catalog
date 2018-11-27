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


@app.route("/tools/db/<string:name>", methods=["GET"])
def get(name):
    cur.execute("select * from "+name)
    result = cur.fetchall()
    return flask.jsonify({'items': result[0]})


@app.route("/tools/db/<string:name>/<int:id>", methods=["GET"])
def get_by_id(name, id):
    cur.execute("select * from "+name+" where id = " + str(id))
    result = cur.fetchall()
    return flask.jsonify({'items': result[0]})


@app.route("/tools/db/<string:name>/vlaues/<string:what>/<string:what2>", methods=['POST'])
def insert_into(name, what, what2):
    cur.execute("insert into " + name + " (column_1, column_2) values ('"+what+"', '"+what2+"')")
    conn.commit()
    cur.execute("select * from "+name)
    result = cur.fetchall()
    return flask.jsonify({'items': result[0]})


@app.route("/tools/db/<string:name>/vlaues/<string:what>/<string:what2>/whereid/<string:id>", methods=['POST'])
def update(name, what, what2, id):
    cur.execute("update " + name + " set column_1 = '"+what+"', column_2 = '"+what2+"' where id = " + id)
    conn.commit()
    cur.execute("select * from "+name)
    result = cur.fetchall()
    return flask.jsonify({'items': result[0]})


@app.route("/tools/db/<string:name>/whereid/<string:id>", methods=['DELETE'])
def delete(name, id):
    cur.execute("delete from "+name+"where id = "+id)
    conn.commit()
    cur.execute("select * from "+name)
    result = cur.fetchall()
    return flask.jsonify({'items': result[0]})


@app.route("/tools/db/createtable/<string:name>")
def make_table(name):
    cur.execute("create table IF NOT EXISTS " + name + " (id serial primary key, column_1 text, column_2 text)")
    conn.commit()
    return "Done! Table {} was created.".format(name)


@app.route("/tools/db/deletetable/<string:name>")
def delete_table(name):
    cur.execute("drop table "+name)
    conn.commit()
    return "Done! Table {} was deleted.".format(name)


@app.route("/tools/db/showalltables")
def show_tables():
    cur.execute("SELECT * FROM pg_catalog.pg_tables")
    result = cur.fetchall()
    return str(result[0])


if __name__ == "__main__":
    app.run()
