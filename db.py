import flask
import psycopg2
import os


DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()


def welcome():
    message = "Bonjoure! C'est mon application. Дальше не знаю."
    return message


def chat_get():
    final = {}
    cur.execute("select * from chat")
    result = cur.fetchall()
    for i in range(len(result)):
        final.update({str(i+1): {'nick': result[i][1], 'message': result[i][2]}})
    return flask.jsonify(final)


def chat_post():
    final = {}
    nick = flask.request.json['nick']
    message = flask.request.json['message']
    cur.execute("insert into chat (nick, message) values (%s, %s)", (nick, message))
    conn.commit()
    cur.execute("select * from chat")
    result = cur.fetchall()
    for i in range(len(result)):
        final.update({str(i+1): {'nick': result[i][1], 'message': result[i][2]}})
    return flask.jsonify(final)


def view(db):
    if db == "worker":
        cur.execute("select * from " + db)
        result = cur.fetchall()
        return result
    elif db == "schedule":
        cur.execute("select * from " + db)
        result = cur.fetchall()
        return result
    elif db == "position":
        cur.execute("select * from " + db)
        result = cur.fetchall()
        return result
    elif db == "worktime":
        cur.execute("select * from " + db)
        result = cur.fetchall()
        return result
    else:
        return "No table called {}".format(db)


def get1():
    cur.execute("select * from schedule")
    result = cur.fetchall()
    return result


def get2():
    cur.execute("select * from worktime")
    result = cur.fetchall()
    return result


def get3():
    cur.execute("select worker.id, worker.surname, worker.name, worker.patronymic, worker.house, worker.phonenumber, worker.payment, worker.payday, position.position from worker inner join position on worker.position=position.id")
    result = cur.fetchall()
    return result


def get_by_id1(id):
    cur.execute("select * from schedule where workerid = %s", (id, ))
    result = cur.fetchall()
    return result


def get_by_id2(id):
    cur.execute("select * from worktime where workerid = %s", (id, ))
    result = cur.fetchall()
    return result


def get_by_id3(id):
    cur.execute("select worker.id, worker.surname, worker.name, worker.patronymic, worker.house, worker.phonenumber, worker.payment, worker.payday, position.position from worker inner join position on worker.position=position.id where worker.id = %s", (id, ))
    result = cur.fetchall()
    return result


def insert_into():
    surname = flask.request.json['surname']
    name = flask.request.json['name']
    patronymic = flask.request.json['patronymic']
    schedule = flask.request.json['schedule'].split(", ")
    worktime = flask.request.json['worktime'].split(", ")
    phonenumber = flask.request.json['phonenumber']
    position = flask.request.json['position']
    payment = flask.request.json['payment']
    payday = flask.request.json['payday']
    house = flask.request.json['house']
    cur.execute("select * from position")
    res = cur.fetchall()
    for a in range(len(res)):
        if position in res:
            pass
        else:
            cur.execute("insert into position (position) values ('"+position+"')")
    cur.execute("insert into worker (surname, name, patronymic, house, phonenumber, payment, payday, position) values ('"+surname+"', '"+name+"', '"+patronymic+"', '"+house+"', '"+phonenumber+"', '"+payment+"', '"+payday+"', (select position.id from position where position = '"+position+"' limit 1))")
    conn.commit()
    for a in range(len(schedule)):
        cur.execute("insert into schedule (workerid, schedule) values ((select id from worker where surname like '"+surname+"' and name like '"+name+"' and patronymic like '"+patronymic+"' limit 1), '"+schedule[a]+"')")
        conn.commit()
    for a in range(len(worktime)):
        cur.execute("insert into worktime (workerid, worktime) values ((select id from worker where surname like '"+surname+"' and name like '"+name+"' and patronymic like '"+patronymic+"' limit 1), '"+worktime[a]+"')")
        conn.commit()
    return "Done!"


def update(id):
    surname = flask.request.json['surname']
    name = flask.request.json['name']
    patronymic = flask.request.json['patronymic']
    schedule = flask.request.json['schedule'].split(", ")
    worktime = flask.request.json['worktime'].split(", ")
    phonenumber = flask.request.json['phonenumber']
    position = flask.request.json['position']
    payment = flask.request.json['payment']
    payday = flask.request.json['payday']
    house = flask.request.json['house']
    cur.execute("select * from position")
    res = cur.fetchall()
    for a in range(len(res)):
        if position in res:
            pass
        else:
            cur.execute("insert into position (position) values ('"+position+"')")

    cur.execute(
        "update worker set surname = '" + surname + "', name = '" + name + "', patronymic = '" + patronymic + "', house = '" + house + "', phonenumber = '"+phonenumber+"', payment = '"+payment+"', payday = '"+payday+"', position = (select position.id from position where position = '"+position+"' limit 1) where id = " + id)
    conn.commit()
    cur.execute("delete from schedule where workerid = " + id)
    conn.commit()
    for a in range(len(schedule)):
        cur.execute("insert into schedule (workerid, schedule) values ((select id from worker where surname like '"+surname+"' and name like '"+name+"' and patronymic like '"+patronymic+"' limit 1), '"+schedule[a]+"')")
    conn.commit()
    cur.execute("delete from worktime where workerid = " + id)
    conn.commit()
    for a in range(len(worktime)):
        cur.execute("insert into worktime (workerid, worktime) values ((select id from worker where surname like '"+surname+"' and name like '"+name+"' and patronymic like '"+patronymic+"' limit 1), '"+worktime[a]+"')")
        conn.commit()
    return "Done!"


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


def reset():
    cur.execute("drop table if exists chat")
    conn.commit()
    cur.execute("create table chat (id serial primary key, nick text, message text)")
    conn.commit()
    cur.execute("insert into chat (nick, message) values ('Система', 'Введите своё сообщение в поле ниже и нажмите отправить')")
    conn.commit()
    return "Done!"
