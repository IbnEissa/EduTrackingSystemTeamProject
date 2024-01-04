import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi

from GUI.Dialogs.InitializingTheProject.DialogsManager import DialogManager
from GUI.Dialogs.InitializingTheProject.classesDialog import ClassesDialog
from models.Device import Device
from models.School import School


class DeviceInitDialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.dialog_manager = dialog_manager
        loadUi("DeviceDialog2.ui", self)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.lastInsertedSchoolId = 0
        # self.btnSkippingDevice.clicked.connect(self.accept)

    # def accept(self):
    #     self.dialog_manager.push_dialog(ClassesDialog(DialogManager))

    def use_ui_elements(self):
        self.btnSaveDevice.clicked.connect(self.add_device_data)
        self.btnSkippingDevice.clicked.connect(self.skipping_dialog)

    def skipping_dialog(self):
        classes = ClassesDialog()
        classes.use_ui_elements()
        self.reject()
        classes.exec_()

    def add_device_data(self):
        name = self.txtDeviceName.toPlainText()
        ip = self.txtIPNumber.toPlainText()
        port = self.txtPortNumber.toPlainText()
        self.lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
        device = Device.add(self.lastInsertedSchoolId, name, ip, port, status='غير متصل')
        if device:
            self.accept()
            classes = ClassesDialog()
            classes.use_ui_elements()
            self.reject()
            classes.exec_()
        else:
            QMessageBox.warning(self, "Error", "Device not added")
