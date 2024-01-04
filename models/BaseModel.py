from peewee import Model, MySQLDatabase


class BaseModel(Model):
    def fetch_database_name(self):
        with open("database_name.txt", "r") as file:
            database_name = file.read().strip()
        db = MySQLDatabase(database=database_name, user="root", password="")
        return db


#############################################
# from peewee import Model, MySQLDatabase
#
# db = MySQLDatabase('sssss_2023-12-06', user='root', password='',
#                    host='localhost')
#
#
# class BaseModel(Model):
#     class Meta:
#         database = db
