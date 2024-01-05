import os
from datetime import datetime

import peewee
from PyQt5.QtWidgets import QApplication, QTableWidget, QWidget, QVBoxLayout, QPushButton, QDialog, \
    QTableWidgetItem, QMessageBox, QStyle, QToolButton
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtCore import Qt, QDate, QTime, QDateTime, QSize
from PyQt5.uic.uiparser import QtCore
from zk import ZK
from zk.exception import ZKErrorResponse

from GUI.Dialogs.PeriodDialog import PeriodDialog
from GUI.Dialogs.RejesterTeacherFingerDialog import RejesterTeacherFingerDialog
from GUI.Dialogs.shift_timeDialog import Shift_timedialog
from GUI.Views.CommonFunctionality import Common
from GUI.Dialogs.CouncilFathersDialog import CouncilFathersDialog
from GUI.Dialogs.DeviceDailog import MyDialog
from GUI.Dialogs.InitializingTheProject.DeviceInintDialog import DeviceInitDialog
from GUI.Dialogs.InitializingTheProject.SchoolDialog import SchoolDialog
from GUI.Dialogs.InitializingTheProject.classesDialog import ClassesDialog
from GUI.Dialogs.TeacherDialog import TeacherDialog
import logging
import codecs

from GUI.Dialogs.UserDialog import UserDialog
from GUI.Views.PersonBasicDataUI import SubMain
from GUI.Views.uihandler import UIHandler
from models.ClassRoom import ClassRoom
from models.CouncilFathers import CouncilFathers
from models.Device import Device
from models.Members import Members
from GUI.Dialogs.DeviceDailog import MyDialog
from GUI.Dialogs.TeacherDialog import TeacherDialog
from GUI.Dialogs.StudentDialog import StudentDialog
from models.Members import Members
from models.Periods import Periods
from models.School import School
from models.Students import Students
from models.Teachers import Teachers
from models.Teachers_Schedule import Teachers_Schedule
from models.Users import Users
from models.Shifts import Shifts
from models.term_table import TeacherSubjectClassRoomTermTable


# lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()


class DeleteUpdateButtonInitClassRoomWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تفاصيل")
        self.delete_button.setFixedSize(110, 40)
        self.update_button.setStyleSheet(
            "QPushButton {  background-color:none;color:rgb(255, 255, 255);font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.delete_button.setStyleSheet(
            "QPushButton { background-color: none; color:red;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.update_button.setFixedSize(110, 40)
        self.delete_button.setFixedSize(110, 40)
        self.delete_button.setIcon(QIcon("icons_rc/delete-svgrepo-com.svg"))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.setLayoutDirection(Qt.LeftToRight)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setIconSize(QSize(24, 24))
        self.update_button.setIcon(QIcon("icons_rc/assigned-person-edit.svg"))
        self.update_button.setLayoutDirection(Qt.LeftToRight)
        # layout
        layout.addSpacing(3)
        layout.addWidget(self.update_button)
        layout.addSpacing(3)
        layout.addWidget(self.delete_button)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.update_button.clicked.connect(self.on_update_button_classroom_clicked)

    def on_delete_button_clicked(self):
        # result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_student")
        # if result_condition is True:
        print("on_delete_button_clicked")
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                # Fetch the user with the selected ID from the database
                class_id = self.table_widget.item(row, 0)
                get_id = class_id.text()
                try:
                    classroom = ClassRoom.get_by_id(get_id)

                    # Show confirmation message box
                    reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الصف",
                                                 QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        print(classroom)
                        self.table_widget.removeRow(row)
                        classroom.delete_instance()
                        QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                except Members.DoesNotExist:
                    print("Student does not exist.")
        # else:
        #     QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_update_button_classroom_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()

                # Fetch the school with the selected ID from the database
                classroom_id = self.table_widget.item(row, 0)
                name = self.table_widget.item(row, 1)
                major_name = self.table_widget.item(row, 2)

                if classroom_id and name and major_name:
                    classroom_dialog = ClassesDialog()
                    classroom_dialog.btnSaveClasses.show()
                    classroom_dialog.btnCancelAddingClasses.show()
                    classroom_dialog.labAddClassRoom.setVisible(False)
                    classroom_dialog.labAddClassRoom.setText(classroom_id.text())
                    classroom_dialog.txtClassName.setText(name.text())  # Use 'setText' instead of 'setPlainText'
                    classroom_dialog.comboMajorName.setEditText(major_name.text())

                    if classroom_dialog.exec_() == QDialog.Accepted:
                        name_class = classroom_dialog.txtClassName.text()  # Assuming you want to retrieve plain text
                        name_major = classroom_dialog.comboMajorName.currentText()

                        # Update the row in the table_widget with the new data
                        self.table_widget.setItem(row, 1, QTableWidgetItem(name_class))
                        self.table_widget.setItem(row, 2, QTableWidgetItem(name_major))

                        # Fetch the user with the selected ID from the database
                        class_id = classroom_dialog.labAddClassRoom.text()
                        class_room = ClassRoom.get_by_id(class_id)
                        class_room.name = name_class
                        class_room.Name_major = name_major
                        class_room.save()

                        QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")


class DeleteUpdateButtonInitDeviceWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget

        layout = QVBoxLayout()

        self.update_button = QPushButton("تفاصيل")
        self.update_button.setStyleSheet(
            "QPushButton {  background-color:none;color:rgb(255, 255, 255);font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.update_button.setFixedSize(110, 40)
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setIconSize(QSize(24, 24))
        self.update_button.setIcon(QIcon("icons_rc/assigned-person-edit.svg"))
        self.update_button.setLayoutDirection(Qt.LeftToRight)
        layout.addSpacing(3)
        layout.addWidget(self.update_button)
        layout.addSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.update_button.clicked.connect(self.on_update_button_device_clicked)

    def on_update_button_device_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()

                device_id = self.table_widget.item(row, 0)
                print("the device id is: ", device_id.text())

                name = self.table_widget.item(row, 1)
                ip = self.table_widget.item(row, 2)
                port = self.table_widget.item(row, 3)

                if device_id and name and ip and port:
                    device_dialog = DeviceInitDialog()
                    device_dialog.labAddDivece.setVisible(False)
                    device_dialog.btnSkippingDevice.setVisible(False)
                    device_dialog.btnSaveDevice.setVisible(False)
                    device_dialog.btnSaveInitDevice.setVisible(True)
                    device_dialog.btnCancelInitDevice.setVisible(True)

                    device_dialog.labAddDivece.setText(device_id.text())
                    device_dialog.txtDeviceName.setPlainText(name.text())
                    device_dialog.txtIPNumber.setPlainText(ip.text())
                    device_dialog.txtPortNumber.setPlainText(port.text())

                    device_dialog.btnSaveInitDevice.clicked.connect(lambda: self.on_button_clicked(device_dialog, row))
                    device_dialog.btnCancelInitDevice.clicked.connect(lambda: self.close_dialog(device_dialog))

                    if device_dialog.exec_() == QDialog.Accepted:
                        pass

    def on_button_clicked(self, device_dialog, row):

        name = device_dialog.txtDeviceName.toPlainText()
        ip = device_dialog.txtIPNumber.toPlainText()
        port = device_dialog.txtPortNumber.toPlainText()

        self.table_widget.setItem(row, 1, QTableWidgetItem(name))
        self.table_widget.setItem(row, 2, QTableWidgetItem(ip))
        self.table_widget.setItem(row, 3, QTableWidgetItem(port))

        device_id = device_dialog.labAddDivece.text()
        print(device_id)

        device = Device.get(Device.id == device_id)
        device.name = name
        device.ip = ip
        device.port = port

        device.save()

        QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
        device_dialog.close()

    def close_dialog(self, device_dialog):
        device_dialog.close()


class DeleteUpdateButtonSchoolWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        self.school_dialog = SchoolDialog()
        layout = QVBoxLayout()

        self.update_button = QPushButton("تفاصيل")
        self.update_button.setStyleSheet(
            "QPushButton {  background-color:none;color:rgb(255, 255, 255);font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.update_button.setFixedSize(110, 40)
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setIconSize(QSize(24, 24))
        self.update_button.setIcon(QIcon("icons_rc/assigned-person-edit.svg"))
        self.update_button.setLayoutDirection(Qt.LeftToRight)
        layout.addSpacing(3)
        layout.addWidget(self.update_button)
        layout.addSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.update_button.clicked.connect(self.on_update_button_school_clicked)

    def on_update_button_school_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()

                school_id = self.table_widget.item(row, 0)
                print("the school id is: ", school_id.text())

                school_name = self.table_widget.item(row, 1)
                city = self.table_widget.item(row, 2)
                directorate = self.table_widget.item(row, 3)
                print("the directorate is : ", directorate)
                print("the directorate is : ", city)
                village = self.table_widget.item(row, 4)
                academic_level = self.table_widget.item(row, 5)
                student_gender_type = self.table_widget.item(row, 6)

                if school_id and school_name and city and village and academic_level and directorate \
                        and student_gender_type:

                    school_dialog = SchoolDialog()
                    school_dialog.labAddSchool.setVisible(False)
                    school_dialog.btnSaveSchool.setVisible(False)
                    school_dialog.btnUpdateSchool.setVisible(True)
                    school_dialog.btnCancelSchool.setVisible(True)
                    school_dialog.labAddSchool.setText(school_id.text())
                    school_dialog.txtSchoolName.setPlainText(school_name.text())
                    school_dialog.comboCity.setCurrentText(city.text())
                    school_dialog.combDirectorates.setCurrentText(directorate.text())
                    school_dialog.comboCity.currentIndexChanged.connect(school_dialog.on_city_select)
                    # school_dialog.combDirectorates.currentIndexChanged.connect(school_dialog.on_city_select)
                    # school_dialog.txtVillage.setPlainText(village.text())
                    school_dialog.comboAcademicLevel.setCurrentText(academic_level.text())
                    school_dialog.comboGenderType.setCurrentText(student_gender_type.text())
                    school_dialog.btnUpdateSchool.clicked.connect(lambda: self.on_button_clicked(school_dialog, row))
                    school_dialog.btnCancelSchool.clicked.connect(lambda: self.close_dialog(school_dialog))

                    if school_dialog.exec_() == QDialog.Accepted:
                        pass

    def on_button_clicked(self, school_dialog, row):

        school_name = school_dialog.txtSchoolName.toPlainText()
        city = school_dialog.comboCity.currentText()
        directorate = school_dialog.combDirectorates.currentText()
        village = school_dialog.txtVillage.toPlainText()
        academic_level = school_dialog.comboAcademicLevel.currentText()
        student_gender_type = school_dialog.comboGenderType.currentText()

        self.table_widget.setItem(row, 1, QTableWidgetItem(school_name))
        self.table_widget.setItem(row, 2, QTableWidgetItem(city))
        self.table_widget.setItem(row, 3, QTableWidgetItem(directorate))
        self.table_widget.setItem(row, 4, QTableWidgetItem(village))
        self.table_widget.setItem(row, 5, QTableWidgetItem(academic_level))
        self.table_widget.setItem(row, 6, QTableWidgetItem(student_gender_type))

        school_id = school_dialog.labAddSchool.text()
        school = School.get(School.id == school_id)
        school.school_name = school_name
        school.city = city
        school.directorate = directorate
        school.village = village
        school.academic_level = academic_level
        school.student_gender_type = student_gender_type

        school.save()

        QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
        school_dialog.close()

    def close_dialog(self, school_dialog):
        school_dialog.close()


class DeleteUpdateButtonStudentsWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تفاصيل")
        self.delete_button.setFixedSize(110, 40)
        self.update_button.setStyleSheet(
            "QPushButton {  background-color:none;color:black;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.delete_button.setStyleSheet(
            "QPushButton { background-color: none; color:red;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.update_button.setFixedSize(110, 40)
        self.delete_button.setFixedSize(110, 40)
        self.delete_button.setIcon(QIcon("icons_rc/delete-svgrepo-com.svg"))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.setLayoutDirection(Qt.LeftToRight)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setIconSize(QSize(24, 24))
        self.update_button.setIcon(QIcon("icons_rc/assigned-person-edit.svg"))
        self.update_button.setLayoutDirection(Qt.LeftToRight)
        # layout
        layout.addSpacing(3)
        layout.addWidget(self.update_button)
        layout.addSpacing(3)
        layout.addWidget(self.delete_button)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.update_button.clicked.connect(self.on_update_button_clicked)

    def on_delete_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_student")
        if result_condition is True:
            print("on_delete_button_clicked")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    # Fetch the user with the selected ID from the database
                    student_id = self.table_widget.item(row, 0)
                    get_id = student_id.text()
                    try:
                        member = Members.get_by_id(get_id)
                        reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الطالب",
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            # Delete associated records in student table
                            Students.delete().where(Students.member_id == get_id).execute()

                            # Remove the member from Members table
                            self.table_widget.removeRow(row)
                            member.delete_instance()
                            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                    except Members.DoesNotExist:
                        print("Student does not exist.")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_update_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_student")
        if result_condition is True:

            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    number_id = self.table_widget.item(row, 0)
                    fname_stu = self.table_widget.item(row, 1)
                    lname_stu = self.table_widget.item(row, 2)
                    gender = self.table_widget.item(row, 3)
                    class_stu = self.table_widget.item(row, 4)
                    birth_stu = self.table_widget.item(row, 5)
                    par_phone = self.table_widget.item(row, 6)
                    fname_stu_item = fname_stu.text()

                    if number_id and fname_stu_item and lname_stu and gender and class_stu and birth_stu and par_phone:

                        words = fname_stu_item.split()

                        if words and words[-1] == lname_stu.text():
                            words = words[:-1]

                        modified_string = ' '.join(words) if words else ''

                        date = QDate.fromString(birth_stu.text(), "yyyy-MM-dd")
                        student_dialog = StudentDialog()
                        student_dialog.labAddStudent.setVisible(False)
                        student_dialog.labAddStudent.setText(number_id.text())
                        student_dialog.txtStudentFName.setPlainText(modified_string)
                        student_dialog.txtStudentLName.setPlainText(lname_stu.text())
                        student_dialog.combStudentGender.setCurrentText(gender.text())
                        student_dialog.combClasses.setCurrentText(class_stu.text())
                        student_dialog.dateStudentDOB.setDate(date)
                        student_dialog.txtStudentParentPhone.setPlainText(par_phone.text())
                        if student_dialog.exec_() == QDialog.Accepted:
                            FName, LName, gender, ClassId, Birth, Phone, ClassName = student_dialog.save_data()
                            # Fetch the student with the selected ID from the database
                            member_id = student_dialog.labAddStudent.text()
                            print("the member id is : ", number_id)
                            member = Members.get_by_id(member_id)
                            if member is not None:
                                member.fName = FName
                                member.lName = LName
                                member.phone = Phone
                                member.dateBerth = Birth
                                member.gender = gender
                                member.save()

                                student = Students.get(Students.member_id == member.id)
                                student.class_id = ClassId
                                student.save()

                                self.table_widget.setItem(row, 0, QTableWidgetItem(number_id.text()))
                                self.table_widget.setItem(row, 1, QTableWidgetItem(FName + ' ' + LName))
                                self.table_widget.setItem(row, 2, QTableWidgetItem(LName))
                                self.table_widget.setItem(row, 3, QTableWidgetItem(gender))
                                self.table_widget.setItem(row, 4, QTableWidgetItem(ClassName))
                                self.table_widget.setItem(row, 5, QTableWidgetItem(str(Birth)))
                                self.table_widget.setItem(row, 6, QTableWidgetItem(Phone))

                                QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")


class DeleteUpdateButtonTeacherScheduleWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.delete_teacher_schedule = QPushButton("حــــذف")
        self.update_teacher_schedule = QPushButton("تعــديل")
        self.delete_teacher_schedule.setFixedSize(110, 40)
        self.update_teacher_schedule.setStyleSheet(
            "color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
        self.delete_teacher_schedule.setStyleSheet("color: white; background-color: red;font:12pt 'PT Bold Heading';")
        self.update_teacher_schedule.setFixedSize(110, 40)
        layout.addSpacing(3)
        layout.addWidget(self.update_teacher_schedule)
        layout.addSpacing(3)
        layout.addWidget(self.delete_teacher_schedule)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.delete_teacher_schedule.clicked.connect(self.on_delete_button_teacher_schedule_clicked)
        self.update_teacher_schedule.clicked.connect(self.on_update_button_teacher_schedule_clicked)

    def on_delete_button_teacher_schedule_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                # Fetch the user with the selected ID from the database
                member_id = self.table_widget.item(row, 0)
                if member_id is not None:
                    member_id = int(member_id.text())  # Convert the item text to an integer
                    try:
                        teacher_schedule = Teachers_Schedule.get_by_id(member_id)

                        # Show confirmation message box
                        reply = QMessageBox.question(self, "تأكيد الحذف", "هل أنت متأكد أنك تريد حذف هذا الطالب",
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            print(teacher_schedule)
                            self.table_widget.removeRow(row)
                            teacher_schedule.delete_instance()
                            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                    except Teachers_Schedule.DoesNotExist:
                        print("Teacher schedule does not exist.")
                else:
                    print("Invalid member ID.")

    def on_update_button_teacher_schedule_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                member_id = self.table_widget.item(row, 0)
                day = self.table_widget.item(row, 1).text()
                subject = self.table_widget.item(row, 2).text()
                session = self.table_widget.item(row, 3).text()
                class_name = self.table_widget.item(row, 4).text()
                teacher_name = self.table_widget.item(row, 5).text()

                if member_id is not None:
                    member_id = int(member_id.text())  # Convert the item text to an integer
                    try:
                        teacher_schedule = Teachers_Schedule.get_by_id(member_id)
                        teacher_schedule.Teacher_Name = teacher_name
                        teacher_schedule.Day = day
                        teacher_schedule.Subject = subject
                        teacher_schedule.session = session
                        teacher_schedule.Class_Name = class_name
                        teacher_schedule.save()

                        QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
                    except Teachers_Schedule.DoesNotExist:
                        print("Teacher schedule does not exist.")
                else:
                    print("Invalid member ID.")


class DeleteUpdateButtonUsersWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تفاصيل")
        self.delete_button.setFixedSize(110, 40)
        self.update_button.setStyleSheet(
            "QPushButton {  background-color:none;color:rgb(255, 255, 255);font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.delete_button.setStyleSheet(
            "QPushButton { background-color: none; color:red;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.delete_button.setFixedSize(110, 40)
        self.delete_button.setIcon(QIcon("icons_rc/delete-svgrepo-com.svg"))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.setLayoutDirection(Qt.LeftToRight)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setFixedSize(110, 40)
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setIconSize(QSize(24, 24))
        self.update_button.setIcon(QIcon("icons_rc/assigned-person-edit.svg"))
        self.update_button.setLayoutDirection(Qt.LeftToRight)
        # layout
        layout.addSpacing(3)
        layout.addWidget(self.update_button)
        layout.addSpacing(3)
        layout.addWidget(self.delete_button)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.delete_button.clicked.connect(self.on_delete_button_user_clicked)
        self.update_button.clicked.connect(self.on_update_button_user_clicked)

    def on_delete_button_user_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_user")
        if result_condition is True:
            print("on_delete_button_clicked")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    # Fetch the user with the selected ID from the database
                    user_id = self.table_widget.item(row, 0)
                    get_id = user_id.text()
                    print("the id user is:")
                    try:
                        reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الطالب",
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            # Delete associated records in student table
                            Users.delete().where(Users.id == get_id).execute()

                            # Remove the member from Members table
                            self.table_widget.removeRow(row)

                            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                    except Members.DoesNotExist:
                        print("Student does not exist.")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_update_button_user_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_user")
        if result_condition is True:

            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()

                    # Fetch the user with the selected ID from the database
                    member_id = self.table_widget.item(row, 0)
                    # Get the data from the selected row in the table_widget
                    accountType = self.table_widget.item(row, 1)
                    Name = self.table_widget.item(row, 2)
                    userName = self.table_widget.item(row, 3)
                    userPassword = self.table_widget.item(row, 4)

                    if member_id and Name and userName and userPassword and accountType:

                        user_dialog = UserDialog()
                        user_dialog.labAddUsers.setVisible(False)
                        user_dialog.labAddUsers.setText(member_id.text())
                        user_dialog.comboAccountType.setCurrentText(accountType.text())
                        user_dialog.comboTeacherName.setCurrentText(Name.text())
                        user_dialog.txtUserName.setPlainText(userName.text())
                        user_dialog.txtPassword.setPlainText(userPassword.text())

                        if user_dialog.exec_() == QDialog.Accepted:
                            accountType = user_dialog.comboAccountType.currentText()
                            Name = user_dialog.comboTeacherName.currentText()
                            userName = user_dialog.txtUserName.toPlainText()
                            userPassword = user_dialog.txtPassword.toPlainText()

                            # Update the row in the table_widget with the new data
                            self.table_widget.setItem(row, 1, QTableWidgetItem(accountType))
                            self.table_widget.setItem(row, 2, QTableWidgetItem(Name))
                            self.table_widget.setItem(row, 3, QTableWidgetItem(userName))
                            self.table_widget.setItem(row, 4, QTableWidgetItem(userPassword))
                            Common.style_table_widget(self, self.table_widget)
                            member_id = user_dialog.labAddUsers.text()
                            user = Users.get_by_id(member_id)
                            user.account_type = accountType
                            user.Name = Name
                            user.userName = userName
                            user.userPassword = userPassword
                            user.save()

                            QMessageBox.information(self, "نجاح", "تم التعديل بنجاح")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")


class DeleteUpdateButtonCouncilFathersWidget(QWidget):
    def __init__(self, table_widget=None, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تفاصيل")
        self.delete_button.setFixedSize(110, 40)
        self.update_button.setStyleSheet(
            "QPushButton {  background-color:none;color:rgb(255, 255, 255);font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.delete_button.setStyleSheet(
            "QPushButton { background-color: none; color:red;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.update_button.setFixedSize(110, 40)
        self.delete_button.setFixedSize(110, 40)
        self.delete_button.setIcon(QIcon("icons_rc/delete-svgrepo-com.svg"))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.setLayoutDirection(Qt.LeftToRight)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setIconSize(QSize(24, 24))
        self.update_button.setIcon(QIcon("icons_rc/assigned-person-edit.svg"))
        self.update_button.setLayoutDirection(Qt.LeftToRight)
        # layout
        layout.addSpacing(3)
        layout.addWidget(self.update_button)
        layout.addSpacing(3)
        layout.addWidget(self.delete_button)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.update_button.clicked.connect(self.on_update_button_clicked)

    def on_delete_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_fathers")
        if result_condition is True:
            print("on_delete")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    # Fetch the user with the selected ID from the database
                    father_id = self.table_widget.item(row, 0)
                    get_id = father_id.text()
                    try:
                        member = Members.get_by_id(get_id)
                        reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا العضو",
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            # Delete associated records in CouncilFathers table
                            CouncilFathers.delete().where(CouncilFathers.members_id == get_id).execute()

                            # Remove the member from Members table
                            self.table_widget.removeRow(row)
                            member.delete_instance()
                            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                    except Members.DoesNotExist:
                        print("Student does not exist.")

        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_update_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_fathers")
        if result_condition is True:
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    # Fetch the user with the selected ID from the database
                    member_id = self.table_widget.item(row, 0)
                    council_fathers_fname = self.table_widget.item(row, 1)
                    council_fathers_lname = self.table_widget.item(row, 2)
                    council_fathers_gender = self.table_widget.item(row, 3)
                    council_fathers_phone = self.table_widget.item(row, 4)
                    council_father_born = self.table_widget.item(row, 5)
                    council_fathers_social_status = self.table_widget.item(row, 6)
                    council_fathers_address = self.table_widget.item(row, 7)
                    council_fathers_organic_status = self.table_widget.item(row, 8)
                    fname_father_item = council_fathers_fname.text()

                    if member_id and council_fathers_fname and council_fathers_lname and council_fathers_gender and council_fathers_phone and council_father_born \
                            and council_fathers_social_status and council_fathers_address and council_fathers_organic_status and fname_father_item:
                        words = fname_father_item.split()

                        if words and words[-1] == council_fathers_lname.text():
                            words = words[:-1]
                        modified_string = ' '.join(words) if words else ''
                        print(modified_string)
                        date = QDate.fromString(council_father_born.text(), "yyyy-MM-dd")
                        council_fathers_dialog = CouncilFathersDialog()
                        council_fathers_dialog.labAddFathers.setVisible(False)
                        council_fathers_dialog.labAddFathers.setText(member_id.text())
                        council_fathers_dialog.txtCouncilFatherfName.setPlainText(modified_string)
                        council_fathers_dialog.txtCouncilLName.setPlainText(council_fathers_lname.text())
                        council_fathers_dialog.combFatherGender.setCurrentText(council_fathers_gender.text())
                        council_fathers_dialog.txtCouncilPhone.setPlainText(council_fathers_phone.text())
                        council_fathers_dialog.dateCouncilDOB.setDate(date)
                        council_fathers_dialog.txtCouncilSocialStatus.setPlainText(council_fathers_social_status.text())
                        council_fathers_dialog.txtCouncilAddrress.setPlainText(council_fathers_address.text())
                        council_fathers_dialog.txtCouncilOrganicStatus.setPlainText(
                            council_fathers_organic_status.text())
                        if council_fathers_dialog.exec_() == QDialog.Accepted:
                            print("hello2")
                            CouncilFatherfName, CouncilLName, CouncilGender, CouncilPhone, CouncilDOB, CouncilSocialStatus, CouncilAddrress, CouncilOrganicStatus = council_fathers_dialog.save_data()
                            lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                            member_id = council_fathers_dialog.labAddFathers.text()
                            print("the member id is : ", member_id)
                            member = Members.get_by_id(member_id)
                            if member is not None:
                                member.school_id = lastInsertedSchoolId
                                member.fName = CouncilFatherfName
                                member.lName = CouncilLName
                                member.phone = CouncilPhone
                                member.dateBerth = CouncilDOB
                                member.gender = CouncilGender
                                member.save()

                                # Update the Students table
                                fathers = CouncilFathers.get(CouncilFathers.members_id == member.id)
                                fathers.social_status = CouncilSocialStatus
                                fathers.address = CouncilAddrress
                                fathers.organic_status = CouncilOrganicStatus
                                fathers.save()
                                print("hello3")
                                # Update the row in the table_widget with the new data
                                self.table_widget.setItem(row, 1,
                                                          QTableWidgetItem(CouncilFatherfName + ' ' + CouncilLName))
                                self.table_widget.setItem(row, 2, QTableWidgetItem(CouncilLName))
                                self.table_widget.setItem(row, 3, QTableWidgetItem(CouncilGender))
                                self.table_widget.setItem(row, 4, QTableWidgetItem(CouncilPhone))
                                self.table_widget.setItem(row, 5, QTableWidgetItem(str(CouncilDOB)))
                                self.table_widget.setItem(row, 6, QTableWidgetItem(CouncilSocialStatus))
                                self.table_widget.setItem(row, 7, QTableWidgetItem(CouncilAddrress))
                                self.table_widget.setItem(row, 8, QTableWidgetItem(CouncilOrganicStatus))
                                QMessageBox.information(self, "تعديل", "تم التعديل  بنجاح.")

        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")


#
# class DeleteUpdateButtonDeviceWidget(QWidget):
#     def __init__(self, table_widget, parent=None):
#         super().__init__(parent)
#         # self.submain = submain_instance
#         # self.ui = self.submain.ui
#         self.table_widget = table_widget
#         # self.zk = ZK()
#         layout = QVBoxLayout()
#
#         self.delete_button = QPushButton("حــــذف")
#         self.update_button = QPushButton("تعــديل")
#         self.connect_button = QPushButton("إتصــــال")
#         self.connect_button.setStyleSheet("color: white; background-color: green;font: 12pt 'PT Bold Heading';")
#         self.delete_button.setFixedSize(110, 40)
#         self.connect_button.setFixedSize(110, 40)
#         self.update_button.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
#         self.delete_button.setStyleSheet("color: white; background-color: red;font:12pt 'PT Bold Heading';")
#         self.update_button.setFixedSize(110, 40)
#
#         layout.addSpacing(3)
#         layout.addWidget(self.connect_button)
#         layout.addWidget(self.update_button)
#         layout.addSpacing(3)
#         layout.addWidget(self.delete_button)
#
#         layout.setContentsMargins(0, 0, 0, 0)
#         layout.setAlignment(Qt.AlignCenter)
#         self.setLayout(layout)
#
#         self.delete_button.clicked.connect(self.on_delete_button_clicked)
#         self.update_button.clicked.connect(self.on_update_button_clicked)
#
#     def on_delete_button_clicked(self):
#         clicked_button = self.sender()
#         if clicked_button:
#             cell_widget = clicked_button.parentWidget()
#             if cell_widget and self.table_widget:
#                 row = self.table_widget.indexAt(cell_widget.pos()).row()
#                 self.table_widget.removeRow(row)
#
#     def on_update_button_clicked(self):
#         clicked_button = self.sender()
#         if clicked_button:
#             cell_widget = clicked_button.parentWidget()
#             if cell_widget and self.table_widget:
#                 row = self.table_widget.indexAt(cell_widget.pos()).row()
#                 # Get the data from the selected row in the table_widget
#                 ip_address_item = self.table_widget.item(row, 1)
#                 port_number_item = self.table_widget.item(row, 2)
#
#                 if ip_address_item and port_number_item:
#                     ip_address = ip_address_item.text()
#                     port_number = port_number_item.text()
#                     device_dialog = MyDialog()
#                     device_dialog.txtIPAddress.setPlainText(ip_address)
#                     device_dialog.txtPortNumber.setPlainText(port_number)
#
#                     if device_dialog.exec_() == QDialog.Accepted:
#                         ip_address = device_dialog.txtIPAddress.toPlainText()
#                         port_number = device_dialog.txtPortNumber.toPlainText()
#
#                         # Update the row in the table_widget with the new data
#                         self.table_widget.setItem(row, 1, QTableWidgetItem(ip_address))
#                         self.table_widget.setItem(row, 2, QTableWidgetItem(port_number))
class DeleteUpdateButtonDeviceWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        # self.submain = submain_instance
        # self.ui = self.submain.ui
        self.table_widget = table_widget
        # self.zk = ZK()
        layout = QVBoxLayout()

        self.save_button = QPushButton("حفظ")
        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تعــديل")
        self.update_button.setStyleSheet(
            "QPushButton {  background-color:none;color:rgb(255, 255, 255);font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.delete_button.setStyleSheet(
            "QPushButton { background-color: none; color:red;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.update_button.setFixedSize(110, 40)
        self.delete_button.setFixedSize(110, 40)
        self.delete_button.setIcon(QIcon("icons_rc/delete-svgrepo-com.svg"))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.setLayoutDirection(Qt.LeftToRight)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setIconSize(QSize(24, 24))
        self.update_button.setIcon(QIcon("icons_rc/assigned-person-edit.svg"))
        self.update_button.setLayoutDirection(Qt.LeftToRight)
        self.save_button.setFixedSize(110, 40)
        self.save_button.setStyleSheet("color: white; background-color: green;font: 12pt 'PT Bold Heading';")

        layout.addSpacing(3)
        layout.addWidget(self.save_button)
        layout.addWidget(self.update_button)
        layout.addSpacing(3)
        layout.addWidget(self.delete_button)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.save_button.clicked.connect(self.on_save_button_clicked)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.update_button.clicked.connect(self.on_update_button_clicked)

    def on_delete_button_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                self.table_widget.removeRow(row)

    def on_update_button_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                # Get the data from the selected row in the table_widget
                ip_address_item = self.table_widget.item(row, 1)
                port_number_item = self.table_widget.item(row, 2)

                if ip_address_item and port_number_item:
                    ip_address = ip_address_item.text()
                    port_number = port_number_item.text()
                    device_dialog = MyDialog()
                    device_dialog.txtIPAddress.setPlainText(ip_address)
                    device_dialog.txtPortNumber.setPlainText(port_number)

                    if device_dialog.exec_() == QDialog.Accepted:
                        ip_address = device_dialog.txtIPAddress.toPlainText()
                        port_number = device_dialog.txtPortNumber.toPlainText()

                        self.table_widget.setItem(row, 1, QTableWidgetItem(ip_address))
                        self.table_widget.setItem(row, 2, QTableWidgetItem(port_number))

    def on_save_button_clicked(self):
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                name_device = self.table_widget.item(row, 0).text()
                ip_address_item = self.table_widget.item(row, 1)
                port_number_item = self.table_widget.item(row, 2)
                status = "غير متصل"
                lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                Device.insert({
                    Device.school_id: lastInsertedSchoolId,
                    Device.name: name_device,
                    Device.ip: ip_address_item.text(),
                    Device.port: port_number_item.text(),
                    Device.status: status,
                }).execute()
                QMessageBox.information(self, "نجاح", "تم الحفظ بنجاح")


class chickedButton(QWidget):
    def __init__(self, table_widget=None, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        self.layout = QVBoxLayout()
        self.trueButton = QToolButton(self)
        self.trueButton.setIcon(QIcon("icons_rc/checked.png"))
        self.trueButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.trueButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.trueButton.setStyleSheet("background-color: none;")
        icon_size = QSize(25, 25)
        self.trueButton.setIconSize(icon_size)
        self.trueButton.setFixedSize(160, 147)
        self.layout.addWidget(self.trueButton)
        self.layout.setAlignment(Qt.AlignCenter)


class unchickedButton(QWidget):
    def __init__(self, table_widget=None, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        self.layout = QVBoxLayout()
        self.falseButton = QToolButton(self)
        self.falseButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.falseButton.setIcon(QIcon("icons_rc/multiply.png"))
        self.falseButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.falseButton.setStyleSheet("background-color: none;")
        icon_size = QSize(25, 25)  # Set the desired size of the icon
        self.falseButton.setIconSize(icon_size)
        self.falseButton.setFixedSize(160, 147)

        self.layout.addWidget(self.falseButton)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setAlignment(Qt.AlignVCenter)


class DeleteUpdateButtonTeachersWidget(QWidget):
    def __init__(self, table_widget=None, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        self.layout = QVBoxLayout()
        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تفاصيل")
        self.delete_button.setFixedSize(110, 40)
        self.update_button.setStyleSheet(
            "QPushButton {  background-color:none;color:black;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.delete_button.setStyleSheet(
            "QPushButton { background-color: none; color:red;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.update_button.setFixedSize(110, 40)
        self.delete_button.setFixedSize(110, 40)
        self.delete_button.setIcon(QIcon("icons_rc/delete-svgrepo-com.svg"))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.setLayoutDirection(Qt.LeftToRight)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setIconSize(QSize(24, 24))
        self.update_button.setIcon(QIcon("icons_rc/assigned-person-edit.svg"))
        self.update_button.setLayoutDirection(Qt.LeftToRight)
        # layout
        self.layout.addSpacing(3)
        self.layout.addWidget(self.update_button)
        self.layout.addSpacing(3)
        self.layout.addWidget(self.delete_button)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.update_button.clicked.connect(self.print_attendance)

    def on_delete_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_teacher")
        if result_condition is True:
            print("on_delete_button_clicked")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    teacher_id = self.table_widget.item(row, 0)
                    get_id = teacher_id.text()
                    try:
                        member = Members.get_by_id(get_id)
                        reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا المعلم",
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            self.table_widget.removeRow(row)
                            member.delete_instance()
                            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                    except Members.DoesNotExist:
                        print("Student does not exist.")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    # def open_add_fingers_dialog(self):
    # rejester_fingers = RejesterTeacherFingerDialog()
    # rejester_fingers.exec_()
    # clicked_button = self.sender()
    # try:
    #     state, ip, port = Common.connect_device(self)
    #     if clicked_button:
    #         if state is not None:
    #             if ip is not None and port is not None:
    #                 cell_widget = clicked_button.parentWidget()
    #                 if cell_widget and self.table_widget:
    #                     row = self.table_widget.indexAt(cell_widget.pos()).row()
    #                     user_id = self.table_widget.item(row, 0)
    #                     user_name = self.table_widget.item(row, 1)
    #                     zk = ZK(ip=ip.text(), port=int(port.text()), timeout=5)
    #                     try:
    #                         conn = zk.connect()
    #                         conn.set_user(uid=int(user_id), user_id=str(user_id),
    #                                       name=user_name)
    #                     except ZKErrorResponse as e:
    #                         QMessageBox.warning(self, "تحذير", str(e) + "تم قطع الاتصال")
    #         else:
    #             QMessageBox.warning(self, 'خطأ', 'يجب الاتصال بالجهاز اولاً')
    # except Exception as e:
    #     QMessageBox.warning(self, "تحذير", str(e) + "هناك خطأ")

    # def set_users_into_device(self):
    #     state, ip, port = Common.connect_device(self.ui)
    #     if state is not None:
    #         if ip is not None and port is not None:
    #             pass

    # def connect_table_widget(self):

    def get_buttons(self, operation):
        if operation == 'New':
            self.setLayout(self.layout1)
        elif operation == 'Old':
            self.setLayout(self.layout)

        return self

    def on_update_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_teacher")
        if result_condition is True:
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    member_id = self.table_widget.item(row, 0)
                    fname = self.table_widget.item(row, 1)
                    lname = self.table_widget.item(row, 2)
                    gender = self.table_widget.item(row, 3)
                    cities = self.table_widget.item(row, 4)
                    teacher_DOB = self.table_widget.item(row, 5)
                    teacher_phone = self.table_widget.item(row, 6)
                    qualification = self.table_widget.item(row, 7)
                    date_qualification = self.table_widget.item(row, 8)
                    Shift_type = self.table_widget.item(row, 9)
                    teacher_major = self.table_widget.item(row, 10)
                    task = self.table_widget.item(row, 11)
                    exceperiance_years = self.table_widget.item(row, 12)
                    teacher_state = self.table_widget.item(row, 13)
                    fname_teacher_item = fname.text()

                    if fname_teacher_item and lname and gender and cities and teacher_DOB and teacher_phone \
                            and qualification and date_qualification and Shift_type and \
                            teacher_major and task and exceperiance_years and teacher_state:
                        words = fname_teacher_item.split()

                        if words and words[-1] == lname.text():
                            words = words[:-1]

                        modified_string = ' '.join(words) if words else ''
                        date = QDate.fromString(teacher_DOB.text(), "yyyy-MM-dd")
                        qualification_date = QDate.fromString(date_qualification.text(), "yyyy-MM-dd")
                        teacher_dialog = TeacherDialog()
                        teacher_dialog.labAddTeacher.setText(member_id.text())
                        teacher_dialog.txtTeacherFName.setPlainText(modified_string)
                        teacher_dialog.txtTeacherLName.setPlainText(lname.text())
                        teacher_dialog.combTeatcherGendar.setCurrentText(gender.text())
                        teacher_dialog.combTeatcherCitye.setCurrentText(cities.text())
                        teacher_dialog.dateTeacherDOB.setDate(date)
                        teacher_dialog.txtTeacherPhone.setPlainText(teacher_phone.text())
                        teacher_dialog.combShiftsType.setCurrentText(Shift_type.text())
                        teacher_dialog.txtTeacherQualification.setPlainText(qualification.text())
                        teacher_dialog.dateTeacherDOQualification.setDate(qualification_date)
                        teacher_dialog.txtTeacherMajor.setPlainText(teacher_major.text())
                        teacher_dialog.ComboTeacherTask.setCurrentText(task.text())
                        teacher_dialog.txtExceperianceYears.setText(exceperiance_years.text())
                        teacher_dialog.ComboTeacherStatus.setCurrentText(teacher_state.text())
                        m = Members.get_members_by_id(self, member_id.text())
                        teacher = Teachers.get_by_id(member_id.text())
                        lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                        teacher_dialog.labAddTeacher.setText(str(teacher.id) + 'رقم البصمة : ')
                        if teacher_dialog.exec_() == QDialog.Accepted:
                            FName, LName, Gender, Cities, DOB, Phone, Qualification, DOQualification, ShiftsType, Major, Task, ExceperianceYears, state = teacher_dialog.save_data()
                            m.school_id = lastInsertedSchoolId
                            m.fName = FName
                            m.lName = LName
                            m.dateBerth = DOB
                            m.phone = Phone
                            m.save()

                            teacher.gender = Gender
                            teacher.cities = Cities
                            teacher.Shift_type = ShiftsType
                            teacher.major = Major
                            teacher.task = Task
                            teacher.exceperiance_years = ExceperianceYears
                            teacher.qualification = Qualification
                            teacher.date_qualification = DOQualification
                            teacher.state = state
                            teacher.save()

                            self.table_widget.setItem(row, 0, QTableWidgetItem(str(teacher.members_id)))
                            self.table_widget.setItem(row, 1, QTableWidgetItem(FName + " " + LName))
                            self.table_widget.setItem(row, 2, QTableWidgetItem(LName))
                            self.table_widget.setItem(row, 3, QTableWidgetItem(Gender))
                            self.table_widget.setItem(row, 4, QTableWidgetItem(Cities))
                            self.table_widget.setItem(row, 5, QTableWidgetItem(str(DOB)))
                            self.table_widget.setItem(row, 6, QTableWidgetItem(str(Phone)))
                            self.table_widget.setItem(row, 7, QTableWidgetItem(Qualification))
                            self.table_widget.setItem(row, 8, QTableWidgetItem(str(DOQualification)))
                            self.table_widget.setItem(row, 9, QTableWidgetItem(ShiftsType))
                            self.table_widget.setItem(row, 10, QTableWidgetItem(Major))
                            self.table_widget.setItem(row, 11, QTableWidgetItem(Task))
                            self.table_widget.setItem(row, 12, QTableWidgetItem(str(ExceperianceYears)))
                            self.table_widget.setItem(row, 13, QTableWidgetItem(state))
                            QMessageBox.information(self, "تعديل", "تم التعديل  بنجاح.")
                            Common.style_table_widget(self, self.table_widget)
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def print_attendance(self):
        self.last_inserted_device = Device.select(peewee.fn.Max(Device.id)).scalar()
        device = Device.get(Device.id == self.last_inserted_device)
        zk = ZK(device.ip, port=device.port, timeout=5)
        users = [1, 30]
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 12, 31)
        try:
            limited_attendances = zk.get_limited_attendance(users=users, start_date=start_date,
                                                            end_date=end_date)
            for attendance in limited_attendances:
                print(attendance)
        except ZKErrorResponse as error:
            print(error)

    def add_users_to_device(self, teacher_id, teacher_name, ip, port):
        # self.last_inserted_device = Device.select(peewee.fn.Max(Device.id)).scalar()
        # device = Device.get(Device.id == self.last_inserted_device)
        zk = ZK(ip, port=port, timeout=5)
        try:
            conn = zk.connect()
            conn.set_user(uid=int(teacher_id), user_id=str(teacher_id), name=teacher_name)
        except ZKErrorResponse as e:
            QMessageBox.warning(self, "خطأ", str("هناك خطأ ما، الرجاء المحاولة لاحقا"))

    def start_enroll_face(sIp="192.168.1.201", iPort=4370, iMachineNumber=1, userid="", fingureindex=0):
        zk = ZK('192.168.1.201', port=4370, timeout=5)
        conn = None
        try:
            conn = zk.connect()
            if conn:
                conn.disable_device()
                user_id = str(userid)
                finger_index = int(fingureindex)

                # Clear the existing face template for the user
                conn.delete_user_face(iMachineNumber, user_id, finger_index)

                # Start the face enrollment process
                if conn.start_enroll_ex(user_id, finger_index, 1):  # 1 represents the face biometric type
                    logging.info(f"Start to enroll a new user, UserID={user_id}, Face ID={finger_index}, Flag=1")
                    conn.start_identify()  # Let the device enter 1:N verification condition after enrolling templates
                    conn.refresh_data(1)  # Refresh the data in the device
                    start_enroll_result = True
                else:
                    logging.error("Failed to start enrollment.")
                    start_enroll_result = False

                conn.enable_device()
                return start_enroll_result
            else:
                logging.error("Failed to establish connection to the device.")
                return False
        except Exception as e:
            logging.error("An error occurred during face enrollment.", exc_info=True)
            return False
        finally:
            if conn:
                conn.disconnect()


class DeleteUpdateButtonShiftsWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تفاصيل")
        self.delete_button.setFixedSize(110, 40)
        self.update_button.setStyleSheet(
            "QPushButton {  background-color:none;color:rgb(255, 255, 255);font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.delete_button.setStyleSheet(
            "QPushButton { background-color: none; color:red;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.update_button.setFixedSize(110, 40)
        self.delete_button.setFixedSize(110, 40)
        self.delete_button.setIcon(QIcon("icons_rc/delete-svgrepo-com.svg"))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.setLayoutDirection(Qt.LeftToRight)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setIconSize(QSize(24, 24))
        self.update_button.setIcon(QIcon("icons_rc/assigned-person-edit.svg"))
        self.update_button.setLayoutDirection(Qt.LeftToRight)
        # layout
        layout.addSpacing(3)
        layout.addWidget(self.update_button)
        layout.addSpacing(3)
        layout.addWidget(self.delete_button)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.update_button.clicked.connect(self.on_update_button_clicked)

    def on_delete_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_attendance")
        if result_condition is True:
            print("on_delete_button_clicked")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    # Fetch the user with the selected ID from the database
                    shift_time_id = self.table_widget.item(row, 0)
                    get_id = shift_time_id.text()
                    try:
                        shift = Shifts.get_by_id(get_id)
                        reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الوردية",
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            self.table_widget.removeRow(row)
                            shift.delete_instance()
                            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                    except Shifts.DoesNotExist:
                        print("shift_time does not exist.")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_update_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_attendance")
        if result_condition is True:
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    Shift_time_id = self.table_widget.item(row, 0)
                    name = self.table_widget.item(row, 1)
                    AttendanceTime = self.table_widget.item(row, 2)
                    LeavingTime = self.table_widget.item(row, 3)
                    AllowedTimeForAttendance = self.table_widget.item(row, 4)
                    AllowedTimeForLeaving = self.table_widget.item(row, 5)
                    StartOfRegistering = self.table_widget.item(row, 6)
                    EndOfRegistering = self.table_widget.item(row, 7)
                    StartOut = self.table_widget.item(row, 8)
                    EndOut = self.table_widget.item(row, 9)

                    if Shift_time_id and name and AttendanceTime and LeavingTime and AllowedTimeForAttendance \
                            and AllowedTimeForLeaving and StartOfRegistering and EndOfRegistering and StartOut and EndOut:

                        attendance_time = QTime.fromString(AttendanceTime.text(), "hh:mm")
                        leaving_time = QTime.fromString(LeavingTime.text(), "hh:mm")
                        start_of_registering = QTime.fromString(StartOfRegistering.text(), "hh:mm")
                        end_of_registering = QTime.fromString(EndOfRegistering.text(), "hh:mm")
                        start_out = QTime.fromString(StartOut.text(), "hh:mm")
                        end_out = QTime.fromString(EndOut.text(), "hh:mm")

                        Shift_time_dialog = Shift_timedialog()
                        Shift_time_dialog.labAddShift.setText(Shift_time_id.text())
                        Shift_time_dialog.labAddShift.setVisible(False)
                        Shift_time_dialog.txtshift_name.setPlainText(name.text())
                        Shift_time_dialog.timeAttendanceTime.setTime(attendance_time)
                        Shift_time_dialog.timeLeavingTime.setTime(leaving_time)
                        Shift_time_dialog.timeAllowedTimeForAttendance.setPlainText(AllowedTimeForAttendance.text())
                        Shift_time_dialog.timeAllowedTimeForLeaving.setPlainText(AllowedTimeForLeaving.text())
                        Shift_time_dialog.timeStartOfRegistering.setTime(start_of_registering)
                        Shift_time_dialog.timeEndOfRegistering.setTime(end_of_registering)
                        Shift_time_dialog.timeStartOut.setTime(start_out)
                        Shift_time_dialog.timeEndOut.setTime(end_out)

                        if Shift_time_dialog.exec_() == QDialog.Accepted:
                            name = Shift_time_dialog.txtshift_name.toPlainText()
                            AttendanceTime = Shift_time_dialog.timeAttendanceTime.time().toPyTime()
                            LeavingTime = Shift_time_dialog.timeLeavingTime.time().toPyTime()
                            AllowedTimeForAttendance = Shift_time_dialog.timeAllowedTimeForAttendance.toPlainText()
                            AllowedTimeForLeaving = Shift_time_dialog.timeAllowedTimeForLeaving.toPlainText()
                            StartOfRegistering = Shift_time_dialog.timeStartOfRegistering.time().toPyTime()
                            EndOfRegistering = Shift_time_dialog.timeEndOfRegistering.time().toPyTime()
                            StartOut = Shift_time_dialog.timeStartOut.time().toPyTime()
                            EndOut = Shift_time_dialog.timeEndOut.time().toPyTime()

                            entry_start_time_str = AttendanceTime.strftime('%H:%M')
                            entry_end_time_str = LeavingTime.strftime('%H:%M')
                            start_of_registering_time_str = StartOfRegistering.strftime('%H:%M')
                            end_of_registering_time_str = EndOfRegistering.strftime('%H:%M')
                            start_out_time_str = StartOut.strftime('%H:%M')
                            end_out_time_str = EndOut.strftime('%H:%M')

                            self.table_widget.setItem(row, 1, QTableWidgetItem(name))
                            self.table_widget.setItem(row, 2, QTableWidgetItem(str(entry_start_time_str)))
                            self.table_widget.setItem(row, 3, QTableWidgetItem(str(entry_end_time_str)))
                            self.table_widget.setItem(row, 4, QTableWidgetItem(str(AllowedTimeForAttendance)))
                            self.table_widget.setItem(row, 5, QTableWidgetItem(str(AllowedTimeForLeaving)))
                            self.table_widget.setItem(row, 6, QTableWidgetItem(str(start_of_registering_time_str)))
                            self.table_widget.setItem(row, 7, QTableWidgetItem(str(end_of_registering_time_str)))
                            self.table_widget.setItem(row, 8, QTableWidgetItem(str(start_out_time_str)))
                            self.table_widget.setItem(row, 9, QTableWidgetItem(str(end_out_time_str)))
                            Common.style_table_widget(self, self.table_widget)

                            shift_id = Shift_time_dialog.labAddShift.text()
                            shifts = Shifts.get_by_id(shift_id)
                            shifts.name = name
                            shifts.attending_time = entry_start_time_str
                            shifts.leaving_time = entry_end_time_str
                            shifts.time_allowed_for_late = AllowedTimeForAttendance
                            shifts.time_allowed_for_leaving = AllowedTimeForLeaving
                            shifts.start_attendance = start_of_registering_time_str
                            shifts.end_attendance = end_of_registering_time_str
                            shifts.start_leaving = start_out_time_str
                            shifts.end_leaving = end_out_time_str
                            shifts.updated_at = QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss")
                            shifts.save()
                            QMessageBox.information(self, "تعديل", "تم التعديل  بنجاح.")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")


class DeleteUpdateButtonShiftsWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.add_period = QPushButton("أضافة فترة")
        self.delete_shift = QPushButton("حــــذف")
        self.update_shift = QPushButton("تعــديل")
        self.add_period.setFixedSize(110, 40)
        self.delete_shift.setFixedSize(110, 40)
        self.update_shift.setFixedSize(110, 40)
        self.add_period.setStyleSheet("color: white; background-color: brown; font: 12pt 'PT Bold Heading';")
        self.update_shift.setStyleSheet("color: white; background-color: blue; font: 12pt 'PT Bold Heading';")
        self.delete_shift.setStyleSheet("color: white; background-color: red;font:12pt 'PT Bold Heading';")
        layout.addWidget(self.add_period)
        layout.addWidget(self.update_shift)
        layout.addWidget(self.delete_shift)
        layout.addSpacing(3)
        layout.addSpacing(3)
        layout.addSpacing(3)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        self.add_period.clicked.connect(self.on_add_period_button_clicked)
        self.delete_shift.clicked.connect(self.on_delete_button_clicked)
        self.update_shift.clicked.connect(self.on_update_button_clicked)

    def on_delete_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_attendance")
        if result_condition is True:
            print("on_delete_button_clicked")
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    # Fetch the user with the selected ID from the database
                    shift_time_id = self.table_widget.item(row, 0)
                    get_id = shift_time_id.text()
                    try:
                        shift = Shifts.get_by_id(get_id)
                        reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الوردية",
                                                     QMessageBox.Yes | QMessageBox.No)
                        if reply == QMessageBox.Yes:
                            self.table_widget.removeRow(row)
                            shift.delete_instance()
                            QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                    except Shifts.DoesNotExist:
                        QMessageBox.Warning(self, "خطأ", "حدث خطأ في الورديات")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_update_button_clicked(self):
        result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_attendance")
        if result_condition is True:
            clicked_button = self.sender()
            if clicked_button:
                cell_widget = clicked_button.parentWidget()
                if cell_widget and self.table_widget:
                    row = self.table_widget.indexAt(cell_widget.pos()).row()
                    Shift_time_id = self.table_widget.item(row, 0)
                    name = self.table_widget.item(row, 1)
                    start_date_shift = self.table_widget.item(row, 2)
                    end_date_shift = self.table_widget.item(row, 3)

                    if Shift_time_id and name and start_date_shift and end_date_shift:

                        date_start = QDate.fromString(start_date_shift.text(), "yyyy-MM-dd")
                        date_end = QDate.fromString(end_date_shift.text(), "yyyy-MM-dd")
                        Shift_time_dialog = Shift_timedialog()
                        Shift_time_dialog.labAddShift.setText(Shift_time_id.text())
                        Shift_time_dialog.txtshift_name.setPlainText(name.text())
                        Shift_time_dialog.dateStartShift.setDate(date_start)
                        Shift_time_dialog.dateEndShift.setDate(date_end)

                        if Shift_time_dialog.exec_() == QDialog.Accepted:
                            name, start_shift, end_shift = Shift_time_dialog.save_data_shift()
                            shift_id = Shift_time_dialog.labAddShift.text()
                            print("the member id is : ", shift_id)
                            shifts = Shifts.get_by_id(shift_id)
                            shifts.name = name
                            shifts.start_date_shift = start_shift
                            shifts.end_date_shift = end_shift
                            shifts.save()

                            self.table_widget.setItem(row, 0, QTableWidgetItem(shift_id))
                            self.table_widget.setItem(row, 1, QTableWidgetItem(name))
                            self.table_widget.setItem(row, 2, QTableWidgetItem(str(start_shift)))
                            self.table_widget.setItem(row, 3, QTableWidgetItem(str(end_shift)))

                            Common.style_table_widget(self, self.table_widget)

                            QMessageBox.information(self, "تعديل", "تم التعديل  بنجاح.")
        else:
            QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_add_period_button_clicked(self):
        for num in range(8, 15):
            self.table_widget.setColumnHidden(num, False)
            # self.table_widget.setColumnHidden(0, False)

        for num in range(1, 7):
            self.table_widget.setColumnHidden(num, True)

        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                get_shift_id = self.table_widget.item(row, 0)
                shift_id = get_shift_id.text()
                self.table_widget.setRowCount(0)

                period_dialog = PeriodDialog()

                if period_dialog.exec_() == QDialog.Accepted:
                    NamePeriod, entry_start_time_str, entry_end_time_str, PricePeriod, AllowedTimeForAttendance, AllowedTimeForLeavingt = period_dialog.save_data_period()
                    # print("elements period are:", NamePeriod,entry_start_time_str,entry_end_time_str,PricePeriod)
                    # try:
                    # operationsButtons = DeleteUpdateButtonShiftsWidget(table_widget=period_dialog.tablPeriods)
                    Periods.insert({
                        Periods.shift_id: shift_id,
                        Periods.name: NamePeriod,
                        Periods.attendance_time: entry_start_time_str,
                        Periods.departure_time: entry_end_time_str,
                        Periods.period_price: PricePeriod,
                        Periods.time_allowed_for_late: AllowedTimeForAttendance,
                        Periods.time_allowed_for_leaving: AllowedTimeForLeavingt,

                    }).execute()
                    lastInsertedPeriodId = Periods.select(peewee.fn.Max(Periods.id)).scalar()

                    operations_buttons = DeleteUpdateButtonPeriodsWidget(table_widget=self.table_widget)
                    current_row = self.table_widget.rowCount()  # Get the current row index
                    self.table_widget.insertRow(
                        current_row)  # Insert a new row at the current row index
                    self.table_widget.setItem(current_row, 0,
                                              QTableWidgetItem(str(shift_id)))
                    self.table_widget.setItem(current_row, 7,
                                              QTableWidgetItem(str(lastInsertedPeriodId)))
                    self.table_widget.setItem(current_row, 8,
                                              QTableWidgetItem(NamePeriod))
                    self.table_widget.setItem(current_row, 9,
                                              QTableWidgetItem(entry_start_time_str))
                    self.table_widget.setItem(current_row, 10, QTableWidgetItem(entry_end_time_str))
                    self.table_widget.setItem(current_row, 11, QTableWidgetItem(str(PricePeriod)))
                    self.table_widget.setItem(current_row, 12,
                                              QTableWidgetItem(str(AllowedTimeForAttendance)))
                    self.table_widget.setItem(current_row, 13,
                                              QTableWidgetItem(str(AllowedTimeForLeavingt)))
                    self.table_widget.setCellWidget(current_row, 14, operations_buttons)
                    self.table_widget.setColumnWidth(current_row, 40)
                    self.table_widget.setRowHeight(current_row, 150)

                    QMessageBox.information(self, "أضافة", "تم اضافة الفترة  بنجاح.")


class DeleteUpdateButtonPeriodsWidget(QWidget):
    def __init__(self, table_widget, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.delete_button = QPushButton("حــــذف")
        self.update_button = QPushButton("تفاصيل")
        self.delete_button.setFixedSize(110, 40)
        self.update_button.setStyleSheet(
            "QPushButton {  background-color:none;color:rgb(255, 255, 255);font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.delete_button.setStyleSheet(
            "QPushButton { background-color: none; color:red;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        self.update_button.setFixedSize(110, 40)
        self.delete_button.setFixedSize(110, 40)
        self.delete_button.setIcon(QIcon("icons_rc/delete-svgrepo-com.svg"))
        self.delete_button.setIconSize(QSize(24, 24))
        self.delete_button.setLayoutDirection(Qt.LeftToRight)
        self.delete_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.update_button.setIconSize(QSize(24, 24))
        self.update_button.setIcon(QIcon("icons_rc/assigned-person-edit.svg"))
        self.update_button.setLayoutDirection(Qt.LeftToRight)
        # layout
        layout.addSpacing(3)
        layout.addWidget(self.update_button)
        layout.addSpacing(3)
        layout.addWidget(self.delete_button)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.update_button.clicked.connect(self.on_update_button_clicked)
        self.setLayout(layout)

    def on_delete_button_clicked(self):
        # result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_delete_attendance")
        # if result_condition is True:
        print("on_delete_button_clicked")
        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                # Fetch the user with the selected ID from the database
                period_id = self.table_widget.item(row, 7)
                get_id = period_id.text()
                try:
                    period = Periods.get_by_id(get_id)
                    reply = QMessageBox.question(self, "تأكيدالحذف", "هل أنت متأكد أنك تريد حذف هذا الوردية",
                                                 QMessageBox.Yes | QMessageBox.No)
                    if reply == QMessageBox.Yes:
                        self.table_widget.removeRow(row)
                        period.delete_instance()
                        QMessageBox.information(self, "نجاح", "تم الحذف بنجاح")
                except Shifts.DoesNotExist:
                    print("shift_time does not exist.")
        # else:
        #     QMessageBox.information(self, "الصلاحية", "ليس لديك الصلاحية")

    def on_update_button_clicked(self):
        # result_condition = Common.grant_permission_to_clicked_button(self, permission="bt_update_attendance")
        # if result_condition is True:

        clicked_button = self.sender()
        if clicked_button:
            cell_widget = clicked_button.parentWidget()
            if cell_widget and self.table_widget:
                row = self.table_widget.indexAt(cell_widget.pos()).row()
                period_id = self.table_widget.item(row, 7)
                name = self.table_widget.item(row, 8)
                AttendanceTime = self.table_widget.item(row, 9)
                LeavingTime = self.table_widget.item(row, 10)
                pricePeriod = self.table_widget.item(row, 11)
                AllowedTimeForAttendance = self.table_widget.item(row, 12)
                AllowedTimeForLeaving = self.table_widget.item(row, 13)
                print("the attendence is:", AttendanceTime.text())
                print("the leaving is:", LeavingTime.text())

                if period_id and name and LeavingTime and AttendanceTime \
                        and LeavingTime and pricePeriod and AllowedTimeForAttendance and AllowedTimeForLeaving:

                    attendance_time = QTime.fromString(AttendanceTime.text(), "hh:mm")
                    leaving_time = QTime.fromString(LeavingTime.text(), "hh:mm")

                    period_dialog = PeriodDialog()
                    period_dialog.labAddPeriod.setText(period_id.text())
                    period_dialog.labAddPeriod.setVisible(False)
                    period_dialog.combPeriodName.setCurrentText(name.text())
                    period_dialog.timeAttendanceTime.setTime(attendance_time)
                    period_dialog.timeLeavingTime.setTime(leaving_time)
                    period_dialog.txtPricePeriod.setPlainText(pricePeriod.text())
                    period_dialog.timeAllowedTimeForAttendance.setPlainText(AllowedTimeForAttendance.text())
                    period_dialog.timeAllowedTimeForLeaving.setPlainText(AllowedTimeForLeaving.text())

                    if period_dialog.exec_() == QDialog.Accepted:
                        NamePeriod, entry_start_time_str, entry_end_time_str, PricePeriod, AllowedTimeForAttendance, AllowedTimeForLeavingt = period_dialog.save_data_period()
                        period_id = period_dialog.labAddPeriod.text()
                        periods = Periods.get_by_id(period_id)
                        periods.name = NamePeriod
                        periods.attendance_time = entry_start_time_str
                        periods.departure_time = entry_end_time_str
                        periods.period_price = PricePeriod
                        periods.time_allowed_for_late = AllowedTimeForAttendance
                        periods.time_allowed_for_leaving = AllowedTimeForLeavingt
                        periods.save()

                        self.table_widget.setItem(row, 8, QTableWidgetItem(NamePeriod))
                        self.table_widget.setItem(row, 9, QTableWidgetItem(entry_start_time_str))
                        self.table_widget.setItem(row, 10, QTableWidgetItem(entry_end_time_str))
                        self.table_widget.setItem(row, 11, QTableWidgetItem(PricePeriod))
                        self.table_widget.setItem(row, 12, QTableWidgetItem(AllowedTimeForAttendance))
                        self.table_widget.setItem(row, 13, QTableWidgetItem(AllowedTimeForLeavingt))

                        Common.style_table_widget(self, self.table_widget)

                        QMessageBox.information(self, "تعديل", "تم التعديل  بنجاح.")
