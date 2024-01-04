from peewee import *
from models.BaseModel import BaseModel, db
from models.City import Cities
import mysql.connector
#
# conn = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='',
#     database='edutrackingsystemdb2'
# )


# def add_data():
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM directory")
#     dire = cursor.fetchall()
#     print(dire)
#     conn.close()
#     Directories.insert_many(dire).execute()


class Directories(BaseModel):
    city_id = ForeignKeyField(model=Cities, backref="city")
    name = CharField(max_length=30)


# db.create_tables([Directories])


# add_data()

###########################
# import datetime
# from peewee import Model, CharField, DateTimeField, ForeignKeyField, DoesNotExist
# from playhouse.mysql_ext import MySQLConnectorDatabase
# from models.City import Cities
#
# db = MySQLConnectorDatabase(None)
#
#
# class Directories(Model):
#     city_id = ForeignKeyField(model=Cities, backref="city")
#     name = CharField(max_length=30)
#
#     class Meta:
#         database = db
