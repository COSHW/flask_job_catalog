import flask


app = flask.Flask(__name__)


@app.route("/<string:what>", methods=["GET"])
def index(what):
    return what


@app.route("/<string:no>", methods=["POST"])
def index2(no):
    return no


app.run()
