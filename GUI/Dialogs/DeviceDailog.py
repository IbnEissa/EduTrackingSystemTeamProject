import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi


class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Load the dialog form created with Qt Designer
        loadUi("DeviceDialog.ui", self)
        self.btnSaveDevice.clicked.connect(self.save_data)
        self.btnCancelAddingDevice.clicked.connect(self.reject)
        self.txtIPAddress.installEventFilter(self)
        self.txtPortNumber.installEventFilter(self)
        self.setTabOrder(self.btnSaveDevice, self.btnCancelAddingDevice)

    def eventFilter(self, obj, event):
        if obj == self.txtIPAddress and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtPortNumber.setFocus()
            return True
        elif obj == self.txtPortNumber and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveDevice.setFocus()
            return True

        return super().eventFilter(obj, event)

    def save_data(self):
        try:
            ip_address = self.txtIPAddress.toPlainText()
            port_number = self.txtPortNumber.toPlainText()
            if port_number.strip() == "":
                raise ValueError("يجب ادخال عنوان Port الخاص بجهاز البصمة")
            if ip_address.strip() == "":
                raise ValueError("يجب ادخال عنوان IP الخاص بجهاز البصمة")
            self.accept()

            return ip_address, port_number

        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None
