from peewee import *

# Connect to a MySQL database on network.
db = MySQLDatabase('school', user='root', password='',
                   host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db


db.connect()
