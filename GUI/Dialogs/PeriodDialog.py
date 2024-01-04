import sys

import peewee
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt, QEvent, QTime
from PyQt5.QtGui import QKeyEvent
from PyQt5.uic import loadUi

from models.Periods import Periods


class PeriodDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Period.ui", self)

        self.btnSaveperiod.clicked.connect(self.save_data_period)
        self.btnCancelAddingperiod.clicked.connect(self.reject)

        self.combPeriodName.installEventFilter(self)
        self.timeAttendanceTime.installEventFilter(self)
        self.timeLeavingTime.installEventFilter(self)

        self.txtPricePeriod.installEventFilter(self)
        self.timeAllowedTimeForAttendance.installEventFilter(self)
        self.timeAllowedTimeForLeaving.installEventFilter(self)

        self.setTabOrder(self.btnSaveperiod, self.btnCancelAddingperiod)

    # def use_ui_elements(self):
    #     self.btnSaveperiod.clicked.connect(self.save_data_period)
    #     self.btnCancelAddingperiod.clicked.connect(self.reject)

    def eventFilter(self, obj, event):
        if obj == self.combPeriodName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.timeAttendanceTime.setFocus()
            return True
        elif obj == self.timeAttendanceTime and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.timeLeavingTime.setFocus()
            return True
        elif obj == self.timeLeavingTime and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtPricePeriod.setFocus()
            return True
        elif obj == self.txtPricePeriod and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.timeAllowedTimeForAttendance.setFocus()
            return True
        elif obj == self.timeAllowedTimeForAttendance and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.timeAllowedTimeForLeaving.setFocus()
            return True
        elif obj == self.timeAllowedTimeForLeaving and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveperiod.setFocus()
            return True

        elif obj == self.btnSaveperiod and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnCancelAddingperiod.setFocus()
            return True

        elif obj == self.btnCancelAddingperiod and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.combPeriodName.setFocus()
            return True
        return super().eventFilter(obj, event)

    def save_data_period(self):
        try:
            NamePeriod = self.combPeriodName.currentText()
            AttendanceTime = self.timeAttendanceTime.time().toPyTime()
            LeavingTime = self.timeLeavingTime.time().toPyTime()
            PricePeriod = self.txtPricePeriod.toPlainText()
            AllowedTimeForAttendance = self.timeAllowedTimeForAttendance.toPlainText()
            AllowedTimeForLeaving = self.timeAllowedTimeForLeaving.toPlainText()

            entry_start_time_str = AttendanceTime.strftime('%H:%M')
            entry_end_time_str = LeavingTime.strftime('%H:%M')

            if NamePeriod == "":
                raise ValueError("يجب ادخال الاسم ")
            if AttendanceTime == "":
                raise ValueError("يجب ادخال  وقت بداية الدخول ")
            if LeavingTime == "":
                raise ValueError("يجب ادخال  وقت نهاية الدخول ")
            if PricePeriod == "":
                raise ValueError("يجب ادخال  سعر الفترة ")
            if not AllowedTimeForAttendance.isdigit():
                raise ValueError("يجب إدخال قيمة رقمية لسماحية وقت الحضور")
            if not AllowedTimeForLeaving.isdigit():
                raise ValueError("يجب إدخال قيمة رقمية لسماحية  وقت الانصراف ")

            self.accept()
            return NamePeriod, entry_start_time_str, entry_end_time_str, PricePeriod, AllowedTimeForAttendance, AllowedTimeForLeaving


        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None
