import flask
import requests
from bs4 import BeautifulSoup
import pandas


all_info = []

req = requests.get("http://prokazan.ru/news/")
cont = req.content
soup = BeautifulSoup(cont, "html.parser")
news = soup.find_all("div", {"id": "RedColumn"})
info1 = news[0].find_all("div", {"class": "news-mid__content"})

times = news[0].find_all("div", {"class": "news-mid__date"})
j = 0
for item in info1:
    link50 = []
    title = []
    d = list()
    d.append("ProKazan")
    for a in item.find_all('a', title=True):
        title = a['title']
    d.append(title)
    time = times[j].text.replace("\n", "")
    d.append(time)
    for a in info1[j].find_all('a', href=True):
        link50.append("http://prokazan.ru" + a['href'])
    d.append(link50[0]+"\n")
    all_info.append(d)
    j += 1

df = pandas.DataFrame(all_info)
columns = ["Источник", "Заголовок", "Время", "Ссылка"]
df.columns = columns

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route('/success', methods=['POST'])
def success():
    return flask.render_template("index2.html", text=df.to_html(index=False))


app.run()
