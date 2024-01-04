import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi

from GUI.Dialogs.InitializingTheProject.TeachersInit import TeachersInit
from models.Device import Device
from models.School import School
from models.Subjects import Subjects


class SubjectsDialog(QDialog):
    def __init__(self):
        super().__init__()
        # self.dialog_manager = dialog_manager
        loadUi("MaterialDataDialog.ui", self)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        # self.btnSkipSubjects.clicked.connect(self.accept)

    # def accept(self):
    #     self.dialog_manager.pop_dialog()

    def use_ui_elements(self):
        self.btnSaveSubjects.clicked.connect(self.add_subjects_data)
        self.btnAddSubject.clicked.connect(self.add_to_list)
        self.btnDeleteSubject.clicked.connect(self.delete_from_list)
        self.btnSkipSubjects.clicked.connect(self.skipping_subjects)

    def skipping_subjects(self):
        teachers = TeachersInit()
        teachers.use_ui_elements()
        self.reject()
        teachers.exec_()

    def add_to_list(self):
        name = self.txtSubjectName.toPlainText()
        self.listSubjects.addItem(name)

    def delete_from_list(self):
        self.listSubjects.takeItem(self.listSubjects.currentRow())

    def add_subjects_data(self):
        subject_added = False

        for row in range(self.listSubjects.count()):
            item = self.listSubjects.item(row)
            name = item.text()
            subjects = Subjects.add([name])

            if subjects:
                subject_added = True  # Set the flag to True
            else:
                QMessageBox.warning(self, "Error", "Subject not added")

        if subject_added:
            self.accept()
            # subjects = SubjectsDialog()
            # subjects.use_ui_elements()
            # subjects.exec_()
