import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate

from models.Members import Members
from models.Teachers import Teachers


class UserDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("newUser.ui", self)
        self.comboTeacherName.setEditable(True)
        self.get_teacher()
        self.btnSaveUser.clicked.connect(self.save_data)
        self.btnCancelAddingUser.clicked.connect(self.reject)
        self.comboTeacherName.installEventFilter(self)
        self.txtUserName.installEventFilter(self)
        self.txtPassword.installEventFilter(self)
        self.btnSaveUser.installEventFilter(self)
        self.btnCancelAddingUser.installEventFilter(self)
        self.setTabOrder(self.btnSaveUser, self.btnCancelAddingUser)

    def eventFilter(self, obj, event):
        if obj == self.comboTeacherName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtUserName.setFocus()
            return True
        elif obj == self.txtUserName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtPassword.setFocus()
            return True
        elif obj == self.txtPassword and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveUser.setFocus()
            return True

        return super().eventFilter(obj, event)

    def get_teacher(self):
        teacher_list = Teachers.select()
        for teacher in teacher_list:
            member = Members.get_by_id(teacher.member_id)
            self.comboTeacherName.addItem(member.fName + ' ' + member.lName)
            index = self.comboTeacherName.count() - 1
            self.comboTeacherName.setItemData(index, member.id, role=Qt.UserRole)

    def save_data(self):
        try:
            account_type = self.comboAccountType.currentText()
            name = self.comboTeacherName.currentText()
            user_name = self.txtUserName.toPlainText()
            password = self.txtPassword.toPlainText()

            if name.strip() == "":
                raise ValueError("يجب ادخال الاسم ")
            if user_name.strip() == "":
                raise ValueError("يجب ادخال إسم المستخدم ")
            if password.strip() == "":
                raise ValueError("يجب ادخال كلمة المرور ")
            self.accept()
            return account_type, name, user_name, password

        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None
