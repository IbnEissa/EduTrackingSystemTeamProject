import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from playhouse.mysql_ext import MySQLConnectorDatabase
import mysql.connector

from models.Session import Department
from models.School import School


# from employee import Employee

class DatabaseCreationWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Create Database')
        self.setup_ui()

    def setup_ui(self):
        self.label = QLabel('Database Name:', self)
        self.label.move(20, 20)

        self.text_input = QLineEdit(self)
        self.text_input.move(120, 20)

        self.create_button = QPushButton('Create', self)
        self.create_button.move(120, 50)
        self.create_button.clicked.connect(self.create_database)

    def create_database(self):
        database_name = self.text_input.text()

        # Connect to MySQL server
        dataBase = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=""
        )

        # Create a cursor object
        cursorObject = dataBase.cursor()

        # Create database
        cursorObject.execute(f"CREATE DATABASE {database_name}")

        # Close the cursor and database connection
        cursorObject.close()
        dataBase.close()

        print(f"Database '{database_name}' created successfully!")

        # Connect to the newly created database
        db = MySQLConnectorDatabase(database=database_name, user="root", passwd="")

        # Set the database in the models
        Department._meta.database = db
        School._meta.database = db

        # Create tables
        with db:
            db.create_tables([Department, School])

        print("Tables created successfully!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DatabaseCreationWidget()
    widget.show()
    sys.exit(app.exec_())
###################################################
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
# from peewee import MySQLDatabase, Model, CharField
# from models.Students import Students
# # Importing required libraries
# import mysql.connector
#
#
# class DatabaseCreationWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Create Database')
#         self.setup_ui()
#
#     def setup_ui(self):
#         self.label = QLabel('Database Name:', self)
#         self.label.move(20, 20)
#
#         self.text_input = QLineEdit(self)
#         self.text_input.move(120, 20)
#
#         self.create_button = QPushButton('Create', self)
#         self.create_button.move(120, 50)
#         self.create_button.clicked.connect(self.create_database)
#
#     def create_database(self):
#         database_name = self.text_input.text()
#
#         # Connect to MySQL server
#         dataBase = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             passwd=""
#         )
#
#         # Create a cursor object
#         cursorObject = dataBase.cursor()
#
#         # Create database
#         cursorObject.execute(f"CREATE DATABASE {database_name}")
#
#         # Close the cursor and database connection
#         cursorObject.close()
#         dataBase.close()
#
#         print(f"Database '{database_name}' created successfully!")
#
#         # Connect to the newly created database
#         db = MySQLDatabase(database=database_name, user="root", passwd="")
#         Students._meta.database = db
#         # Teacher._meta.database = db
#
#         # Create an instance of AnotherClass
#         another_instance = Students()
#
#         # Call the create_table method
#         another_instance.create_table()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     widget = DatabaseCreationWidget()
#     widget.show()
#     sys.exit(app.exec_())
#
