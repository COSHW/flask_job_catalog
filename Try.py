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


if __name__ == "__main__":
    app.run()
