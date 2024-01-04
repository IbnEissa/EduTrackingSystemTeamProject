import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonStudentsWidget
from GUI.Dialogs.StudentDialog import StudentDialog
from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
from models.Members import Members
from models.School import School
from models.Students import Students


class StudentsUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.lastInsertedStudentId = 0
        self.id = 0
        self.ui.tblStudents.setColumnHidden(0, True)
        self.ui.tblStudents.setColumnHidden(2, True)
        _translate = QtCore.QCoreApplication.translate
        self.ui.txtStudentsSearch.setPlaceholderText(_translate("Dialog", "بحث ... "))

    def use_ui_elements(self):
        self.ui.tblStudents.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblStudents.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblStudents.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewStudent.clicked.connect(self.add_members_database)
        self.ui.txtStudentsSearch.textChanged.connect(self.get_member_data)

    def add_members_database(self):
        self.ui.tblStudents.setRowCount(0)
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_save_student")
        if result_condition is True:
            student_dialog = StudentDialog()
            if student_dialog.exec_() == QDialog.Accepted:
                try:
                    lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                    FName, LName, gender, ClassId, Birth, Phone, ClassName = student_dialog.save_data()
                    lastInsertedMemberId = Members.insert({
                        Members.school_id: lastInsertedSchoolId,
                        Members.fName: FName,
                        Members.lName: LName,
                        Members.dateBerth: Birth,
                        Members.phone: Phone,
                        Members.type: "طالب",
                        Members.gender: gender,
                    }).execute()
                    # self.lastInsertedMemberId = Members.select(peewee.fn.Max(Members.id)).scalar()
                    Students.insert({
                        Students.member_id: lastInsertedMemberId,
                        Students.class_id: ClassId,
                    }).execute()
                    self.lastInsertedStudentId = Students.select(peewee.fn.Max(Students.member_id)).scalar()
                    student = [FName, LName, gender, ClassId, Birth, Phone, ClassName]
                    self.add_new_student_to_table_widget(self.lastInsertedStudentId, student)
                    QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                except ValueError as e:
                    QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")
        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

    def add_new_student_to_table_widget(self, student_id, student):
        try:

            current_row = self.ui.tblStudents.rowCount()  # Get the current row index
            self.ui.tblStudents.insertRow(current_row)  # Insert a new row at the current row index
            self.ui.tblStudents.setItem(current_row, 0, QTableWidgetItem(str(student_id)))
            self.ui.tblStudents.setItem(current_row, 1, QTableWidgetItem(student[0] + ' ' + student[1]))
            self.ui.tblStudents.setItem(current_row, 2, QTableWidgetItem(student[1]))
            self.ui.tblStudents.setItem(current_row, 3, QTableWidgetItem(student[2]))
            self.ui.tblStudents.setItem(current_row, 4, QTableWidgetItem(student[6]))
            self.ui.tblStudents.setItem(current_row, 5, QTableWidgetItem(str(student[4])))
            self.ui.tblStudents.setItem(current_row, 6, QTableWidgetItem(str(student[5])))
            operations_buttons = DeleteUpdateButtonStudentsWidget(table_widget=self.ui.tblStudents)
            self.ui.tblStudents.setCellWidget(current_row, 7, operations_buttons)
            self.ui.tblStudents.setColumnWidth(current_row, 40)
            self.ui.tblStudents.setRowHeight(current_row, 150)
            Common.style_table_widget(self.ui, self.ui.tblStudents)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def get_member_data(self):
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_search_student")
        if result_condition:
            self.ui.tblStudents.setColumnHidden(8, False)
            self.ui.tblStudents.setRowCount(0)
            search_item = self.ui.txtStudentsSearch.text().lower()
            students = Members.select().where(Members.fName.contains(search_item) | Members.lName.contains(search_item))
            for student in students:
                studentData = Students.get_or_none(Students.member_id == student.id)
                if studentData:
                    class_id = studentData.class_id
                    class_room = ClassRoom.get_by_id(class_id)
                    row = self.ui.tblStudents.rowCount()
                    self.ui.tblStudents.insertRow(row)
                    self.ui.tblStudents.setItem(row, 0, QTableWidgetItem(str(student.id)))
                    self.ui.tblStudents.setItem(row, 1, QTableWidgetItem(f"{student.fName} {student.lName}"))
                    self.ui.tblStudents.setItem(row, 2, QTableWidgetItem(str(student.lName)))
                    self.ui.tblStudents.setItem(row, 3, QTableWidgetItem(str(student.gender)))
                    self.ui.tblStudents.setItem(row, 4, QTableWidgetItem(str(class_room.name)))
                    self.ui.tblStudents.setItem(row, 5, QTableWidgetItem(str(student.dateBerth)))
                    self.ui.tblStudents.setItem(row, 6, QTableWidgetItem(str(student.phone)))
                    self.ui.tblStudents.setColumnWidth(row, 40)
                    self.ui.tblStudents.setRowHeight(row, 150)
                    self.ui.tblStudents.setCellWidget(row, 7, DeleteUpdateButtonStudentsWidget(
                        table_widget=self.ui.tblStudents))
                    Common.style_table_widget(self.ui, self.ui.tblStudents)

        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")
            # def get_member_data(self):
            #     result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_search_student")
            #     if result_condition is True:
            #         self.ui.tblStudents.setColumnHidden(8, False)
            #         self.ui.tblStudents.setRowCount(0)
            #         students_data = Students.select()
            #         for student in students_data:
            #             operations_buttons = DeleteUpdateButtonStudentsWidget(table_widget=self.ui.tblStudents)
            #             member = Members.get_by_id(student.member_id)
            #             student = Students.get_by_id(student.member_id)
            #             row = self.ui.tblStudents.rowCount()
            #             class_id=student.class_id
            #             class_name=ClassRoom.get_by_id(ClassRoom.class_id)
            #             self.ui.tblStudents.insertRow(row)
            #             self.ui.tblStudents.setItem(row, 0, QTableWidgetItem(str(member.id)))
            #             self.ui.tblStudents.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
            #             self.ui.tblStudents.setItem(row, 2, QTableWidgetItem(str(member.lName)))
            #             self.ui.tblStudents.setItem(row, 3, QTableWidgetItem(str(class_name)))
            #             self.ui.tblStudents.setItem(row, 4, QTableWidgetItem(str(member.dateBerth)))
            #             self.ui.tblStudents.setItem(row, 5, QTableWidgetItem(str(member.phone)))
            #             self.ui.tblStudents.setColumnWidth(row, 40)
            #             self.ui.tblStudents.setRowHeight(row, 150)
            #             self.ui.tblStudents.setCellWidget(row, 6, operations_buttons)
            #             Common.style_table_widget(self.ui, self.ui.tblStudents)
            #     else:
            #         QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")
