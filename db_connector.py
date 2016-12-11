# -*- coding: utf-8 -*-
# import sqlite3 as db
import psycopg2 as db
from os import environ

# host = environ['POSTGRESQL_SERVICE_HOST']
c = db.connect("host='ec2-54-247-119-94.eu-west-1.compute.amazonaws.com'"
               "dbname='dbaj1fb1ian3ve' "
               "user='zlkllrubxwxjik' "
               "password='EH_UQI5UZMpBpBJb7t7f-Xabfn'")
# c = db.connect("host='%s'"
#                "dbname='sampledb' "
#                "user='userL0G' "
#                "password='iXMTnXJnPhOCGn4Q'" % host)
# c = db.connect(database="luckyhandbot.db", check_same_thread=False)

sql = c.cursor()


def sql_select(cols, table, condition):
    query = "SELECT %s FROM %s WHERE %s;" % (cols, table, condition)
    # print query
    sql.execute(query)
    try:
        return sql.fetchall()[0]
    except IndexError:
        return None,

# try:
#     sql.execute(
#         CREATE TABLE user (id
#     #     """
#     #     CREATE TABLE "user" (
#     #         `id`	INTEGER PRIMARY KEY AUTOINCREMENT,
#     #         `user_id`	INTEGER NOT NULL,
#     #         `name`	TEXT NOT NULL,
#     #         `state`	TEXT,
#     #         `lang`	TEXT,
#     #         `diamond`	INTEGER,
#     #         `dollar`	REAL,
#     #         `rouble`	REAL,
#     #         `last_game_time`	TEXT,
#     #         `last_game_currency`	TEXT,
#     #         `last_game_id`	INTEGER,
#     #         `diamond_request_time`	TEXT,
#     #         `ik_num`	INTEGER NOT NULL DEFAULT 0,
#     #         `referral_user_id`	INTEGER
#     #     );
#     # """
#     )
# except db.DatabaseError as x:
#     print("Ошибка: ", x)
# # c.commit()
# # c.close()
# try:
#     sql.execute("""
#         CREATE TABLE "feedback" (
#             `id`	INTEGER PRIMARY KEY AUTOINCREMENT,
#             `feedback_user_id`	INTEGER NOT NULL,
#             `date`	TEXT NOT NULL,
#             `text`	TEXT,
#             `author`	INTEGER NOT NULL,
#             `author_name`	TEXT NOT NULL,
#             `message_id`	INTEGER,
#             `query_id`	INTEGER
#         );
#     """)
# except db.DatabaseError as x:
#     print("Ошибка: ", x)
# # c.commit()
# # c.close()
# try:
#     sql.execute("""
#         CREATE TABLE "game" (
#             `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             `opponent1_id`	INTEGER,
#             `opponent2_id`	INTEGER,
#             `opponent1_choose`	TEXT,
#             `opponent2_choose`	TEXT,
#             `start_time`	TEXT
#         );
#     """)
# except db.DatabaseError as x:
#     print("Ошибка: ", x)
# c.commit()
# c.close()
# try:
#     sql.execute("""
#         CREATE TABLE "add_balance_requests" (
#             `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             `admin_user_id`	INTEGER NOT NULL,
#             `user_id`	INTEGER NOT NULL,
#             `sum`	REAL,
#             `currency`	TEXT,
#             `date`	TEXT,
#             `done`	INTEGER NOT NULL DEFAULT 0
#         );
#     """)
# except db.DatabaseError as x:
#     print("Ошибка: ", x)
# c.commit()
# c.close()
