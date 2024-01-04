import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
from models.Users import Users
from models.Permissions import Permissions


class PermissionUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        # self.ips = ''
        # self.ports = ''
        # self.lastInsertedMemberId = 0
        # self.lastInsertedUserId = 0
        # self.ui.tblUsers.setColumnHidden(0, True)
        # self.state = 'False'
        # self.initialization = 'False'
        self.add_user_to_comb()

    def permission_ui_elements(self):
        self.ui.SavePermisson.clicked.connect(self.add_permission_to_user)
        self.ui.ShowPermisson.clicked.connect(self.show_permission_for_user)
        self.ui.SelectedAll.stateChanged.connect(self.handle_checkbox_change)

    def add_user_to_comb(self):
        user_comb_permission = [user.Name for user in Users.select(Users.Name)]
        self.ui.CobUserPerm.addItems(user_comb_permission)
        # print(user_comb_permission)

    def add_permission_to_user(self):
        selected_user = self.ui.CobUserPerm.currentText()
        user = Users.get(Users.Name == selected_user)
        user_id = user.id

        # Update the Permissions table based on checkbox states
        permissions = Permissions.get(users_id=user_id)

        permissions.led_main = self.ui.led_main.isChecked()
        permissions.led_manage = self.ui.led_manage.isChecked()
        permissions.led_setting = self.ui.led_setting.isChecked()
        # grant permissions to student tab
        permissions.bt_save_student = self.ui.bt_save_student.isChecked()
        permissions.bt_search_student = self.ui.bt_search_student.isChecked()
        permissions.bt_update_student = self.ui.bt_update_student.isChecked()
        permissions.bt_delete_student = self.ui.bt_delete_student.isChecked()
        # permissions.bt_reports_student = self.ui.bt_reports_student.isChecked()
        permissions.bt_show_student = self.ui.bt_show_student.isChecked()
        permissions.bt_export_student = self.ui.bt_export_student.isChecked()

        # grant permissions to teacher tab
        permissions.bt_save_teacher = self.ui.bt_save_teacher.isChecked()
        permissions.bt_search_teacher = self.ui.bt_search_teacher.isChecked()
        permissions.bt_update_teacher = self.ui.bt_update_teacher.isChecked()
        permissions.bt_delete_teacher = self.ui.bt_delete_teacher.isChecked()
        permissions.bt_reports_teacher = self.ui.bt_reports_teacher.isChecked()
        permissions.bt_show_teacher = self.ui.bt_show_teacher.isChecked()
        permissions.bt_export_teacher = self.ui.bt_export_teacher.isChecked()
        # grant permissions to fathers   tab
        permissions.bt_save_fathers = self.ui.bt_save_fathers.isChecked()
        permissions.bt_search_fathers = self.ui.bt_search_fathers.isChecked()
        permissions.bt_update_fathers = self.ui.bt_update_fathers.isChecked()
        permissions.bt_delete_fathers = self.ui.bt_delete_fathers.isChecked()
        # grant permissions to user  tab
        permissions.bt_save_user = self.ui.bt_save_user.isChecked()
        permissions.bt_search_user = self.ui.bt_search_user.isChecked()
        permissions.bt_update_user = self.ui.bt_update_user.isChecked()
        permissions.bt_delete_user = self.ui.bt_delete_user.isChecked()
        # grant permissions to device  tab
        permissions.bt_save_device = self.ui.bt_save_device.isChecked()
        permissions.bt_search_device = self.ui.bt_search_device.isChecked()
        permissions.bt_update_device = self.ui.bt_update_device.isChecked()
        permissions.bt_delete_device = self.ui.bt_delete_device.isChecked()
        permissions.bt_export_device = self.ui.bt_export_device.isChecked()
        permissions.bt_show_device = self.ui.bt_show_device.isChecked()
        # grant permissions to attendance   tab
        permissions.bt_save_attendance = self.ui.bt_save_attendance.isChecked()
        permissions.bt_search_attendance = self.ui.bt_search_attendance.isChecked()
        permissions.bt_update_attendance = self.ui.bt_update_attendance.isChecked()
        permissions.bt_delete_attendance = self.ui.bt_delete_attendance.isChecked()
        permissions.bt_export_attendance = self.ui.bt_export_attendance.isChecked()
        permissions.bt_show_attendance = self.ui.bt_show_attendance.isChecked()
        # grant permissions to timetable_student   tab
        permissions.bt_save_timetable_student = self.ui.bt_save_attendance.isChecked()
        permissions.bt_show_timetable_student = self.ui.bt_search_attendance.isChecked()
        permissions.bt_export_timetable_student = self.ui.bt_update_attendance.isChecked()
        # grant permissions to timetable_teacher   tab
        permissions.bt_show_timetable_teacher = self.ui.bt_search_attendance.isChecked()
        # permissions.bt_save_timetable_teacher = self.ui.bt_save_attendance.isChecked()
        # permissions.bt_export_timetable_teacher = self.ui.bt_update_attendance.isChecked()

        permissions.save()
        # Reset checkbox states
        self.ui.led_main.setChecked(False)
        self.ui.led_manage.setChecked(False)
        self.ui.led_setting.setChecked(False)
        # grant permissions to student  tab
        self.ui.bt_save_student.setChecked(False)
        self.ui.bt_search_student.setChecked(False)
        self.ui.bt_update_student.setChecked(False)
        self.ui.bt_delete_student.setChecked(False)
        self.ui.bt_reports_student.setChecked(False)
        self.ui.bt_show_student.setChecked(False)
        self.ui.bt_export_student.setChecked(False)
        # grant permissions to teacher  tab
        self.ui.bt_save_teacher.setChecked(False)
        self.ui.bt_search_teacher.setChecked(False)
        self.ui.bt_update_teacher.setChecked(False)
        self.ui.bt_delete_teacher.setChecked(False)
        self.ui.bt_reports_teacher.setChecked(False)
        self.ui.bt_show_teacher.setChecked(False)
        self.ui.bt_export_teacher.setChecked(False)
        # grant permissions to fathers  tab
        self.ui.bt_save_fathers.setChecked(False)
        self.ui.bt_search_fathers.setChecked(False)
        self.ui.bt_update_fathers.setChecked(False)
        self.ui.bt_delete_fathers.setChecked(False)
        # grant permissions to user  tab
        self.ui.bt_save_user.setChecked(False)
        self.ui.bt_search_user.setChecked(False)
        self.ui.bt_update_user.setChecked(False)
        self.ui.bt_delete_user.setChecked(False)
        # grant permissions to device  tab
        self.ui.bt_save_device.setChecked(False)
        self.ui.bt_search_device.setChecked(False)
        self.ui.bt_update_device.setChecked(False)
        self.ui.bt_delete_device.setChecked(False)
        self.ui.bt_export_device.setChecked(False)
        self.ui.bt_show_device.setChecked(False)
        # grant permissions to attendance  tab
        self.ui.bt_save_attendance.setChecked(False)
        self.ui.bt_search_attendance.setChecked(False)
        self.ui.bt_update_attendance.setChecked(False)
        self.ui.bt_delete_attendance.setChecked(False)
        self.ui.bt_export_attendance.setChecked(False)
        self.ui.bt_show_attendance.setChecked(False)
        # grant permissions to timetable_student  tab
        self.ui.bt_save_timetable_student.setChecked(False)
        self.ui.bt_show_timetable_student.setChecked(False)
        self.ui.bt_export_timetable_student.setChecked(False)
        # grant permissions to timetable_teacher  tab
        self.ui.bt_show_timetable_teacher.setChecked(False)
        # self.ui.bt_save_timetable_teacher.setChecked(False)
        # self.ui.bt_export_timetable_teacher.setChecked(False)

        QMessageBox.information(self.ui, "الصلاحيات", "تم حفظ التعديلات بنجاح")
        print(selected_user)
        print(user_id)

    def show_permission_for_user(self):
        selected_user = self.ui.CobUserPerm.currentText()
        user = Users.get(Users.Name == selected_user)
        user_id = user.id

        # Retrieve the Permissions for the selected user
        permissions = Permissions.get(users_id=user_id)

        # Set checkbox states based on field values
        self.ui.led_main.setChecked(permissions.led_main)
        self.ui.led_manage.setChecked(permissions.led_manage)
        self.ui.led_setting.setChecked(permissions.led_setting)
        # grant permissions to student  tab
        self.ui.bt_save_student.setChecked(permissions.bt_save_student)
        self.ui.bt_search_student.setChecked(permissions.bt_search_student)
        self.ui.bt_update_student.setChecked(permissions.bt_update_student)
        self.ui.bt_delete_student.setChecked(permissions.bt_delete_student)
        self.ui.bt_reports_student.setChecked(permissions.bt_reports_student)
        self.ui.bt_show_student.setChecked(permissions.bt_show_student)
        self.ui.bt_export_student.setChecked(permissions.bt_export_student)
        # grant permissions to teacher  tab
        self.ui.bt_save_teacher.setChecked(permissions.bt_save_teacher)
        self.ui.bt_search_teacher.setChecked(permissions.bt_search_teacher)
        self.ui.bt_update_teacher.setChecked(permissions.bt_update_teacher)
        self.ui.bt_delete_teacher.setChecked(permissions.bt_delete_teacher)
        self.ui.bt_reports_teacher.setChecked(permissions.bt_reports_teacher)
        self.ui.bt_show_teacher.setChecked(permissions.bt_show_teacher)
        self.ui.bt_export_teacher.setChecked(permissions.bt_export_teacher)
        # grant permissions to fathers  tab
        self.ui.bt_save_fathers.setChecked(permissions.bt_save_fathers)
        self.ui.bt_search_fathers.setChecked(permissions.bt_search_fathers)
        self.ui.bt_update_fathers.setChecked(permissions.bt_update_fathers)
        self.ui.bt_delete_fathers.setChecked(permissions.bt_delete_fathers)
        # grant permissions to user  tab
        self.ui.bt_save_user.setChecked(permissions.bt_save_user)
        self.ui.bt_search_user.setChecked(permissions.bt_search_user)
        self.ui.bt_update_user.setChecked(permissions.bt_update_user)
        self.ui.bt_delete_user.setChecked(permissions.bt_delete_user)
        # grant permissions to device.  tab
        self.ui.bt_save_device.setChecked(permissions.bt_save_device)
        self.ui.bt_search_device.setChecked(permissions.bt_search_device)
        self.ui.bt_update_device.setChecked(permissions.bt_update_device)
        self.ui.bt_delete_device.setChecked(permissions.bt_delete_device)
        self.ui.bt_export_device.setChecked(permissions.bt_export_device)
        self.ui.bt_show_device.setChecked(permissions.bt_show_device)
        # grant permissions to attendance  tab
        self.ui.bt_save_attendance.setChecked(permissions.bt_save_attendance)
        self.ui.bt_search_attendance.setChecked(permissions.bt_search_attendance)
        self.ui.bt_update_attendance.setChecked(permissions.bt_update_attendance)
        self.ui.bt_delete_attendance.setChecked(permissions.bt_delete_attendance)
        self.ui.bt_show_attendance.setChecked(permissions.bt_show_attendance)
        self.ui.bt_export_attendance.setChecked(permissions.bt_export_attendance)
        # grant permissions to timetable_student  tab
        self.ui.bt_save_timetable_student.setChecked(permissions.bt_save_timetable_student)
        self.ui.bt_show_timetable_student.setChecked(permissions.bt_show_timetable_student)
        self.ui.bt_export_timetable_student.setChecked(permissions.bt_export_timetable_student)
        # grant permissions to timetable_teacher  tab
        self.ui.bt_show_timetable_teacher.setChecked(permissions.bt_show_timetable_teacher)
        # self.ui.bt_save_timetable_teacher.setChecked(permissions.bt_save_attendance)
        # self.ui.bt_export_timetable_teacher.setChecked(permissions.bt_update_attendance)

    def set_all_checkboxes(self, checked):
        self.ui.led_main.setChecked(checked)
        self.ui.led_manage.setChecked(checked)
        self.ui.led_setting.setChecked(checked)
        # grant permissions to student  tab
        self.ui.bt_save_student.setChecked(checked)
        self.ui.bt_search_student.setChecked(checked)
        self.ui.bt_update_student.setChecked(checked)
        self.ui.bt_delete_student.setChecked(checked)
        self.ui.bt_reports_student.setChecked(checked)
        self.ui.bt_show_student.setChecked(checked)
        self.ui.bt_export_student.setChecked(checked)
        # grant permissions to teacher  tab
        self.ui.bt_save_teacher.setChecked(checked)
        self.ui.bt_search_teacher.setChecked(checked)
        self.ui.bt_update_teacher.setChecked(checked)
        self.ui.bt_delete_teacher.setChecked(checked)
        self.ui.bt_reports_teacher.setChecked(checked)
        self.ui.bt_show_teacher.setChecked(checked)
        # grant permissions to fathers  tab
        self.ui.bt_save_fathers.setChecked(checked)
        self.ui.bt_search_fathers.setChecked(checked)
        self.ui.bt_update_fathers.setChecked(checked)
        self.ui.bt_delete_fathers.setChecked(checked)
        # grant permissions to user  tab
        self.ui.bt_save_user.setChecked(checked)
        self.ui.bt_search_user.setChecked(checked)
        self.ui.bt_update_user.setChecked(checked)
        self.ui.bt_delete_user.setChecked(checked)
        # grant permissions to device  tab
        self.ui.bt_save_device.setChecked(checked)
        self.ui.bt_search_device.setChecked(checked)
        self.ui.bt_update_device.setChecked(checked)
        self.ui.bt_delete_device.setChecked(checked)
        self.ui.bt_export_device.setChecked(checked)
        self.ui.bt_show_device.setChecked(checked)
        # grant permissions to attendance  tab
        self.ui.bt_save_attendance.setChecked(checked)
        self.ui.bt_search_attendance.setChecked(checked)
        self.ui.bt_update_attendance.setChecked(checked)
        self.ui.bt_delete_attendance.setChecked(checked)
        self.ui.bt_export_attendance.setChecked(checked)
        self.ui.bt_show_attendance.setChecked(checked)
        # grant permissions to timetable_student tab
        self.ui.bt_save_timetable_student.setChecked(checked)
        self.ui.bt_show_timetable_student.setChecked(checked)
        self.ui.bt_export_timetable_student.setChecked(checked)
        # grant permissions to timetable student tab
        self.ui.bt_show_timetable_teacher.setChecked(checked)
        # self.ui.bt_save_timetable_teacher.setChecked(checked)
        # self.ui.bt_export_timetable_teacher.setChecked(checked)

    def handle_checkbox_change(self):
        # Get the state of the checkbox that triggered the change event
        checkbox_state = self.ui.SelectedAll.isChecked()

        if checkbox_state:
            # If the checkbox is checked, set all checkboxes to True
            self.set_all_checkboxes(True)
        else:
            # If the checkbox is unchecked, set all checkboxes to False
            self.set_all_checkboxes(False)
