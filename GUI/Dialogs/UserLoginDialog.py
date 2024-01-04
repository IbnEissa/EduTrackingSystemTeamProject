import sys
from datetime import date

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QPushButton
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
from django.core.checks import database
from peewee import DoesNotExist, DatabaseError

from models.Users import Users
import login


class UserLoginDialog(login.Ui_Dialog, QDialog):
    def __init__(self):
        super().__init__()
        # loadUi("login.ui", self)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.ui.Users.update_state_to_false()
        self.message_box = QMessageBox()
        self.message_box.setStyleSheet("QMessageBox { background-color:white; color: black; }")
        button_stylesheet = "QPushButton { color: #FF0000; background-color: #FFFFFF; }"
        self.message_box.setStyleSheet(self.message_box.styleSheet() + button_stylesheet)
        ok_button = self.message_box.addButton(QMessageBox.Ok)
        ok_button.setText("موافق")

    def use_ui_elements(self):
        self.btnLoginUser.clicked.connect(self.login)
        self.btnClose.clicked.connect(self.close_dialog)

    def close_dialog(self):
        message_box = QMessageBox()
        message_box.setStyleSheet("QMessageBox { background-color: white; color: black; }")
        ok_button = QPushButton("موافق")
        cancel_button = QPushButton("إلغاء")
        message_box.addButton(ok_button, QMessageBox.AcceptRole)
        message_box.addButton(cancel_button, QMessageBox.RejectRole)
        message_box.setWindowTitle("تنبيه")
        message_box.setText("هل تريد الخروج حقاً؟")
        message_box.setIcon(QMessageBox.Warning)
        message_box.exec_()
        clicked_button = message_box.clickedButton()
        if clicked_button == ok_button:
            self.close()
        elif clicked_button == cancel_button:
            return

    def login(self):
        username = self.txtUserNameLogin.text()
        password = self.txtPasswordUserLogin.text()

        try:
            if not username or not password:
                self.message_box.warning(None, "فشل", "يجب تعبئة جميع الحقول!")
                return
            with Users.database.transaction():
                user = Users.get(Users.userName == username)

                if user.userPassword == password:
                    user.state = 'True'
                    Users.update(state='False').where(Users.userName == username).execute()
                    user.save()
                    self.accept()
                    return True, username
                else:
                    self.message_box.critical(None, "خطأ", "كلمة المرور غير صحيحة!")
                    # QMessageBox.warning(self, "فشل", "كلمة المرور غير صحيحة!")
        except DoesNotExist:
            self.message_box.warning(None, "فشل", "المستخدم غير موجود!")
        except DatabaseError:
            self.message_box.warning(None, "فشل", "خطأ في الاتصال بقاعدة البيانات")
        return False, None

    # def get_name_with_false_state(self):
    #     Users.update(state='False').where(Users.userName == username).execute()
    def eventFilter(self, obj, event):
        if obj == self.txtUserNameLogin and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtPasswordUserLogin.setFocus()
            return True
        elif obj == self.txtPasswordUserLogin and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnLoginUser.setFocus()
            return True
        return super().eventFilter(obj, event)
