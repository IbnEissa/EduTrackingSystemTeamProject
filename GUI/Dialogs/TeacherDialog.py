import sys
from datetime import date

import re

import peewee
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate
from zk import ZK

from GUI.Views.CommonFunctionality import Common
from models.Device import Device
from models.Members import Members
from models.Shifts import Shifts
from models.Teachers import Teachers


class TeacherDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("teacherDialog.ui", self)
        self.btnSaveTeacher.clicked.connect(self.save_data)
        # self.btnLoadFingersData.clicked.connect(self.save_data)
        self.btnCancelAddingTeacher.clicked.connect(self.reject)
        self.btnCloseDialog.clicked.connect(self.reject)
        self.lblTeacherID.setVisible(False)
        self.get_cities_combo_data()
        shift_names = [shift.name for shift in Shifts.select(Shifts.name)]
        for shift in shift_names:
            self.combShiftsType.addItem(shift)
        self.txtTeacherFName.installEventFilter(self)
        self.txtTeacherLName.installEventFilter(self)
        self.combTeatcherGendar.installEventFilter(self)
        self.combTeatcherCitye.installEventFilter(self)
        self.dateTeacherDOB.installEventFilter(self)
        self.txtTeacherPhone.installEventFilter(self)
        self.combShiftsType.installEventFilter(self)
        self.txtTeacherQualification.installEventFilter(self)
        self.dateTeacherDOQualification.installEventFilter(self)
        self.txtTeacherMajor.installEventFilter(self)
        self.txtTeacherExceperianceYears.installEventFilter(self)
        self.ComboTeacherTask.installEventFilter(self)
        self.setTabOrder(self.btnSaveTeacher, self.btnCancelAddingTeacher)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.FramelessWindowHint)

    def get_templates_data(self):
        lastInsertedTeacherId = Teachers.select(peewee.fn.Max(Teachers.member_id)).scalar()

    def get_cities_combo_data(self):
        cities = Common.get_cities(self)
        self.combTeatcherCitye.clear()
        self.combTeatcherCitye.addItems(cities)

    def eventFilter(self, obj, event):
        if obj == self.txtTeacherFName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtTeacherLName.setFocus()
            return True
        elif obj == self.txtTeacherLName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.combTeatcherGendar.setFocus()
            return True
        elif obj == self.combTeatcherGendar and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.combTeatcherCitye.setFocus()
            return True
        elif obj == self.combTeatcherCitye and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateTeacherDOB.setFocus()
            return True
        elif obj == self.dateTeacherDOB and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtTeacherPhone.setFocus()
            return True
        elif obj == self.txtTeacherPhone and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.combShiftsType.setFocus()
            return True
        elif obj == self.combShiftsType and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtTeacherQualification.setFocus()
            return True
        elif obj == self.txtTeacherQualification and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateTeacherDOQualification.setFocus()
            return True
        elif obj == self.dateTeacherDOQualification and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtTeacherMajor.setFocus()
            return True
        elif obj == self.txtTeacherMajor and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.ComboTeacherTask.setFocus()
            return True
        elif obj == self.ComboTeacherTask and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtTeacherExceperianceYears.setFocus()
            return True
        elif obj == self.txtTeacherExceperianceYears and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveTeacher.setFocus()
            return True
        return super().eventFilter(obj, event)

    def save_data(self):
        try:
            FName = self.txtTeacherFName.text()
            LName = self.txtTeacherLName.text()
            Gender = self.combTeatcherGendar.currentText()
            Cities = self.combTeatcherCitye.currentText()
            DOB = self.dateTeacherDOB.date().toPyDate()
            Phone = self.txtTeacherPhone.text()
            ShiftsType = self.combShiftsType.currentText()
            Qualification = self.txtTeacherQualification.text()
            DOQualification = self.dateTeacherDOQualification.date().toPyDate()
            Major = self.txtTeacherMajor.text()
            Task = self.ComboTeacherTask.currentText()
            state = self.ComboTeacherStatus.currentText()
            ExceperianceYears = self.txtTeacherExceperianceYears.text()
            fields = {
                "FName": "يجب ادخال الاسم الاول",
                "Qualification": "يجب ادخال المؤهل",
                "ExceperianceYears": "يجب ادخال سنوات الخبرة",
                "LName": "يجب ادخال اللقب",
                "Phone": "تحذير: يرجى إدخال رقم هاتف ولي الأمر",
                "Major": "يجب ادخال التخصص",
            }
            for field, error_message in fields.items():
                value = getattr(self, f"txtTeacher{field}").text().strip()
                if not value:
                    raise ValueError(error_message)

            self.accept()
            return FName, LName, Gender, Cities, DOB, Phone, Qualification, DOQualification, ShiftsType, Major, Task, ExceperianceYears, state
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None, None, None, None, None, None, None
