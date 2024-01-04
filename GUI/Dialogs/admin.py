import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLabel, QVBoxLayout, QLineEdit, QPlainTextEdit, \
    QTextEdit, QMainWindow
from PyQt5.uic import loadUi


class AdminDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("untitle.ui", self)
        self.btnYes.clicked.connect(self.save_password)
        self.password_input = QLineEdit()
        self.txtpassword.setEchoMode(QtWidgets.QLineEdit.Password)

    def save_password(self):
        password = self.txtpassword.toPlainText()
        print(password)
        self.accept()


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)

    # Create an instance of the AdminDialog and show it
    dialog = AdminDialog()
    dialog.show()

    # Execute the application's event loop
    sys.exit(app.exec_())
