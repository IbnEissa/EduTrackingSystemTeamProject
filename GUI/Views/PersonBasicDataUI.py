from datetime import datetime
import datetime
from functools import partial
import peewee
import re
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QAbstractItemView, QMainWindow, QHeaderView, QApplication
from PyQt5.QtCore import QDate
from django.contrib.admin.views.main import ERROR_FLAG
from peewee import OperationalError, MySQLDatabase

from GUI.Dialogs.TeacherDialog import TeacherDialog
from GUI.Views.CommonFunctionality import Common


# from models.PersonBasicData import PersonBasicData


class SubMain(QMainWindow):
    def __init__(self, ui_handler):
        super(SubMain, self).__init__()
        self.ui_handler = ui_handler
        self.ui = self.ui_handler.get_ui()
        Common.style_table_widget(self.ui, self.ui.tblStudents)

        # self.ui.setFixedSize(1700, 950)
        # self.ui.setGeometry(200, 100, 70, 500)
        # button.setStyleSheet("border: none;")
        # self.ui.tabWidget.tabBar().setVisible(False)

        # self.ui.pushButton_12.setStyleSheet(
        #     self.ui.pushButton_12.styleSheet() + "border: none; ")
        # self.ui.pushButton_6.setStyleSheet(
        #     self.ui.pushButton_6.styleSheet() + "border: none; ")
        #
        # self.ui.pushButton_13.setStyleSheet(
        #     self.ui.pushButton_13.styleSheet() + "border: none; ")
        # self.ui.pushButton_11.setStyleSheet(
        #     self.ui.pushButton_11.styleSheet() + "border: none; ")
