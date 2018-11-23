import flask


app = flask.Flask(__name__)


@app.route("/<string:what>")
def index(what):
    return what


app.run()
