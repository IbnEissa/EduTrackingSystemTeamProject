import sys
from datetime import date
import re
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi
from datetime import datetime
import datetime
from PyQt5.QtCore import QDate
from PyQt5.QtCore import Qt, QEvent
from models.Members import Members
from PyQt5.QtCore import Qt, QEvent


class CouncilFathersDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Load the dialog form created with Qt Designer
        loadUi("CouncilFathersDialog.ui", self)
        self.btnSaveCouncil.clicked.connect(self.save_data)
        self.btnCancelAddingCouncil.clicked.connect(self.reject)
        self.btnCloseDialog.clicked.connect(self.reject)
        self.txtCouncilFatherfName.installEventFilter(self)
        self.txtCouncilLName.installEventFilter(self)
        self.txtCouncilPhone.installEventFilter(self)
        self.dateCouncilDOB.installEventFilter(self)
        self.txtCouncilOrganicStatus.installEventFilter(self)
        self.txtCouncilAddrress.installEventFilter(self)
        self.txtCouncilOrganicStatus.installEventFilter(self)
        self.combFatherGender.installEventFilter(self)
        self.setTabOrder(self.btnSaveCouncil, self.btnCancelAddingCouncil)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint | Qt.FramelessWindowHint)

    def eventFilter(self, obj, event):
        if obj == self.txtCouncilFatherfName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtCouncilLName.setFocus()
            return True

        elif obj == self.txtCouncilLName and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtCouncilPhone.setFocus()
            return True
        elif obj == self.txtCouncilPhone and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.dateCouncilDOB.setFocus()
            return True
        elif obj == self.dateCouncilDOB and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtCouncilSocialStatus.setFocus()
            return True
        elif obj == self.txtCouncilSocialStatus and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtCouncilAddrress.setFocus()
            return True
        elif obj == self.txtCouncilAddrress and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.txtCouncilOrganicStatus.setFocus()
            return True
        elif obj == self.txtCouncilOrganicStatus and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.combFatherGender.setFocus()
            return True
        elif obj == self.combFatherGender and event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.btnSaveCouncil.setFocus()
            return True
        return super().eventFilter(obj, event)

    def save_data(self):
        try:
            print("hello")
            CouncilFatherfName = self.txtCouncilFatherfName.toPlainText()
            CouncilLName = self.txtCouncilLName.toPlainText()
            CouncilPhone = self.txtCouncilPhone.toPlainText()
            CouncilDOB = self.dateCouncilDOB.date().toPyDate()
            CouncilSocialStatus = self.txtCouncilSocialStatus.toPlainText()
            CouncilAddrress = self.txtCouncilAddrress.toPlainText()
            CouncilOrgaincStatus = self.txtCouncilOrganicStatus.toPlainText()
            CouncilGender = self.combFatherGender.currentText()

            if CouncilFatherfName.strip() == "":
                raise ValueError("يجب ادخال الاسم  ")

            if CouncilLName.strip() == "":
                raise ValueError("يجب ادخال اللقب ")
            if CouncilDOB > datetime.date.today():
                raise ValueError("تحذير", "يرجى إدخال تاريخ ميلاد صحيح للطالب")
            if CouncilPhone.strip() == "":
                raise ValueError("تحذير", "يرجى إدخال رقم هاتف ولي الأمر")
            if not re.match(r'^\d{9}$', CouncilPhone):
                raise ValueError("تحذير", "يرجى إدخال رقم ولي الأمر هاتف صحيح مؤلف من تسعة أرقام ")
            if CouncilSocialStatus.strip() == "":
                raise ValueError("يجب ادخال الحالة الاجتماعية ")
            if CouncilAddrress.strip() == "":
                raise ValueError("يجب ادخال العنوان ")
            if CouncilOrgaincStatus.strip() == "":
                raise ValueError("يجب ادخال الحالة العضوية ")
            if CouncilGender.strip() == "":
                raise ValueError("يجب ادخال الجنس ")
                # existing_member = Members.select().where(
                #     (Members.fName == CouncilFathersName) &
                #
                #     (Members.lName == CouncilLName)
                # ).first()
                # if existing_member:
                #     raise ValueError("العضو موجوداً بالفعل ")
                # else:
            self.accept()
            return CouncilFatherfName, CouncilLName,CouncilGender, CouncilPhone, CouncilDOB, CouncilSocialStatus, CouncilAddrress, CouncilOrgaincStatus
        except Exception as e:
            # Display error message in a message box
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)
            return None, None, None, None, None, None, None, None
