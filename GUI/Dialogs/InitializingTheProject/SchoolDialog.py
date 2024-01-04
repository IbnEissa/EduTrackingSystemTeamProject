import peewee
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from GUI.Dialogs.InitializingTheProject.TermSessionsInit import TermSessionsInit, DeleteUpdateButtonTermInitWidget
from GUI.Dialogs.InitializingTheProject.classesDialog import ClassesDialog
# from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonShiftsWidget
from GUI.Dialogs.shift_timeDialog import Shift_timedialog
from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
from models.Device import Device
from models.Permissions import Permissions
# from models.City import Cities
from models.School import School
from models.Shifts import Shifts
from models.Subjects import Subjects
from models.Users import Users
from models.term_table import TeacherSubjectClassRoomTermTable


class SchoolDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("newinitDialog.ui", self)
        self.state = 'False'
        self.initialization = 'False'
        self.lastInsertedTermSession = ""
        self.lastInsertedShifts = ""
        self.get_cities_combo_data()
        self.tabinitialize.tabBar().setVisible(False)
        self.comboMajorName.setEditable(True)

        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)

    # this is the method that makes the design of the dialog very good

    def use_ui_elements(self):
        self.comboCity.currentIndexChanged.connect(self.on_city_select)

        self.btnMoveSubjects.clicked.connect(self.skipping_subjects)
        self.btnMoveClassess.clicked.connect(self.skipping_classroom)
        self.btnMoveTermSessions.clicked.connect(self.skipping_sessions)

        self.btnAddSchool.clicked.connect(self.add_school_data)
        self.btnAddSubject.clicked.connect(self.add_to_subject_table)
        self.btnAddClasses.clicked.connect(self.add_to_classroom_table)
        self.btAddSession.clicked.connect(self.add_to_session_table)
        self.btnAddShift.clicked.connect(self.add_to_shift_table)

        self.btnDeleteSubject.clicked.connect(self.delete_from_subject_table)
        self.btnDeleteClassroom.clicked.connect(self.delete_from_classroom_table)
        self.btnDeleteSession.clicked.connect(self.delete_from_session_table)
        self.btnDeleteShift.clicked.connect(self.delete_from_shift_table)

        self.btnCancelSchool.clicked.connect(self.backwards_subjects)
        self.btnCancelAddingClasses.clicked.connect(self.backwards_classroom)
        self.btnCancelTermSessions.clicked.connect(self.backwards_session)
        self.btnCancelShift.clicked.connect(self.backwards_shift)



        self.btnSaveAll.clicked.connect(self.save_all_data)
    def get_cities_combo_data(self):
        cities = Common.get_cities(self)
        self.comboCity.clear()
        self.comboCity.addItems(cities)

    def on_city_select(self, index):
        selected_city = self.comboCity.currentText()
        cities = Common.get_cities(self)
        directorates = cities[selected_city]
        self.combDirectorates.clear()
        self.combDirectorates.addItems(directorates)

    def skipping_subjects(self):
        if self.tblsubject.rowCount() > 0:
            self.tabinitialize.setCurrentIndex(2)
            self.secondlabel.setStyleSheet("color: white; background-color: olive;")
        else:
            QMessageBox.warning(self, "تحذير", "يجب تهيئة اسماء المواد")

    def skipping_classroom(self):
        if self.tblClassRoom.rowCount() > 0:
            for row in range(self.tblClassRoom.rowCount()):
                name = self.tblClassRoom.item(row, 0).text()
                self.comboClasses.addItem(name)
            for row in range(self.tblsubject.rowCount()):
                name = self.tblsubject.item(row, 0).text()
                self.comboSubjects.addItem(name)

            self.tabinitialize.setCurrentIndex(3)
            self.thirdlabel.setStyleSheet("color: white; background-color: olive;")
        else:
            QMessageBox.warning(self, "تحذير", "يجب تهيئة اسماء الفصول")

    def skipping_sessions(self):
        self.tabinitialize.setCurrentIndex(4)
        self.fourlabel.setStyleSheet("color: white; background-color: olive;")

    def add_school_data(self):
        try:
            name = self.txtSchoolName.toPlainText().strip()
            city = self.comboCity.currentText().strip()
            directorate = self.combDirectorates.currentText().strip()
            village = self.txtVillage.toPlainText().strip()
            academic_level = self.comboAcademicLevel.currentText().strip()
            student_gender_type = self.comboGenderType.currentText().strip()

            if name == "":
                raise ValueError("يجب ادخال إسم المدرسة")
            if city == "":
                raise ValueError("يجب ادخال إسم المحافظة")
            if directorate == "":
                raise ValueError("يجب ادخال إسم المديرية")
            if village == "":
                raise ValueError("يجب ادخال إسم القرية او العزلة")
            if academic_level == "":
                raise ValueError("يجب ادخال المستوى الاكاديمي")
            if student_gender_type == "":
                raise ValueError("يجب ادخال نوع الطلاب")

            self.firstlabel.setStyleSheet("color: white; background-color: olive;")
            self.tabinitialize.setCurrentIndex(1)
            return name, city, directorate, village, academic_level, student_gender_type

        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)

    def add_to_subject_table(self):
        try:
            name = self.txtSubjectName.toPlainText()
            if name.strip() == "":
                raise ValueError("يجب ادخال إسم المادة ")
            current_row = self.tblsubject.rowCount()

            self.tblsubject.insertRow(current_row)
            self.tblsubject.setItem(current_row, 0, QTableWidgetItem(name))
            self.txtSubjectName.clear()
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)

    def add_to_classroom_table(self):
        class_name = self.txtClassName.toPlainText()
        major_name = self.comboMajorName.currentText()
        self.comboMajorName.setEditable(False)
        class_dialog = ClassesDialog()
        class_dialog.add_new_classroom(class_name, major_name)
        if class_name:
            current_row = self.tblClassRoom.rowCount()  # Get the current row index
            self.tblClassRoom.insertRow(current_row)  # Insert a new row at the current row index
            self.tblClassRoom.setItem(current_row, 0, QTableWidgetItem(class_name))
            self.tblClassRoom.setItem(current_row, 1, QTableWidgetItem(major_name))
            Common.style_table_widget(self, self.tblClassRoom)
            self.txtClassName.clear()
            self.comboMajorName.clear()
            self.comboMajorName.setEditable(True)
        # return class_name, major_name

    def add_to_session_table(self):

        try:

            self.comboClasses.setEditable(True)
            self.comboSubjects.setEditable(True)

            class_name = self.comboClasses.currentText()
            subject = self.comboSubjects.currentText()
            number_of_sessions = self.txtNumberOfSessions.toPlainText()

            if number_of_sessions.strip() == "":
                raise ValueError("يجب ادخال عدد الحصص ")
            if not number_of_sessions.isdigit():
                raise ValueError("يجب إدخال قيمة رقمية ")

            exists = False
            for row in range(self.tblTermSessions.rowCount()):
                if self.tblTermSessions.item(row, 0).text() == class_name and self.tblTermSessions.item(row,
                                                                                                        1).text() == subject:
                    exists = True
                    break

            if exists:
                QMessageBox.warning(self, "تحذير", "تم تهيئة المادة لهذا الفصل")
            else:
                self.tblTermSessions.insertRow(self.tblTermSessions.rowCount())
                self.tblTermSessions.setItem(self.tblTermSessions.rowCount() - 1, 0, QTableWidgetItem(class_name))
                self.tblTermSessions.setItem(self.tblTermSessions.rowCount() - 1, 1, QTableWidgetItem(subject))
                self.tblTermSessions.setItem(self.tblTermSessions.rowCount() - 1, 2,
                                             QTableWidgetItem(str(number_of_sessions)))
                Common.style_table_widget(self, self.tblTermSessions)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)

    def add_to_shift_table(self):

        name = self.txtshift_name.toPlainText()
        start_shift = self.dateStartShift.date().toPyDate()
        end_shift = self.dateEndShift.date().toPyDate()
        shifts_dialog = Shift_timedialog()
        shifts_dialog.save_data_shift(name, start_shift, end_shift)
        if name and start_shift and end_shift:
            current_row = self.tblshifts.rowCount()
            self.tblshifts.insertRow(current_row)
            self.tblshifts.setItem(current_row, 0, QTableWidgetItem(name))
            self.tblshifts.setItem(current_row, 1, QTableWidgetItem(str(start_shift)))
            self.tblshifts.setItem(current_row, 2, QTableWidgetItem(str(end_shift)))

            Common.style_table_widget(self, self.tblshifts)

    def delete_from_subject_table(self):
        selected_row = self.tblsubject.currentRow()
        if selected_row >= 0:
            self.tblsubject.removeRow(selected_row)

    def delete_from_classroom_table(self):
        selected_row = self.tblClassRoom.currentRow()
        if selected_row >= 0:
            self.tblClassRoom.removeRow(selected_row)

    def delete_from_session_table(self):
        selected_row = self.tblTermSessions.currentRow()
        if selected_row >= 0:
            self.tblTermSessions.removeRow(selected_row)

    def delete_from_shift_table(self):
        selected_row = self.tblshifts.currentRow()
        if selected_row >= 0:
            self.tblshifts.removeRow(selected_row)

    # this subject dialog
    def backwards_subjects(self):
        self.tabinitialize.setCurrentIndex(0)
        self.firstlabel.setStyleSheet("color: black; background-color: white;")

    def backwards_classroom(self):
        self.tabinitialize.setCurrentIndex(1)
        self.secondlabel.setStyleSheet("color: black; background-color: white;")

    def backwards_session(self):
        self.tabinitialize.setCurrentIndex(2)
        self.thirdlabel.setStyleSheet("color: black; background-color: white;")

    def backwards_shift(self):
        self.tabinitialize.setCurrentIndex(3)
        self.fourlabel.setStyleSheet("color: black; background-color: white;")


    def save_all_data(self):
        name, city, directorate, village, academic_level, student_gender_type = self.add_school_data()
        school = School.add(name, city, directorate, village, academic_level, student_gender_type)
        if school:
            default_device = Device(
                school_id=school.id,
                name=school.school_name,
                ip='192.168.1.201',
                port='4370',
                status='غير متصل',
            )
            default_device.save()

        # save  subjects
        for row in range(self.tblsubject.rowCount()):
            name = self.tblsubject.item(row, 0).text()

            Subjects.insert({
                ClassRoom.name: name,

            }).execute()

        self.tblsubject.clearContents()
        self.tblsubject.setRowCount(0)
        # save classes
        lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
        for row in range(self.tblClassRoom.rowCount()):
            name = self.tblClassRoom.item(row, 0).text()
            major_name = self.tblClassRoom.item(row, 1).text()

            ClassRoom.insert({
                ClassRoom.school_id: lastInsertedSchoolId,
                ClassRoom.name: name,
                ClassRoom.Name_major: major_name,

            }).execute()
        # save sessions
        for row in range(self.tblTermSessions.rowCount()):
            class_name = self.tblTermSessions.item(row, 0).text()
            subject = self.tblTermSessions.item(row, 1).text()
            number_of_sessions = self.tblTermSessions.item(row, 2).text()

            class_id = ClassRoom.get_class_id_from_name(self, class_name)

            TeacherSubjectClassRoomTermTable.insert({
                TeacherSubjectClassRoomTermTable.subject_id: subject,
                TeacherSubjectClassRoomTermTable.class_room_id: class_id,
                TeacherSubjectClassRoomTermTable.number_of_lessons: number_of_sessions,
            }).execute()

        # save shifts
        for row in range(self.tblshifts.rowCount()):
            name = self.tblshifts.item(row, 0).text()
            start_shift = self.tblshifts.item(row, 1).text()
            end_shift = self.tblshifts.item(row, 2).text()
            Shifts.insert({
                Shifts.name: name,
                Shifts.start_date_shift: start_shift,
                Shifts.end_date_shift: end_shift,

            }).execute()

        self.fiveabel.setStyleSheet("color: white; background-color: olive;")
        self.accept()
        QMessageBox.information(self, "نجاح", "تم تهيئة  النظام بنجاح ")