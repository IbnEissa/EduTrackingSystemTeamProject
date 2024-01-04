import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonUsersWidget, DeleteUpdateButtonTeachersWidget, \
    DeleteUpdateButtonStudentsWidget
from GUI.Dialogs.UserDialog import UserDialog
from GUI.Dialogs.UserLoginDialog import UserLoginDialog
from GUI.Views.CommonFunctionality import Common
from GUI.Views.PermissionUI import PermissionUI
from models.Members import Members
from models.School import School
from models.Teachers import Teachers
from models.Users import Users
from models.Permissions import Permissions


class UsersUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedUserId = 0
        self.ui.tblUsers.setColumnHidden(0, True)
        self.ui.tblUsers.setColumnHidden(9, True)
        self.state = 'False'
        self.initialization = 'False'

    def use_ui_elements(self):
        self.ui.tblUsers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblUsers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblUsers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewUser.clicked.connect(self.add_new_user)
        self.ui.txtUsersSearch.textChanged.connect(self.get_users_data)

    def login(self):
        user_login = UserLoginDialog()
        user_login.use_ui_elements()
        user_login.exec_()
        result = user_login.login()
        if result is True:
            return True
        else:
            return False
    def add_new_user(self):
        # result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_save_user")
        # if result_condition is True:
        user_dialog = UserDialog()
        if user_dialog.exec_() == QDialog.Accepted:
            try:
                # lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                account_type, name, user_name, password = user_dialog.save_data()
                # teacher = Members.get((Members.fName + ' ' + Members.lName) == name)
                # id_user = teacher.id
                Users.insert({
                    Users.account_type: account_type,
                    Users.Name: name,
                    Users.userName: user_name,
                    Users.userPassword: password,
                    Users.state: self.state,
                    Users.initialization: self.initialization,
                }).execute()
                self.lastInsertedUserId = Users.select(peewee.fn.Max(Users.id)).scalar()
                Permissions.insert({
                    Permissions.users_id: self.lastInsertedUserId,
                    Permissions.led_main: False,
                    Permissions.led_manage: False,
                    Permissions.led_setting: False,

                    Permissions.bt_save_student: False,
                    Permissions.bt_search_student: False,
                    Permissions.bt_update_student: False,
                    Permissions.bt_delete_student: False,
                    Permissions.bt_export_student: False,
                    Permissions.bt_show_student: False,
                    Permissions.bt_reports_student: False,

                    Permissions.bt_save_teacher: False,
                    Permissions.bt_search_teacher: False,
                    Permissions.bt_update_teacher: False,
                    Permissions.bt_delete_teacher: False,
                    Permissions.bt_export_teacher: False,
                    Permissions.bt_show_teacher: False,
                    Permissions.bt_reports_teacher: False,

                    Permissions.bt_save_fathers: False,
                    Permissions.bt_search_fathers: False,
                    Permissions.bt_update_fathers: False,
                    Permissions.bt_delete_fathers: False,

                    Permissions.bt_save_user: False,
                    Permissions.bt_search_user: False,
                    Permissions.bt_update_user: False,
                    Permissions.bt_delete_user: False,

                    Permissions.bt_save_device: False,
                    Permissions.bt_search_device: False,
                    Permissions.bt_update_device: False,
                    Permissions.bt_delete_device: False,
                    Permissions.bt_export_device: False,
                    Permissions.bt_show_device: False,

                    Permissions.bt_save_attendance: False,
                    Permissions.bt_search_attendance: False,
                    Permissions.bt_update_attendance: False,
                    Permissions.bt_delete_attendance: False,
                    Permissions.bt_export_attendance: False,
                    Permissions.bt_show_attendance: False,

                    Permissions.bt_save_timetable_student: False,
                    Permissions.bt_show_timetable_student: False,
                    Permissions.bt_export_timetable_student: False,

                    Permissions.bt_show_timetable_teacher: False,
                    # Permissions.bt_save_timetable_teacher: False,
                    # Permissions.bt_export_timetable_teacher: False,

                }).execute()
                user = Users.get(Users.id == self.lastInsertedUserId)
                creation_date = user.created_at
                update_date = user.updated_at
                user = [self.lastInsertedUserId, account_type, name, user_name, password, creation_date,update_date,self.state,self.initialization]
                self.add_new_user_to_table_widget(user)
                Common.style_table_widget(self.ui, self.ui.tblStudents)
                QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                # PermissionUI.add_permission_to_user()
            except ValueError as e:
                QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")

        # else:
        #     QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

    def add_new_user_to_table_widget(self, user):
        self.ui.tblUsers.setRowCount(0)
        try:
            operationsButtons = DeleteUpdateButtonUsersWidget(table_widget=self.ui.tblUsers)
            current_row = self.ui.tblUsers.rowCount()  # Get the current row index
            self.ui.tblUsers.insertRow(current_row)  # Insert a new row at the current row index
            self.ui.tblUsers.setItem(current_row, 0, QTableWidgetItem(user[0]))
            self.ui.tblUsers.setItem(current_row, 1, QTableWidgetItem(user[1]))
            self.ui.tblUsers.setItem(current_row, 2, QTableWidgetItem(user[2]))
            self.ui.tblUsers.setItem(current_row, 3, QTableWidgetItem(user[3]))
            self.ui.tblUsers.setItem(current_row, 4, QTableWidgetItem(user[4]))
            self.ui.tblUsers.setItem(current_row, 5, QTableWidgetItem(str(user[5])))
            self.ui.tblUsers.setItem(current_row, 6, QTableWidgetItem(str(user[6])))
            self.ui.tblUsers.setItem(current_row, 7, QTableWidgetItem(str(user[7])))
            self.ui.tblUsers.setItem(current_row, 8, QTableWidgetItem(str(user[8])))
            self.ui.tblUsers.setCellWidget(current_row, 9, operationsButtons)
            self.ui.tblUsers.setColumnWidth(current_row, 40)
            self.ui.tblUsers.setRowHeight(current_row, 150)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def get_users_data(self):
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_search_user")
        if result_condition is True:
            self.ui.tblUsers.setColumnHidden(9, False)
            Common.style_table_widget(self.ui, self.ui.tblStudents)
            try:
                columns = ['id', 'account_type', 'Name', 'userName', 'userPassword', 'created_at', 'updated_at',
                           'state',
                           'initialization']
                search_item = self.ui.txtUsersSearch.toPlainText().lower()
                members_query = Users.select().where(
                    peewee.fn.LOWER(Users.Name).contains(search_item)).distinct()
                self.ui.tblUsers.setRowCount(0)  # Clear existing rows in the table
                for row, member_data in enumerate(members_query):
                    table_items = []
                    for column_name in columns:
                        try:
                            item_value = getattr(member_data, column_name)
                        except AttributeError:
                            User_data = Users.get(Users.id)
                            item_value = getattr(User_data, column_name)

                        table_item = QTableWidgetItem(str(item_value))
                        table_items.append(table_item)

                    self.ui.tblUsers.insertRow(row)
                    for col, item in enumerate(table_items):
                        self.ui.tblUsers.setItem(row, col, item)

                    self.ui.tblUsers.setColumnWidth(row, 40)
                    self.ui.tblUsers.setRowHeight(row, 150)

                    operations_buttons = DeleteUpdateButtonUsersWidget(table_widget=self.ui.tblUsers)
                    self.ui.tblUsers.setCellWidget(row, 9, operations_buttons)
                    Common.style_table_widget(self.ui, self.ui.tblUsers)
            except Exception as e:
                error_message = "حدث خطأ:\n\n" + str(e)
                QMessageBox.critical(self.ui, "خطأ", error_message)
        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")
