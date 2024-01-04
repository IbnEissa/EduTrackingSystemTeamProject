import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

from GUI.Dialogs.InitializingTheProject.TermSessionsInit import TermSessionsInit
from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeachersWidget
from GUI.Dialogs.TeacherDialog import TeacherDialog
from GUI.Views.CommonFunctionality import Common
from models.Device import Device
from models.Members import Members
from models.School import School
from models.Subjects import Subjects
from models.Teachers import Teachers


class TeachersInit(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("teachersInit.ui", self)
        self.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        self.lastInsertedTeacherId = 0
        self.lastInsertedMemberId = 0
        self.use_ui_elements()

    def use_ui_elements(self):
        self.btnAddNewTeacher.clicked.connect(self.add_members_database)
        self.btnSkippingTeachers.clicked.connect(self.skipping_teachers)

    # def delete_from_list(self):
    #     self.listTeachers.takeItem(self.listTeachers.currentRow())

    # def add_new_teacher_to_list_view(self, teacher):
    #     teacher_str = ' '.join(teacher)  # Convert the list to a single string
    #     self.listTeachers.addItem(teacher_str)
    def skipping_teachers(self):
        term = TermSessionsInit()
        term.use_ui_elements()
        self.reject()
        term.exec_()

    def add_members_database(self):
        Common.style_table_widget(self, self.listTeachers)
        teacher_dialog = TeacherDialog()
        if teacher_dialog.exec_() == QDialog.Accepted:
            try:
                lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                FName, SName, TName, LName, Phone, DOB, Major, Task, state = teacher_dialog.save_data()
                Members.insert({
                    Members.school_id: lastInsertedSchoolId,
                    Members.fName: FName,
                    Members.sName: SName,
                    Members.tName: TName,
                    Members.lName: LName,
                    Members.phone: Phone,
                    Members.dateBerth: DOB,
                }).execute()
                self.lastInsertedMemberId = Members.select(peewee.fn.Max(Members.id)).scalar()
                Teachers.insert({
                    Teachers.members_id: self.lastInsertedMemberId,
                    Teachers.major: Major,
                    Teachers.task: Task,
                    Teachers.state: state,
                }).execute()
                has_finger_print_data = 'لا'
                teacher = [self.lastInsertedTeacherId, FName, SName, TName, LName, state, has_finger_print_data]
                self.lastInsertedTeacherId = Teachers.select(peewee.fn.Max(Teachers.id)).scalar()
                # self.get_members_data()
                fullName = [teacher[0], teacher[1], teacher[3]]
                print(fullName)
                operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.listTeachers)
                result = operations_buttons.add_users_to_device(self.lastInsertedTeacherId)
                print("the data returned is : ", result)
                if result:
                    self.add_new_teacher_to_table_widget(teacher)
                    Common.style_table_widget(self, self.listTeachers)
                    QMessageBox.information(self, "نجاح", "تم الحفظ بنجاح")
                else:
                    QMessageBox.critical(self, "خطأ", "لم يتم الحفظ بنجاح")

            except ValueError as e:
                QMessageBox.critical(self, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")

    def add_new_teacher_to_table_widget(self, teacher):
        try:
            operations_buttons = DeleteUpdateButtonTeachersWidget(table_widget=self.listTeachers)
            current_row = self.listTeachers.rowCount()
            self.listTeachers.insertRow(current_row)
            self.listTeachers.setItem(current_row, 0, QTableWidgetItem(str(teacher[0])))
            self.listTeachers.setItem(current_row, 1, QTableWidgetItem(teacher[1]))
            self.listTeachers.setItem(current_row, 2, QTableWidgetItem(teacher[2]))
            self.listTeachers.setItem(current_row, 3, QTableWidgetItem(teacher[3]))
            self.listTeachers.setItem(current_row, 4, QTableWidgetItem(teacher[4]))
            self.listTeachers.setItem(current_row, 5, QTableWidgetItem(str(teacher[5])))
            # self.listTeachers.setItem(current_row, 6, QTableWidgetItem(str(teacher[6])))
            # self.listTeachers.setItem(current_row, 7, QTableWidgetItem(teacher[6]))
            # self.listTeachers.setItem(current_row, 8, QTableWidgetItem(teacher[7]))
            # self.listTeachers.setItem(current_row, 9, QTableWidgetItem(teacher[8]))
            # self.listTeachers.setItem(current_row, 10, QTableWidgetItem(teacher[9]))
            self.listTeachers.setCellWidget(current_row, 6, operations_buttons.get_buttons('Old'))
            self.listTeachers.setColumnWidth(current_row, 40)
            self.listTeachers.setRowHeight(current_row, 150)
            Common.style_table_widget(self, self.listTeachers)
            # self.add_to_members_to_device(str(teacher_id),teacher[0])
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self, "خطأ", error_message)

    # def add_teacher_data(self):
    #     teacher_dialog = TeacherDialog()
    #     if teacher_dialog.exec_() == QDialog.Accepted:
    #         try:
    #             lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
    #             FName, SName, TName, LName, Phone, DOB, Major, Task, state = teacher_dialog.save_data()
    #             Members.insert({
    #                 Members.school_id: lastInsertedSchoolId,
    #                 Members.fName: FName,
    #                 Members.sName: SName,
    #                 Members.tName: TName,
    #                 Members.lName: LName,
    #                 Members.phone: Phone,
    #                 Members.dateBerth: DOB,
    #             }).execute()
    #             self.lastInsertedMemberId = Members.select(peewee.fn.Max(Members.id)).scalar()
    #             Teachers.insert({
    #                 Teachers.members_id: self.lastInsertedMemberId,
    #                 Teachers.major: Major,
    #                 Teachers.task: Task,
    #                 Teachers.state: state,
    #             }).execute()
    #             has_finger_print_data = 'لا'
    #             teacher = [self.lastInsertedMemberId, FName, SName, TName, LName, Phone, DOB, Major, Task, state,
    #                        has_finger_print_data]
    #             self.lastInsertedTeacherId = Teachers.select(peewee.fn.Max(Teachers.id)).scalar()
    #             fullName = [str(teacher[0]), teacher[1], teacher[3], teacher[4]]
    #             self.add_new_teacher_to_list_view(fullName)
    #             QMessageBox.information(self, "نجاح", "تم الحفظ بنجاح")
    #
    #         except ValueError as e:
    #             QMessageBox.critical(self, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")
