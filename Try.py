import flask
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

app = flask.Flask(__name__)


@app.route("/")
def welcome():
    message = "Bonjoure! C'est mon application. Дальше не знаю. \n Ссылки для манимуляций с датабазой: \n     https://romanrestplz.herokuapp.com/tools/db/maintain/<database name> ([GET, POST]) \n    https://romanrestplz.herokuapp.com/tools/db/maintain/<database name> ([GET, PUT, DELETE])"
    return message


@app.route("/<string:db>/tools/db/maintain", methods=["GET"])
def get(db):
    cur.execute("select * from "+db)
    result = cur.fetchall()
    final = {}
    for a in range(len(result)):
        final.update({result[a][0]: {"name": result[a][1], "surname": result[a][2]}})
    return flask.jsonify({"items": final})


@app.route("/<string:db>/tools/db/maintain/<int:id>", methods=["GET"])
def get_by_id(db, id):
    cur.execute("select * from "+db+" where id = " + str(id))
    result = cur.fetchall()
    final = {}
    final.update({result[0][0]: {"name": result[0][1], "surname": result[0][2]}})
    return flask.jsonify({"items": final})


@app.route("/<string:db>/tools/db/maintain", methods=['POST'])
def insert_into(db):
    if not flask.request.json or not 'name' in flask.request.json or not 'surname' in flask.request.json:
        flask.abort(400)
    name = flask.request.json['name']
    surname = flask.request.json['surname']
    cur.execute("insert into " + db + " (column_1, column_2) values ('"+name+"', '"+surname+"')")
    conn.commit()
    cur.execute("select * from "+db)
    result = cur.fetchall()
    final = {}
    for a in range(len(result)):
        final.update({result[a][0]: {"name": result[a][1], "surname": result[a][2]}})
    return flask.jsonify({"items": final})


@app.route("/<string:db>/tools/db/maintain/<string:id>", methods=['PUT'])
def update(db, id):
    if not flask.request.json or not 'name' in flask.request.json or not 'surname' in flask.request.json:
        flask.abort(400)
    name = flask.request.json['name']
    surname = flask.request.json['surname']
    cur.execute("update " + db + " set column_1 = '"+name+"', column_2 = '"+surname+"' where id = " + id)
    conn.commit()
    cur.execute("select * from "+db)
    result = cur.fetchall()
    final = {}
    for a in range(len(result)):
        final.update({result[a][0]: {"name": result[a][1], "surname": result[a][2]}})
    return flask.jsonify({"items": final})



@app.route("/<string:db>/tools/db/maintain/<string:id>", methods=['DELETE'])
def delete(db, id):
    cur.execute("delete from "+db+" where id = "+id)
    conn.commit()
    cur.execute("select * from "+db)
    result = cur.fetchall()
    final = {}
    for a in range(len(result)):
        final.update({result[a][0]: {"name": result[a][1], "surname": result[a][2]}})
    return flask.jsonify({"items": final})


@app.route("/tools/db/createtable/worker")
def make_table1():
    cur.execute("create table IF NOT EXISTS worker (id serial primary key, surname text, name text, patronymic text, house text)")
    conn.commit()
    return "Done! Table {} was created."


@app.route("/tools/db/createtable/schedule")
def make_table2():
    cur.execute("create table IF NOT EXISTS schedule (workerid int, schedule text, worktime text, phonenumber text, foreign key (workerid) references worker(id))")
    conn.commit()
    return "Done! Table {} was created."


@app.route("/tools/db/createtable/position")
def make_table3():
    cur.execute("create table IF NOT EXISTS position (workerid int, position text, payment text, payday text, foreign key (workerid) references worker(id))")
    conn.commit()
    return "Done! Table {} was created."



@app.route("/tools/db/showalltables")
def show_tables():
    cur.execute("SELECT * FROM pg_catalog.pg_tables")
    result = cur.fetchall()
    return flask.jsonify({'items': str([item[1] for item in result[:-69]])})


if __name__ == "__main__":
    app.run()
