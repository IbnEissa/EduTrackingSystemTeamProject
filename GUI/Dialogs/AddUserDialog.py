import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate


class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("AddUserDialog.ui", self)
        self.btnAddUser.clicked.connect(self.save_data)
        self.cobAccountType.installEventFilter(self)
        self.txtUserName.installEventFilter(self)
        self.txtPassWord.installEventFilter(self)

        self.setTabOrder(self.btnSaveUser, self.btnCancelAddingUser)

    def eventFilter(self, obj, event):
        if obj == self.cobAccountType and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtUserName.setFocus()
            return True
        elif obj == self.txtUserName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtPassWord.setFocus()
            return True
        elif obj == self.txtPassWord and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveUser.setFocus()
            return True

        return super().eventFilter(obj, event)

    def save_data(self):
        try:
            typeAccount = self.cobAccountType.toPlainText()
            userName = self.txtUserName.toPlainText()
            passWord = self.txtPassWord.toPlainText()

            if typeAccount.strip() == "":
                raise ValueError("يجب ادخال نوع الحساب ")
            if userName.strip() == "":
                raise ValueError("يجب ادخال اسم المستخدم")
            if passWord.strip() == "":
                raise ValueError("يجب ادخال كلمة السر ")




        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None, None
