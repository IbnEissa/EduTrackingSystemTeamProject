import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QCompleter
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi

from models.AbsentExcuse import AbsentExcuse
from models.Members import Members
from models.Teachers import Teachers
from models.Shifts import Shifts


class ExecutionsDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Load the dialog form created with Qt Designer
        loadUi("excuseAttendenceDialog.ui", self)
        self.btnSaveExecution.clicked.connect(self.save_data)
        self.btnCancelAddingExecution.clicked.connect(self.reject)
        self.dateOfAbsent.installEventFilter(self)
        self.combTeachersNames.installEventFilter(self)
        self.radioAllEmps.installEventFilter(self)
        self.radioSingleEmp.installEventFilter(self)
        self.txtExecutionReason.installEventFilter(self)
        self.radioSingleEmp.setChecked(True)
        for teacher in Teachers.select():
            member_data = Members.get_by_id(teacher.member_id)
            teacher_name = f"{member_data.fName} {member_data.lName}"
            self.combTeachersNames.addItem(teacher_name)
            item_index = self.combTeachersNames.count() - 1
            self.combTeachersNames.setItemData(item_index, teacher.member_id)
        self.execution_type = ''
        self.setTabOrder(self.btnSaveExecution, self.btnCancelAddingExecution)
        # make the text searchable in combobox
        self.combTeachersNames.setEditable(True)
        completer = QCompleter(self.combTeachersNames.model())
        self.combTeachersNames.setCompleter(completer)
        self.radioAllEmps.toggled.connect(self.on_radio_all_state_changed)

    def on_radio_all_state_changed(self, checked):
        if checked:
            self.execute_method_when_checked()
        else:
            self.execute_method_when_unchecked()

    def execute_method_when_checked(self):
        self.combTeachersNames.setEnabled(False)
        self.combTeachersNames.setStyleSheet("QComboBox { background-color: rgb(25, 21, 59); color: #333333; }")

    def execute_method_when_unchecked(self):
        self.combTeachersNames.setEnabled(True)

        self.combTeachersNames.setStyleSheet(
            "QComboBox { background-color: rgb(25, 21, 59); color:rgb(255, 255, 255); font-family:'PT Bold Heading';font-size:19px;font-weight:bold; }")

    def eventFilter(self, obj, event):
        if obj == self.radioAllEmps and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateOfAbsent.setFocus()
            return True
        elif obj == self.dateOfAbsent and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtExecutionResone.setFocus()
            return True

        return super().eventFilter(obj, event)

    def save_data(self):
        try:
            absent_date = self.dateOfAbsent.date().toPyDate()
            execution_reason = self.txtExecutionReason.toPlainText()
            if execution_reason.strip() == "":
                raise ValueError("يجب كتابة سبب الفياب")
            if self.radioAllEmps.isChecked():
                self.execution_type = 'all'
                self.accept()
                return self.execution_type, absent_date, execution_reason
            else:
                teacher_name = self.combTeachersNames.currentText()
                selected_index = self.combTeachersNames.currentIndex()
                selected_id = self.combTeachersNames.itemData(selected_index)
                self.execution_type = 'single'
                self.accept()
                return self.execution_type, absent_date, selected_id, teacher_name, execution_reason
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None
