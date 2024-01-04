import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from peewee import MySQLDatabase, Model, CharField

# Importing required libraries
import mysql.connector
from playhouse.db_url import connect


class BaseModel(Model):
    class Meta:
        database = None


class Student(BaseModel):
    name = CharField()
    age = CharField()


class Teacher(BaseModel):
    name = CharField()
    subject = CharField()


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

    import mysql.connector

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = DatabaseCreationWidget()
    widget.show()
    sys.exit(app.exec_())
