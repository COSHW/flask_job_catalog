import flask
import psycopg2
import os


DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()


def welcome():
    message = "Bonjoure! C'est mon application. Дальше не знаю."
    return message


def view(db):
    final = {}
    if db == "worker":
        cur.execute("select * from " + db)
        result = cur.fetchall()
        for a in range(len(result)):
            final.update({result[a][0]: {"surname": result[a][1], "name": result[a][2], "patronymic": result[a][3], "house": result[a][4], "phonenumber": result[a][5], "payment": result[a][6], "payday": result[a][7]}})
        return flask.jsonify({"workers": final})
    elif db == "schedule":
        cur.execute("select * from " + db)
        result = cur.fetchall()
        print(result)
        for a in range(len(result)):
            final.update({result[a][0]: {"schedule": [items for items in result[a][1]]}})
        return flask.jsonify({"schedules": final})
    elif db == "position":
        cur.execute("select * from " + db + "where")
        result = cur.fetchall()
        for a in range(len(result)):
            final.update({result[a][0]: {"position": result[a][1]}})
        return flask.jsonify({"positions": final})
    elif db == "worktime":
        cur.execute("select * from " + db)
        result = cur.fetchall()
        for a in range(len(result)):
            final.update({result[a][0]: {"worktime": [items for items in result[a][1]]}})
        return flask.jsonify({"worktime": final})
    else:
        return "No table called {}".format(db)


def get():
    cur.execute("select worker.id, worker.surname, worker.name, worker.patronymic, worker.house, worker.phonenumber, worker.payment, worker.payday, schedule.schedule, worktime.worktime, position.position from worker inner join schedule on worker.id=schedule.workerid inner join worktime on worker.id=worktime.workerid inner join position on worker.position=position.id")
    result = cur.fetchall()
    final = {}
    for a in range(len(result)):
        final.update({result[a][0]: {"surname": result[a][1], "name": result[a][2], "patronymic": result[a][3], "house": result[a][4], "phonenumber": result[a][5], "payment": result[a][6], "payday": result[a][7], "schedule": [items for items in result[a][8]], "worktime": [items for items in result[a][9]], "position": result[a][10]}})
    return flask.jsonify({"workers": final})


def get_by_id(id):
    cur.execute("select worker.id, worker.surname, worker.name, worker.patronymic, worker.house, worker.phonenumber, worker.payment, worker.payday, schedule.schedule, worktime.worktime, position.position from worker inner join schedule on worker.id=schedule.workerid inner join worktime on worker.id=worktime.workerid inner join position on worker.position=position.id where id = " + str(id))
    result = cur.fetchall()
    final = {}
    final.update({result[0][0]: {"surname": result[0][1], "name": result[0][2], "patronymic": result[0][3], "house": result[0][4], "phonenumber": result[0][5], "payment": result[0][6], "payday": result[0][7], "schedule": result[0][8], "worktime": result[0][9], "position": result[0][10]}})
    return flask.jsonify({"items": final})


def insert_into():
    surname = flask.request.json['surname']
    name = flask.request.json['name']
    patronymic = flask.request.json['patronymic']
    schedule = flask.request.json['schedule']
    worktime = flask.request.json['worktime']
    phonenumber = flask.request.json['phonenumber']
    position = flask.request.json['position']
    payment = flask.request.json['payment']
    payday = flask.request.json['payday']
    house = flask.request.json['house']
    cur.execute("insert into worker (surname, name, patronymic, house, phonenumber, payment, payday, position) values ('"+surname+"', '"+name+"', '"+patronymic+"', '"+house+"', '"+phonenumber+"', '"+payment+"', '"+payday+"', "+str(position)+")")
    conn.commit()
    for a in range(len(schedule)):
        cur.execute("insert into schedule (workerid, schedule) values ((select id from worker where surname like '"+surname+"' and name like '"+name+"' and patronymic like '"+patronymic+"' limit 1), '"+schedule[a]+"')")
        conn.commit()
    for a in range(len(worktime)):
        cur.execute("insert into worktime (workerid, worktime) values ((select id from worker where surname like '"+surname+"' and name like '"+name+"' and patronymic like '"+patronymic+"' limit 1), '"+worktime[a]+"')")
        conn.commit()
    return "Done!"


"""
def update(id):
    surname = flask.request.json['surname']
    name = flask.request.json['name']
    patronymic = flask.request.json['patronymic']
    house = flask.request.json['house']
    cur.execute(
        "update worker set surname = '" + surname + "', name = '" + name + "', patronymic = '" + patronymic + "', house = '" + house + "' where id = " + id)
    conn.commit()
    schedule = flask.request.json['schedule']
    worktime = flask.request.json['worktime']
    phonenumber = flask.request.json['phonenumber']
    cur.execute(
        "update worker set schedule = '" + schedule + "', worktime = '" + worktime + "', phonenumber = '" + phonenumber + "' where id = " + id)
    conn.commit()
    position = flask.request.json['position']
    payment = flask.request.json['payment']
    payday = flask.request.json['payday']
    cur.execute(
        "update worker set position = '" + position + "', payment = '" + payment + "', payday = '" + payday + "' where id = " + id)
    conn.commit()
    return "Done!"
"""


def delete(id):
    cur.execute("delete from schedule where workerid = "+id)
    cur.execute("delete from worktime where workerid = "+id)
    cur.execute("delete from worker where id = "+id)
    conn.commit()
    return "Done!"


def delete_table(table):
    cur.execute("drop table "+table)
    conn.commit()
    return "Done!"


def make_table_worker():
    cur.execute("create table IF NOT EXISTS worker (id serial primary key, surname text, name text, patronymic text, house text, phonenumber text, payment text, payday text, position int, foreign key (position) references position(id))")
    conn.commit()
    return "Done! Table worker was created."


def make_table_schedule():
    cur.execute("create table IF NOT EXISTS schedule (workerid int, schedule text, foreign key (workerid) references worker(id))")
    conn.commit()
    return "Done! Table schedule was created."


def make_table_worktime():
    cur.execute("create table if not exists worktime (workerid int, worktime text, foreign key (workerid) references worker(id))")
    conn.commit()
    return "Done! Table worktime was created."


def make_table_position():
    cur.execute("create table IF NOT EXISTS position (id serial primary key, position text)")
    conn.commit()
    positions = ["Администратор гостиницы", "Администратор кафе", "Администратор ресторана",
                 "Администратор салона красоты", "Аккаунт-менеджер", "Бизнес-аналитик", "Бухгалтер", "Инкассатор",
                 "Кассир", "Кредитный инспектор", "Мерчендайзер", "Метролог", "Пресс-секретарь", "Продавец-консультант",
                 "Промоутер", "Супервайзер", "Товаровед", "Торговый представитель", "Финансовый консультант",
                 "Экономист", "Архивариус", "Ученый секретарь", "Директор магазина", "Генеральный директор",
                 "Арт-директор", "Начальник отдела продаж", "Бизнес-тренер", "Инженер по пожарной безопасности",
                 "Актуарий", "Андеррайтер", "Страховой агент", "Логист", "Дальнобойщик", "Адвокат", "Нотариус",
                 "Судебный эксперт", "Юрисконсульт", "Юрист", "Главный редактор", "Звукорежиссер", "Журналист",
                 "Кинооператор", "Корректор", "Корреспондент", "Продюсер", "Телеведущий", "Сценарист",
                 "Агент по недвижимости", "Риэлтор", "Косметолог"]
    for item in positions:
        cur.execute("insert into position (position) values (%s)", (item, ))
    return "Done! Table position was created."


