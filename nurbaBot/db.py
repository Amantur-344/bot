from datetime import datetime

import mysql.connector

from nurbaBot.setting import HOST, USER, PASSWORD, DATABASE

mydb = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    database=DATABASE
)

mycursor = mydb.cursor()


def insert_table(user_id, user_name):
    mycursor.execute("SELECT user_id FROM telegram_users_id")
    myresult = mycursor.fetchall()

    if len(myresult) == 0:
        sql = "INSERT INTO telegram_users_id (user_id, user_name) VALUES (%s, %s)"
        val = (user_id, user_name)
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        for id in myresult:
            str_id = ''.join(id)  # Превращаем в строку что бы можно было сравнивть
            if str_id == user_id:
                break
            else:
                sql = "INSERT INTO telegram_users_id (user_id, user_name) VALUES (%s, %s)"
                val = (user_id, user_name)
                mycursor.execute(sql, val)
                mydb.commit()
                break


def insert_poster(category, name, address, date_time, text, location):
    try:
        sql = "INSERT INTO poster (category, name, address, date_time, text, location) VALUES(%s, %s, %s, %s, %s, %s)"
        val = (category, name, address, date_time, text, location)
        mycursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.errors.DataError:
        return 0
    return mycursor.rowcount  # Возвращать при успешной загрузке


def select_poster():
    mycursor.execute("SELECT * FROM poster")
    return mycursor.fetchall()


def select_category():
    sql = 'SELECT DISTINCT category FROM poster'
    mycursor.execute(sql)

    my_result = mycursor.fetchall()

    category = []
    for ctg in my_result:
        category.append(ctg)
    return category


def select_category_where(category):
    sql = 'SELECT * FROM poster WHERE category = %s'
    ctg = (category,)
    mycursor.execute(sql, ctg)

    my_result = mycursor.fetchall()

    return my_result


def beautifully_poster(my_result):
    article_poster = {}

    for article in my_result:
        d_now = datetime.today()
        d_poster = article[4]

        if (d_poster - d_now).days >= -1:  # Что бы показвал афишу еще день после его начало
            id = str(article[0])
            article_poster['id' + id] = article[0]
            article_poster['category' + id] = article[1]
            article_poster['name' + id] = article[2]
            article_poster['address' + id] = article[3]

            t = article[4]
            date_time = t.strftime('%d/%b  %H:%M')
            article_poster['date_time' + id] = date_time

            article_poster['text' + id] = article[5]
            article_poster['location' + id] = article[6]
        else:
            sql = "DELETE FROM poster WHERE id = %s"
            id_delete = (article[0],)
            mycursor.execute(sql, id_delete)

            mydb.commit()
            print(mycursor.rowcount, "record(s) deleted")

    return article_poster

# def select_category_poster(category):
#     sql = 'SELECT * FROM poster WHERE category = %s'
#     ctg = (category, )
#
#     my_result = mydb.fetchall()
#
#     for x in my_result:
#         return

# def create_file_id(telegram_id = ''):
#     mycursor.execute("SELECT telegram_id FROM telegram_users")
#     myresult = mycursor.fetchall()
#
#     if myresult > 0:
#         for id in myresult:
#             if id == telegram_id:
#                 break
#             else:
#                 sql = "INSERT INTO telegram_users (telegram_id) VALUES (%s)"
#                 mycursor.execute(sql, telegram_id)
#     else:
#         sql = "INSERT INTO telegram_users (telegram_id) VALUES (%s)"
#         mycursor.execute(sql, telegram_id)
