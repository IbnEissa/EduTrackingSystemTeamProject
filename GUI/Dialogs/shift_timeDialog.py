import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent, QTime
from PyQt5.QtGui import QKeyEvent
from PyQt5.uic import loadUi


class Shift_timedialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("shiftDialog.ui", self)
        self.btnSaveshift.clicked.connect(self.shifts_parameters)
        self.btnCancelAddingshift.clicked.connect(self.reject)

        self.txtshift_name.installEventFilter(self)
        self.dateStartShift.installEventFilter(self)
        self.dateEndShift.installEventFilter(self)

        self.setTabOrder(self.btnSaveshift, self.btnCancelAddingshift)

    def eventFilter(self, obj, event):
        if obj == self.txtshift_name and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateStartShift.setFocus()
            return True
        elif obj == self.dateStartShift and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateEndShift.setFocus()
            return True

        elif obj == self.dateEndShift and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveshift.setFocus()
        elif obj == self.btnSaveshift and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnCancelAddingshift.setFocus()
            return True
        elif obj == self.btnCancelAddingshift and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtshift_name.setFocus()
            return True
        return super().eventFilter(obj, event)

    def shifts_parameters(self):
        name = self.txtshift_name.toPlainText()
        start_shift = self.dateStartShift.date().toPyDate()
        end_shift = self.dateEndShift.date().toPyDate()
        self.save_data_shift(name, start_shift,end_shift)

    def save_data_shift(self,name, start_shift,end_shift):
        try:

            if name == "":
                raise ValueError("يجب ادخال اسم الوردية ")
            if start_shift == "":
                raise ValueError("تحذير", "يرجى إدخال تاريخ فترة البداية")
            if end_shift == "":
                raise ValueError("تحذير", "يرجى إدخال تاريخ فترة النهاية")

            self.accept()
            return name, start_shift, end_shift

        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None
