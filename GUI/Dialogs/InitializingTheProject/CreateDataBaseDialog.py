import sys

import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QDialog, QMessageBox
from PyQt5.uic import loadUi
from playhouse.mysql_ext import MySQLConnectorDatabase
import mysql.connector
from models.AbsentExcuse import AbsentExcuse
from models.Periods import Periods
from models.Teachers_Schedule import Teachers_Schedule
from models.Attendance import AttendanceModel
from models.BoardFathers import BoardFathers
from models.ClassRoom import ClassRoom
from models.CouncilFathers import CouncilFathers
from models.Device import Device
from models.Members import Members
from models.Permissions import Permissions
from models.School import School
from models.Session import Session
from models.Students import Students
from models.Subjects import Subjects
from models.System_screen import SystemScreens
from models.TeacherShifts import TeacherShifts
from models.Teachers import Teachers
from models.Users import Users
from models.Weekly_class_schedule import WeeklyClassSchedule
from models.fingerPrintData import FingerPrintData
from models.Shifts import Shifts
from models.term_table import TeacherSubjectClassRoomTermTable
import mysql.connector
from PyQt5.QtCore import Qt
import datetime
import mysql.connector


# from models.Session import Department
# from models.School import School


class CreateDataBaseDialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.dialog_manager = dialog_manager
        loadUi("create_databaseDialog.ui", self)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.lastInsertedUserId = 0
        self.btnConnectoinDataBase.hide()
        self.checkShowDatabaseExists.hide()
        self.btnCancelConnectDatabase.hide()

    def use_ui_elements(self):
        self.btnCreateDataBase.clicked.connect(self.create_database)
        self.btnConnectoinDataBase.clicked.connect(self.connect_database)
        self.btnCancelConnectDatabase.clicked.connect(self.cancel_connect_database)
        self.checkShowDatabaseExists.stateChanged.connect(self.on_checkbox_state_changed)

    # def skipping_dialog(self):
    #     self.close()

    def create_database(self):
        # self.self.combDataBaseInitialize.setEditable(True)
        self.btnConnectoinDataBase.hide()
        # try:
        database_name = self.combDataBaseInitialize.currentText()
        if database_name.strip() == "":
            raise ValueError("يجب ادخال أسم قاعدة البيانات ")

        # Connect to MySQL server
        dataBase = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=""
        )

        # Create a cursor object
        cursorObject = dataBase.cursor()

        # Combine current date with database name
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        database_name_with_date = f"{database_name}_{current_date}"

        # Create database
        cursorObject.execute(f"CREATE DATABASE `{database_name_with_date}`")

        # Close the cursor and database connection
        cursorObject.close()
        dataBase.close()

        # Connect to the newly created database
        db = MySQLConnectorDatabase(database=database_name_with_date, user="root", passwd="")
        with open("database_name.txt", "w") as file:
            file.write(database_name_with_date)

        # Set the database in the models
        School._meta.database = db
        ClassRoom._meta.database = db
        Device._meta.database = db
        Users._meta.database = db
        Permissions._meta.database = db
        Session._meta.database = db
        Shifts._meta.database = db
        Subjects._meta.database = db
        SystemScreens._meta.database = db
        TeacherSubjectClassRoomTermTable._meta.database = db
        Members._meta.database = db
        BoardFathers._meta.database = db
        CouncilFathers._meta.database = db
        Students._meta.database = db
        Teachers._meta.database = db
        AbsentExcuse._meta.database = db
        FingerPrintData._meta.database = db
        TeacherShifts._meta.database = db
        Periods._meta.database = db
        AttendanceModel._meta.database = db
        WeeklyClassSchedule._meta.database = db
        Teachers_Schedule._meta.database = db


        # Create tables
        with db:
            db.create_tables([School, Teachers_Schedule, ClassRoom,
                              Device, Users, Permissions, Session, Shifts,
                              Subjects, SystemScreens, TeacherSubjectClassRoomTermTable, Members,
                              BoardFathers, CouncilFathers,
                              Students, Teachers, FingerPrintData, TeacherShifts, AttendanceModel,
                              WeeklyClassSchedule, Periods,AbsentExcuse])
            # Add default user
            default_user = Users(
                account_type='مسؤول',
                Name='admin',
                userName='admin',
                userPassword='777',
                state='False',
                initialization='False'
            )
            default_user.save()

            # Get the ID of the last inserted user
            last_inserted_user_id = default_user.id

            # Add permissions for the default user
            permissions = Permissions(
                users_id=last_inserted_user_id,
                led_main=True,
                led_manage=True,
                led_setting=True,
                bt_save_student=True,
                bt_search_student=True,
                bt_update_student=True,
                bt_delete_student=True,
                bt_export_student=True,
                bt_show_student=True,
                bt_reports_student=True,
                bt_save_teacher=True,
                bt_search_teacher=True,
                bt_update_teacher=True,
                bt_delete_teacher=True,
                bt_export_teacher=True,
                bt_show_teacher=True,
                bt_reports_teacher=True,
                bt_save_fathers=True,
                bt_search_fathers=True,
                bt_update_fathers=True,
                bt_delete_fathers=True,
                bt_save_user=True,
                bt_search_user=True,
                bt_update_user=True,
                bt_delete_user=True,
                bt_save_device=True,
                bt_search_device=True,
                bt_update_device=True,
                bt_delete_device=True,
                bt_export_device=True,
                bt_show_device=True,
                bt_save_attendance=True,
                bt_search_attendance=True,
                bt_update_attendance=True,
                bt_delete_attendance=True,
                bt_export_attendance=True,
                bt_show_attendance=True,
                bt_save_timetable_student=True,
                bt_show_timetable_student=True,
                bt_export_timetable_student=True,
                bt_show_timetable_teacher=True
                # bt_save_timetable_teacher=False,
                # bt_export_timetable_teacher=False,
            )
            permissions.save()

        QMessageBox.information(self, "نجاح",
                                f"تم انشاء قاعدة البيانات {database_name_with_date} بنجاح وتم حفظ اسمها في ملف نصي")

        # QMessageBox.information(self, "نجاح", "تم انشاء جداول قاعدة البيانات بنجاح")

        self.close()
        # except Exception as e:
        #     # Display error message in a message box
        #     error_message = "حدث خطأ:\n\n" + str(e)
        #     QMessageBox.critical(self, "خطأ", error_message)

    def on_checkbox_state_changed(self, state):
        if state == Qt.Checked:
            self.btnCreateDataBase.hide()

            # Connect to the MySQL server
            # self.btnConnectoinDataBase.show()
            cnx = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd=""
            )
            cursor = cnx.cursor()

            # Execute the query to get the list of databases
            cursor.execute("SHOW DATABASES")

            # Fetch all the database names
            databases = [row[0] for row in cursor.fetchall()]

            # Clear the current items in the combobox
            self.combDataBaseInitialize.clear()

            # Add the database names to the combobox
            self.combDataBaseInitialize.addItems(databases)

            # Close the cursor and connection
            cursor.close()
            cnx.close()
        else:
            # Clear the combobox when the checkbox is unchecked
            self.combDataBaseInitialize.clear()

    def connect_database(self):
        # self.btnCancelConnectDatabase.show()

        database_name = self.combDataBaseInitialize.currentText()
        # Save database_name to a text file
        with open("database_name.txt", "w") as file:
            file.truncate(0)  # Clear the file contents
            file.write(database_name)
        QMessageBox.information(self, "نجاح",
                                f"تم الاتصال بقاعدة البيانات {database_name} بنجاح يمكنك تسجيل الخروج من النظام للعمل عليها ",
                                QMessageBox.No | QMessageBox.Yes)

    def cancel_connect_database(self):
        self.close()
