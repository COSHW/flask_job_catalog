import flask
import db

app = flask.Flask(__name__)


@app.route("/")
def welcome():
    return db.welcome()


@app.route("/tools/db/tablecontent/<string:table>", methods=["GET"])
def view(table):
    return db.view(table)


@app.route("/tools/db/maintain", methods=["GET"])
def get():
    return db.get()


@app.route("/tools/db/maintain/<int:id>", methods=["GET"])
def get_by_id(id):
    return db.get_by_id(id)


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
