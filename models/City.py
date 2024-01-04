
# from peewee import *
# from models.BaseModel import BaseModel, db

# Establish a connection to the MySQL database
# conn = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='',
#     database='edutrackingsystemdb2'
# )


# Define the Cities model

# def add_data():
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM City")
#     cities = cursor.fetchall()
#     print(cities)
#     conn.close()
#     Cities.insert_many(cities).execute()


# class Cities(BaseModel):
#     name = CharField(max_length=20)
#
#
# db.create_tables([Cities])

# add_data()
