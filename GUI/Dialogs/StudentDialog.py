import sys
from datetime import date
import re
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate

from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom


class StudentDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("studentDialog.ui", self)
        self.btnSaveStudent.clicked.connect(self.save_data)
        self.btnCancelAddingStudent.clicked.connect(self.reject)
        self.get_classes_combo_data()
        self.combClasses.currentIndexChanged.connect(self.comb_classes_changed)
        # تعيين ترتيب التنقل بين العناصر
        self.txtStudentFName.installEventFilter(self)
        # self.txtStudentSecName.installEventFilter(self)
        # self.txtStudentThirName.installEventFilter(self)
        self.txtStudentLName.installEventFilter(self)
        self.combClasses.installEventFilter(self)
        self.dateStudentDOB.installEventFilter(self)
        self.txtStudentParentPhone.installEventFilter(self)
        self.combStudentGender.installEventFilter(self)
        self.btnCloseDialog.clicked.connect(self.reject)
        self.setTabOrder(self.btnSaveStudent, self.btnCancelAddingStudent)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.FramelessWindowHint )

    def comb_classes_changed(self):
        class_name = self.combClasses.currentText()
        class_id = ClassRoom.get_class_id_from_name(self, class_name)
        return class_id

    def get_classes_combo_data(self):
        column_names = 'name'
        classes = Common.get_combo_box_data(self, ClassRoom, column_names)
        self.combClasses.clear()
        self.combClasses.addItems(classes)

    def eventFilter(self, obj, event):
        if obj == self.txtStudentFName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtStudentLName.setFocus()
            return True
        elif obj == self.txtStudentLName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtStudentParentPhone.setFocus()
            return True
        elif obj == self.txtStudentParentPhone and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateStudentDOB.setFocus()
            return True
        elif obj == self.dateStudentDOB and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.combClasses.setFocus()
            return True
        elif obj == self.combClasses and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveStudent.setFocus()
            return True
        elif obj == self.combClasses and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.combStudentGender.setFocus()
            return True
        elif obj == self.combStudentGender and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveStudent.setFocus()
            return True
        elif obj == self.btnSaveStudent and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnCancelAddingStudent.setFocus()
            return True
        elif obj == self.btnCancelAddingStudent and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtStudentFName.setFocus()
            return True
        return super().eventFilter(obj, event)

    def save_data(self):
        try:
            FName = self.txtStudentFName.toPlainText()
            LName = self.txtStudentLName.toPlainText()
            ClassId = self.comb_classes_changed()
            ClassName = self.combClasses.currentText()
            Birth = self.dateStudentDOB.date().toPyDate()
            Phone = self.txtStudentParentPhone.toPlainText()
            Gender = self.combStudentGender.currentText()
            if FName.strip() == "":
                raise ValueError("يجب ادخال الاسم الاول ")
            if LName.strip() == "":
                raise ValueError("يجب ادخال إسم اللقب ")
            if Birth > datetime.date.today():
                raise ValueError("تحذير", "يرجى إدخال تاريخ ميلاد صحيح للطالب")
            if Phone.strip() == "":
                raise ValueError("تحذير", "يرجى إدخال رقم هاتف ولي الأمر")
            if not re.match(r'^\d{9}$', Phone):
                raise ValueError("تحذير", "يرجى إدخال رقم ولي الأمر هاتف صحيح مؤلف من تسعة أرقام ")
            if Phone.strip() == "":
                raise ValueError("يجب ادخال رقم الهاتف ")
            if Gender.strip() == "":
                raise ValueError("يجب ادخال الجنس ")
            self.accept()
            return FName, LName, Gender, ClassId, Birth, Phone, ClassName

        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None
