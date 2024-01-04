import peewee
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QListWidgetItem
from PyQt5.uic import loadUi

from GUI.Dialogs.InitializingTheProject.TermSessionsInit import TermSessionsInit
from models.ClassRoom import ClassRoom
from models.Members import Members
from models.School import School
from models.Teachers import Teachers


class ClassesDialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.dialog_manager = dialog_manager
        loadUi("ChaptersDataDialog.ui", self)
        self.get_teacher()
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.lastInsertedSchoolId = 0
        self.btnSaveClasses.hide()
        self.btnCancelAddingClasses.hide()
        self.btnSaveClass.hide()
        self.btnSkipClasses.hide()
        self.btnSaveClasses.clicked.connect(self.save_data)
        self.btnSaveClass.clicked.connect(self.add_new_classroom)
        self.btnCancelAddingClasses.clicked.connect(self.reject)
        self.btnSkipClasses.clicked.connect(self.skipping_classes)

        # تعيين ترتيب التنقل بين العناصر
        self.txtClassName.installEventFilter(self)
        self.comboMajorName.installEventFilter(self)
        self.setTabOrder(self.btnSaveClasses, self.btnCancelAddingClasses)

    def eventFilter(self, obj, event):
        if obj == self.txtClassName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.comboMajorName.setFocus()
            return True
        elif obj == self.comboMajorName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveClasses.setFocus()
            return True

        elif obj == self.btnSaveClasses and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnCancelAddingClasses.setFocus()
            return True
        elif obj == self.btnCancelAddingClasses and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtClassName.setFocus()
            return True
        return super().eventFilter(obj, event)

    def get_teacher(self):
        teacher_list = Teachers.select()
        for teacher in teacher_list:
            member = Members.get_by_id(teacher.member_id)
            self.comboMajorName.addItem(member.fName + ' ' + member.lName)
            index = self.comboMajorName.count() - 1
            self.comboMajorName.setItemData(index, member.id, role=Qt.UserRole)

    def save_data(self):
        try:
            class_name = self.txtClassName.text()
            major_name = self.comboMajorName.currentText()
            if class_name.strip() == "":
                raise ValueError("يجب ادخال الصف ")
            if major_name.strip() == "":
                raise ValueError("يجب ادخال إسم رائد الفصل ")

            self.accept()
            return class_name, major_name
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None

    #
    def skipping_classes(self):
        term = TermSessionsInit()
        term.use_ui_elements()
        self.reject()
        term.exec_()

    def add_new_classroom(self, class_name, major_name):
        try:

            if class_name.strip() == "":
                raise ValueError("يجب ادخال الصف ")
            if major_name.strip() == "":
                major_name = "غير معروف"
                self.comboMajorName.setCurrentText(major_name)

            self.accept()
            return class_name, major_name
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)