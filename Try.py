import flask
import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

app = flask.Flask(__name__)


@app.route("/")
def welcome():
    message = "Bonjoure! C'est mon application. Дальше не знаю."
    return message


@app.route("/tools/db/tablecontent/<string:db>", methods=["GET"])
def view(db):
    final = {}
    if db == "worker":
        cur.execute("select * from " + db)
        result = cur.fetchall()
        for a in range(len(result)):
            final.update({result[a][0]: {"surname": result[a][1], "name": result[a][2], "patronymic": result[a][3], "house": result[a][4]}})
        return flask.jsonify({"workers": final})
    elif db == "schedule":
        cur.execute("select * from " + db)
        result = cur.fetchall()
        for a in range(len(result)):
            final.update({result[a][0]: {"schedule": result[a][1], "worktime": result[a][2], "phonenumber": result[a][3]}})
        return flask.jsonify({"schedules": final})
    elif db == "position":
        cur.execute("select * from " + db)
        result = cur.fetchall()
        for a in range(len(result)):
            final.update({result[a][0]: {"position": result[a][1], "payment": result[a][2], "payday": result[a][3]}})
        return flask.jsonify({"positions": final})
    else:
        return "No table called {}".format(db)


@app.route("/tools/db/maintain", methods=["GET"])
def get():
    cur.execute("select worker.*, schedule.schedule, schedule.worktime, schedule.phonenumber, position.position, position.payment, position.payday from worker inner join schedule on worker.id=schedule.workerid inner join position on worker.id=position.workerid")
    result = cur.fetchall()
    final = {}
    for a in range(len(result)):
        final.update({result[a][0]: {"surname": result[a][1], "name": result[a][2], "patronymic": result[a][3], "house": result[a][4], "schedule": result[a][5], "worktime": result[a][6], "phonenumber": result[a][7], "position": result[a][8], "payment": result[a][9], "payday": result[a][10]}})
    return flask.jsonify({"workers": final})


@app.route("/tools/db/maintain/<int:id>", methods=["GET"])
def get_by_id(id):
    cur.execute("select worker.*, schedule.schedule, schedule.worktime, schedule.phonenumber, position.position, position.payment, position.payday from worker inner join schedule on worker.id=schedule.workerid inner join position on worker.id=position.workerid where id = " + str(id))
    result = cur.fetchall()
    final = {}
    final.update({result[0][0]: {"surname": result[0][1], "name": result[0][2], "patronymic": result[0][3],
                                 "house": result[0][4], "schedule": result[0][5], "worktime": result[0][6],
                                 "phonenumber": result[0][7], "position": result[0][8], "payment": result[0][9],
                                 "payday": result[0][10]}})
    return flask.jsonify({"items": final})


@app.route("/tools/db/maintain", methods=['POST'])
def insert_into():
    if not flask.request.json or not 'name' in flask.request.json or not 'surname' in flask.request.json:
        flask.abort(400)
    surname = flask.request.json['surname']
    name = flask.request.json['name']
    patronymic = flask.request.json['patronymic']
    house = flask.request.json['house']
    cur.execute("insert into worker (surname, name, patronymic, house) values ('"+surname+"', '"+name+"', '"+patronymic+"', '"+house+"')")
    conn.commit()
    schedule = flask.request.json['schedule']
    worktime = flask.request.json['worktime']
    phonenumber = flask.request.json['phonenumber']
    cur.execute("insert into schedule (workerid, schedule, worktime, phonenumber) values ((select id from worker where surname like '"+surname+"' and name like '"+name+"' and patronymic like '"+patronymic+"' limit 1), '"+schedule+"', '"+worktime+"', '"+phonenumber+"')")
    conn.commit()
    position = flask.request.json['position']
    payment = flask.request.json['payment']
    payday = flask.request.json['payday']
    cur.execute("insert into position (workerid, position, payment, payday) values ((select id from worker where surname like '"+surname+"' and name like '"+name+"' and patronymic like '"+patronymic+"' limit 1), '"+position+"', '"+payment+"', '"+payday+"')")
    conn.commit()
    return "Done!"


@app.route("/tools/db/maintain/<string:id>", methods=['PUT'])
def update(id):
    if not flask.request.json or not 'name' in flask.request.json or not 'surname' in flask.request.json:
        flask.abort(400)
    surname = flask.request.json['surname']
    name = flask.request.json['name']
    patronymic = flask.request.json['patronymic']
    house = flask.request.json['house']
    cur.execute("update worker set surname = '"+surname+"', name = '"+name+"', patronymic = '"+patronymic+"', house = '"+house+"' where id = "+id)
    conn.commit()
    schedule = flask.request.json['schedule']
    worktime = flask.request.json['worktime']
    phonenumber = flask.request.json['phonenumber']
    cur.execute("update worker set schedule = '"+schedule+"', worktime = '"+worktime+"', phonenumber = '"+phonenumber+"' where id = "+id)
    conn.commit()
    position = flask.request.json['position']
    payment = flask.request.json['payment']
    payday = flask.request.json['payday']
    cur.execute("update worker set position = '"+position+"', payment = '"+payment+"', payday = '"+payday+"' where id = "+id)
    conn.commit()
    return "Done!"


@app.route("/tools/db/maintain/<string:id>", methods=['DELETE'])
def delete(id):
    cur.execute("delete from worker where id = "+id)
    conn.commit()
    return "Done!"



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


@app.route("/tools/db/deletetable/<string:db>")
def delete_table(db):
    cur.execute("drop table "+db)
    conn.commit()
    return "Done!"


if __name__ == "__main__":
    app.run()
