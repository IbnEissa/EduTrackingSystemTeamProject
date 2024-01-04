import sys

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

from GUI.Dialogs.UserLoginDialog import UserLoginDialog


class UserLogoutDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("UserLogoutDialog.ui", self)
        self.start_ui()
        self.state = False

    def start_ui(self):
        self.btnLogoutYes.clicked.connect(self.logout)
        self.btnLogoutNo.clicked.connect(self.reject)

    def logout(self):
        self.accept()
        from main import Main
        main = Main(1, False)
        main.main()
        # sys.exit(app.exec_())
