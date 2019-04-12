import flask
import db


app = flask.Flask(__name__)


@app.route("/")
def welcome():
    for key, value in flask.request.form.items():
        print("key: {0}, value: {1}".format(key, value))
    return flask.render_template("index.html")


@app.route("/chat", methods=["GET"])
def chat_get():
    return db.chat_get()


@app.route("/chat", methods=["POST"])
def chat_post():
    return db.chat_post()


@app.route("/chat", methods=["DELETE"])
def chat_reset():
    return db.reset()


@app.route("/tools/db/tablecontent/<string:table>", methods=["GET"])
def view(table):
    final = {}
    things = ""
    if table == "worker":
        for a in range(len(db.view(table))):
            final.update({db.view(table)[a][0]: {"surname": db.view(table)[a][1], "name": db.view(table)[a][2], "patronymic": db.view(table)[a][3],
                                         "house": db.view(table)[a][4], "phonenumber": db.view(table)[a][5], "payment": db.view(table)[a][6],
                                         "payday": db.view(table)[a][7]}})
        return flask.jsonify({"workers": final})
    elif table == "schedule":
        for a in range(len(db.view(table))):
            try:
                if db.view(table)[a][0] == db.view(table)[a + 1][0]:
                    things = things + db.view(table)[a][1] + ", "
                else:
                    things = things + db.view(table)[a][1] + ", "
                    final.update({db.view(table)[a][0]: {"schedule": things[:-2]}})
                    things = ""
            except:
                things = things + db.view(table)[a][1] + ", "
                final.update({db.view(table)[a][0]: {"schedule": things[:-2]}})
        return flask.jsonify({"schedules": final})
    elif table == "position":
        for a in range(len(db.view(table))):
            final.update({db.view(table)[a][0]: {"position": db.view(table)[a][1]}})
        return flask.jsonify({"positions": final})
    elif table == "worktime":
        for a in range(len(db.view(table))):
            try:
                if db.view(table)[a][0] == db.view(table)[a+1][0]:
                    things = things + db.view(table)[a][1] + ", "
                else:
                    things = things + db.view(table)[a][1] + ", "
                    final.update({db.view(table)[a][0]: {"worktime": things[:-2]}})
                    things = ""
            except:
                things = things + db.view(table)[a][1] + ", "
                final.update({db.view(table)[a][0]: {"worktime": things[:-2]}})
        return flask.jsonify({"worktime": final})
    else:
        return "No table called {}".format(table)


@app.route("/tools/db/maintain", methods=["GET"])
def get():
    schedule = ""
    schedules = []
    for a in range(len(db.get1())):
        try:
            if db.get1()[a][0] == db.get1()[a + 1][0]:
                schedule = schedule + db.get1()[a][1] + ", "
            else:
                schedule = schedule + db.get1()[a][1]
                schedules.append(schedule)
                schedule = ""
        except:
            schedule = schedule + db.get1()[a][1]
            schedules.append(schedule)
    worktime = ""
    worktimes = []
    for a in range(len(db.get2())):
        try:
            if db.get2()[a][0] == db.get2()[a + 1][0]:
                worktime = worktime + db.get2()[a][1] + ", "
            else:
                worktime = worktime + db.get2()[a][1]
                worktimes.append(worktime)
                worktime = ""
        except:
            worktime = worktime + db.get2()[a][1]
            worktimes.append(worktime)

    final = {}
    for a in range(len(db.get3())):
        final.update({db.get3()[a][0]: {"surname": db.get3()[a][1], "name": db.get3()[a][2], "patronymic": db.get3()[a][3], "house": db.get3()[a][4], "phonenumber": db.get3()[a][5], "payment": db.get3()[a][6], "payday": db.get3()[a][7], "schedule": schedules[a], "worktime": worktimes[a], "position": db.get3()[a][8]}})
    return flask.jsonify({"workers": final})


@app.route("/tools/db/maintain/<int:id>", methods=["GET"])
def get_by_id(id):
    schedule = ""
    schedules = []
    for a in range(len(db.get_by_id1())):
        schedule = schedule + db.get_by_id1()[a][1] + ", "
    schedules.append(schedule[:-2])

    worktime = ""
    worktimes = []
    for a in range(len(db.get_by_id2())):
        worktime = worktime + db.get_by_id2()[a][1] + ", "
    worktimes.append(worktime[:-2])

    final = {}
    final.update({db.get_by_id3()[0][0]: {"surname": db.get_by_id3()[0][1], "name": db.get_by_id3()[0][2], "patronymic": db.get_by_id3()[0][3], "house": db.get_by_id3()[0][4], "phonenumber": db.get_by_id3()[0][5], "payment": db.get_by_id3()[0][6], "payday": db.get_by_id3()[0][7], "schedule": schedules[0], "worktime": worktimes[0], "position": db.get_by_id3()[0][8]}})
    return flask.jsonify({"workers": final})



@app.route("/tools/db/maintain", methods=['POST'])
def insert_into():
    if not flask.request.json or not 'name' in flask.request.json or not 'surname' in flask.request.json:
        flask.abort(400)
    return db.insert_into()


@app.route("/tools/db/maintain/<string:id>", methods=['PUT'])
def update(id):
    if not flask.request.json or not 'name' in flask.request.json or not 'surname' in flask.request.json:
        flask.abort(400)
    return db.update(id)


@app.route("/tools/db/maintain/<string:id>", methods=['DELETE'])
def delete(id):
    return db.delete(id)


@app.route("/tools/db/createtable/worker")
def make_table1():
    return db.make_table_worker()


@app.route("/tools/db/createtable/schedule")
def make_table2():
    return db.make_table_schedule()


@app.route("/tools/db/createtable/position")
def make_table3():
    return db.make_table_position()
    
    
@app.route("/tools/db/createtable/worktime")
def make_table4():
    return db.make_table_worktime()


@app.route("/tools/db/deletetable/<string:db>")
def delete_table(db):
    return db.delete_table()


if __name__ == "__main__":
    app.run()
