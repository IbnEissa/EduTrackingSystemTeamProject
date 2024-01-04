from datetime import datetime, timedelta
import pandas as pd
import peewee
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QMessageBox, QDialog, QFileDialog
from zk import ZK

from GUI.Dialogs.InitializingTheProject.ListOptions import OptionDialog
from GUI.Views.CommonFunctionality import Common
from GUI.Views.TeachersUI import TeachersUI
from models.Attendance import AttendanceModel
from models.Device import Device
from models.Members import Members
from models.Teachers import Teachers
from models.Shifts import Shifts


class Attendance(object):
    def __init__(self, user_id, timestamp, status, punch):
        self.user_id = user_id
        self.timestamp = timestamp
        self.status = status
        self.punch = punch
        self.last_inserted_device = 0


class AttendanceRetriever(object):
    def __init__(self, device_ip, device_port=4370):
        self.device_ip = device_ip
        self.device_port = device_port

    def retrieve_attendance_data(self):
        zk = ZK(ip='192.168.1.201', port=4370)
        conn = zk.connect()
        if conn:
            attendance_data = conn.get_attendance()
            conn.disconnect()
            return attendance_data
        else:
            print('Failed to connect to the device')
            return []


class AttendanceUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.search_thread = None
        self.search_thread2 = None
        self.attendance_time = ''
        self.ip = '192.168.1.201'
        self.port = 4370
        self.previous_stylesheet = self.ui.comboAddendenceTime.styleSheet()
        self.ui.checkFilterWithDays.stateChanged.connect(self.on_checkbox_days_state_changed)
        self.ui.checkFilterWithDate.stateChanged.connect(self.on_checkbox_date_state_changed)
        # self.ui.comboAddendenceTime.stateChanged.connect()
        self.data_yesterday = False
        self.data_today = False
        self.data_this_month = False
        self.data_previous_month = False
        self.data_between_dates = False
        Common.style_table_widget(self.ui, self.ui.tblLoadAttendence)
        self.last_inserted_device = 0
        self.device = 0
        self.dialog = OptionDialog()
        # teacher = TeachersUI(self.ui)
        # state, ip, port = teacher.connect_device()
        # if state:
        #     if ip is not None and port is not None:
        #         self.ip = ip
        #         self.port = port

    def use_ui_elements(self):
        self.ui.tblLoadAttendence.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblLoadAttendence.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblLoadAttendence.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.ui.btnLoadAttendence.clicked.connect(lambda: self.show_load_options('btnLoadAttendence'))
        self.ui.btnSaveAttendenceData.clicked.connect(lambda: self.show_export_options('btnSaveAttendenceData'))
        # self.ui.btnSaveAttendenceData.clicked.connect(self.add_attendance_to_database)
        Common.style_table_widget(self.ui, self.ui.tblLoadAttendence)

    def get_user_name(self, user_id):
        self.last_inserted_device = Device.select(peewee.fn.Max(Device.id)).scalar()
        # self.device = Device.get(Device.id == self.last_inserted_device)
        self.dialog = OptionDialog()
        zk = ZK(ip='192.168.1.201',port=4370, timeout=5)
        conn = zk.connect()
        if conn:
            conn.enable_device()
            users = conn.get_users()
            for user in users:
                if user.user_id == user_id:
                    return user.name

        return 'Unknown'

    def show_searching_widget(self):
        self.ui.layout.addWidget(self.ui.searching_widget)  # Show the searching widget

    def on_checkbox_days_state_changed(self, state):
        if state:
            self.execute_method_when_checked()
            self.ui.checkFilterWithDate.setChecked(False)
        else:
            self.execute_method_when_unchecked()
            self.ui.checkFilterWithDate.setChecked(True)

    def on_checkbox_date_state_changed(self, state):
        if state:
            self.the_state_of_check_date_is_true()
            self.ui.checkFilterWithDays.setChecked(False)
        else:
            self.the_state_of_check_date_is_false()
            self.ui.checkFilterWithDays.setChecked(True)

    def the_state_of_check_date_is_false(self):
        self.ui.dateFrom.setEnabled(False)
        self.ui.dateTo.setEnabled(False)
        self.ui.dateFrom.setStyleSheet("QDateEdit { background-color: #333333; color: #333333;}")
        self.ui.dateTo.setStyleSheet("QDateEdit {background-color: #333333; color: #333333;}")

    def the_state_of_check_date_is_true(self):
        self.ui.dateFrom.setEnabled(True)
        self.ui.dateTo.setEnabled(True)
        self.ui.dateFrom.setStyleSheet(
            "QDateEdit { background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); }")
        self.ui.dateTo.setStyleSheet(
            "QDateEdit {background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); }")

    def execute_method_when_checked(self):
        self.ui.comboAddendenceTime.setEnabled(True)
        self.ui.comboAddendenceTime.setStyleSheet(
            "QComboBox { background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); }")

    def execute_method_when_unchecked(self):
        self.ui.comboAddendenceTime.setEnabled(False)
        self.ui.comboAddendenceTime.setStyleSheet("QComboBox { background-color: #333333; color: #333333; }")

    def hide_searching_widget(self):
        self.ui.layout.removeWidget(self.ui.searching_widget)
        self.ui.searching_widget.hide()  # Hide the searching widget

    def add_attendance_to_database(self):
        self.last_inserted_device = Device.select(peewee.fn.Max(Device.id)).scalar()
        # self.device = Device.get(Device.id == self.last_inserted_device)

        try:
            if self.last_inserted_device != 0:
                if self.ui.tblLoadAttendence.rowCount() > 0:
                    for row in range(self.ui.tblLoadAttendence.rowCount()):
                        uid = self.ui.tblLoadAttendence.item(row, 0).text()
                        timestamp = self.ui.tblLoadAttendence.item(row, 2).text()
                        status = self.ui.tblLoadAttendence.item(row, 3).text()
                        punch = self.ui.tblLoadAttendence.item(row, 4).text()
                        AttendanceModel.insert({
                            AttendanceModel.member_id: uid,
                            AttendanceModel.device_number: self.last_inserted_device,
                            AttendanceModel.out_time: timestamp,
                            AttendanceModel.input_time: timestamp,
                            AttendanceModel.status: status,
                            AttendanceModel.punch: punch,
                        }).execute()
                    QMessageBox.information(self.ui, 'نجاح', 'تمت إضافة البيانات')
                else:
                    QMessageBox.warning(self.ui, 'خطأ', 'لايوجد بييانات لإضافتها')
            else:
                QMessageBox.warning(self.ui, 'تحذير', 'قم بإضافة جهاز بصمة')
        except Exception as e:
            error_message = "حدث خطأ\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def start_attendance_retrieval(self, type_of_search):
        if type_of_search == 'all':
            if not self.search_thread or not self.search_thread.isRunning():
                self.search_thread = AttendanceSearchThread(self.display_attendance_data)
                self.search_thread.start()
        elif type_of_search == 'with_date':
            if not self.search_thread2 or not self.search_thread2.isRunning():
                try:
                    self.search_thread2 = AttendanceSearchThread(self.get_date_attendance_from_dates)
                    self.search_thread2.start()
                except Exception as e:
                    error_message = "حدث خطأ\n" + str(e)
                    QMessageBox.critical(self.ui, "خطأ", error_message)

    def display_attendance_data(self, attendance_data):
        self.ui.tblLoadAttendence.clearContents()
        self.ui.tblLoadAttendence.setRowCount(0)
        if attendance_data:
            for index, attendance in enumerate(attendance_data):
                user_id = attendance.user_id
                status = attendance.status
                punch = str(attendance.punch)
                if punch == '0':
                    punch = 'وصول'
                elif punch == '1':
                    punch = 'خروج'
                if user_id.isdigit():
                    teacher = Teachers.get(Teachers.members_id == user_id)
                    member = Members.get(Members.id == teacher.members_id)
                    user_name = member.fName + ' ' + member.lName
                    timestamp = attendance.timestamp.strftime('%Y-%m-%d-%H:%M:%S')
                    current_row = self.ui.tblLoadAttendence.rowCount()
                    self.ui.tblLoadAttendence.insertRow(current_row)
                    self.ui.tblLoadAttendence.setItem(current_row, 0, QTableWidgetItem(str(user_id)))
                    self.ui.tblLoadAttendence.setItem(current_row, 1, QTableWidgetItem(user_name))
                    self.ui.tblLoadAttendence.setItem(current_row, 2, QTableWidgetItem(timestamp))
                    self.ui.tblLoadAttendence.setItem(current_row, 3, QTableWidgetItem(status))
                    self.ui.tblLoadAttendence.setItem(current_row, 4, QTableWidgetItem(str(punch)))
            Common.style_table_widget(self.ui, self.ui.tblLoadAttendence)

    def show_load_options(self, button_name):
        options = [
            ("من جهاز البصمة", "icons_rc/users_Details.svg"),
            ("من أكسل", "icons_rc/users_Details.svg"),
        ]
        self.show_options(options, button_name)

    def show_export_options(self, button_name):
        options = [
            ('إلى قاعدة البيانات', "icons_rc/users_Details.svg"),
            ('إلى أكسل', "icons_rc/users_Details.svg"),
        ]
        self.show_options(options, button_name)

    def show_options(self, options, button_name):
        if button_name == 'btnLoadAttendence':
            self.dialog.setOptions(options)
            btnLoadAttendence_pos = self.ui.btnLoadAttendence.pos()
            dialog_x = btnLoadAttendence_pos.x() - 200
            dialog_y = btnLoadAttendence_pos.y() + self.ui.btnLoadAttendence.height() + 130
            self.dialog.move(dialog_x, dialog_y)
            # self.dialog.move(1350, 500)
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_entry_tab(selected_option)
        elif button_name == 'btnSaveAttendenceData':
            self.dialog.setOptions(options)
            btnSaveAttendenceData_pos = self.ui.btnSaveAttendenceData.pos()
            dialog_x = btnSaveAttendenceData_pos.x() + 100
            dialog_y = btnSaveAttendenceData_pos.y() + self.ui.btnSaveAttendenceData.height() + 130
            self.dialog.move(dialog_x, dialog_y)
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_export_tab(selected_option)

    def show_entry_tab(self, selected_option):
        if selected_option == 'من جهاز البصمة':
            self.filter_methods()
        if selected_option == "من أكسل":
            self.get_data_from_excel()

    def get_data_from_excel(self):
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getOpenFileName(self.ui, "اختر ملف Excel", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            try:
                data_frame = pd.read_excel(file_name)
                num_rows, num_cols = data_frame.shape
                self.ui.tblLoadAttendence.setRowCount(num_rows)
                self.ui.tblLoadAttendence.setColumnCount(num_cols)

                for row in range(num_rows):
                    for col in range(num_cols):
                        cell_value = str(data_frame.iloc[row, col])
                        item = QTableWidgetItem(cell_value)
                        self.ui.tblLoadAttendence.setItem(row, col, item)
                QMessageBox.information(self.ui, "معلومة", "تم استيراد البيانات بنجاح")
            except Exception as e:
                QMessageBox.critical(self.ui, "خطأ", "حدث خطأ أثناء استيراد البيانات:" + str(e))

    def show_export_tab(self, selected_option):
        if selected_option == 'إلى قاعدة البيانات':
            self.add_attendance_to_database()
        if selected_option == 'إلى أكسل':
            self.export_data_to_excel()

    def export_data_to_excel(self):
        file_dialog = QFileDialog()
        file_name, _ = file_dialog.getSaveFileName(self.ui, "اختر ملف Excel", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            try:
                num_rows = self.ui.tblLoadAttendence.rowCount()
                num_cols = self.ui.tblLoadAttendence.columnCount()

                data = []
                for row in range(num_rows):
                    row_data = []
                    for col in range(num_cols):
                        item = self.ui.tblLoadAttendence.item(row, col)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append("")
                    data.append(row_data)

                columns = [f"Column {col + 1}" for col in range(num_cols)]
                df = pd.DataFrame(data, columns=columns)

                df.to_excel(file_name, index=False)
                QMessageBox.information(self.ui, "معلومة", "تم حفظ البيانات بنجاح في ملف Excel.ً")

            except Exception as e:
                QMessageBox.critical(self.ui, "خطأ", "حدث خطأ أثناء تصدير البيانات:" + str(e))

    def filter_methods(self):
        # if self.ui.checkFilterWithDays.isNotChecked():
        if self.ui.btnConnectDivice.text() == "الجهاز متصل":
            attendance_time = self.ui.comboAddendenceTime.currentText()
            if self.ui.checkFilterWithDays.isChecked():
                if attendance_time == 'اليوم':
                    # self.display_today_attendance()
                    QMessageBox.information(self.ui, "معلومة", "لايمكن تحميل الا الكل ً")
                elif attendance_time == 'الكل':
                    self.start_attendance_retrieval("all")
                elif attendance_time == 'امس':
                    QMessageBox.information(self.ui, "معلومة", "لايمكن تحميل الا الكل ً")
                    # self.start_attendance_yesterday()
                elif attendance_time == 'هذا الشهر':
                    QMessageBox.information(self.ui, "معلومة", "لايمكن تحميل الا الكل ً")
                    # self.show_month_attendance_data()
                elif attendance_time == 'الشهر الماضي':
                    QMessageBox.information(self.ui, "معلومة", "لايمكن تحميل الا الكل ً")
                    # self.show_previous_month_attendance_data()
            else:
                self.start_attendance_retrieval('with_date')
        else:
            QMessageBox.warning(self.ui, "تحذير", "الجهاز غير متصل حالياً")

    def get_date_attendance_from_dates(self, attendance_data):
        self.ui.tblLoadAttendence.clearContents()
        self.ui.tblLoadAttendence.setRowCount(0)
        date_from_str = self.ui.dateFrom.text()
        date_to_str = self.ui.dateTo.text()
        attendance_from_date = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        attendance_to_date = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        for index, attendance in enumerate(attendance_data):
            user_id = attendance.user_id
            status = attendance.status
            punch = str(attendance.punch)
            if punch == '0':
                punch = 'وصول'
            elif punch == '1':
                punch = 'خروج'
            if user_id.isdigit():
                teacher = Teachers.get(Teachers.members_id == user_id)
                member = Members.get(Members.id == teacher.members_id)
                user_name = member.fName + ' ' + member.lName
                timestamp = attendance.timestamp
                try:
                    if attendance_from_date <= timestamp.date() <= attendance_to_date:
                        self.data_between_dates = True
                        current_row = self.ui.tblLoadAttendence.rowCount()
                        self.ui.tblLoadAttendence.insertRow(current_row)
                        self.ui.tblLoadAttendence.setItem(current_row, 0, QTableWidgetItem(str(user_id)))
                        self.ui.tblLoadAttendence.setItem(current_row, 1, QTableWidgetItem(user_name))
                        self.ui.tblLoadAttendence.setItem(current_row, 2,
                                                          QTableWidgetItem(timestamp.strftime('%Y-%m-%d')))
                        self.ui.tblLoadAttendence.setItem(current_row, 3, QTableWidgetItem(status))
                        self.ui.tblLoadAttendence.setItem(current_row, 4, QTableWidgetItem(punch))
                    Common.style_table_widget(self.ui, self.ui.tblLoadAttendence)
                except Exception as e:
                    QMessageBox.critical(self.ui, "خطأ", str(e) + "لا يوجد بيانات حضور في هذا التاريخ ")

    def display_today_attendance(self):
        self.ui.tblLoadAttendence.clearContents()
        self.ui.tblLoadAttendence.setRowCount(0)
        attendance_time = self.ui.comboAddendenceTime.currentText()
        state, ip, port = Common.connect_device(self.ui)
        if state:
            attendance_retriever = AttendanceRetriever(ip)
            attendance_data = attendance_retriever.retrieve_attendance_data()
            today = datetime.today().strftime('%Y-%m-%d')
            self.array_of_ids = []
            if attendance_time == 'اليوم':
                for attendance in attendance_data:
                    user_id = attendance.user_id
                    timestamp = attendance.timestamp.strftime('%Y-%m-%d')
                    if timestamp == today:
                        self.array_of_ids.append(user_id)
                        self.data_today = True
                attendance_retriever2 = AttendanceRetriever(self.ip)
                attendance_data2 = attendance_retriever2.retrieve_attendance_data()
                for id in self.array_of_ids:
                    for data in attendance_data2:
                        if id == data.user_id:
                            user_id = id
                            status = data.status
                            punch = str(data.punch)
                            teacher = Teachers.get(Teachers.id == user_id)
                            member = Members.get(Members.id == teacher.members_id)
                            user_name = member.fName + '' + member.sName + '' + member.tName + ' ' + member.lName
                            timestamp = data.timestamp.strftime('%Y-%m-%d-%H:%M:%S')
                            current_row = self.ui.tblLoadAttendence.rowCount()
                            self.ui.tblLoadAttendence.insertRow(current_row)
                            self.ui.tblLoadAttendence.setItem(current_row, 0, QTableWidgetItem(str(user_id)))
                            self.ui.tblLoadAttendence.setItem(current_row, 1, QTableWidgetItem(user_name))
                            self.ui.tblLoadAttendence.setItem(current_row, 2, QTableWidgetItem(timestamp))
                            self.ui.tblLoadAttendence.setItem(current_row, 3, QTableWidgetItem(status))
                            self.ui.tblLoadAttendence.setItem(current_row, 4, QTableWidgetItem(punch))
            Common.style_table_widget(self.ui, self.ui.tblLoadAttendence)
            if not self.data_today:
                QMessageBox.critical(self.ui, "خطأ", "لا يوجد بيانات حضور اليوم ")

    def show_month_attendance_data(self):
        self.ui.tblLoadAttendence.clearContents()
        self.ui.tblLoadAttendence.setRowCount(0)
        attendance_time = self.ui.comboAddendenceTime.currentText()
        attendance_retriever = AttendanceRetriever(self.ip)
        attendance_data = attendance_retriever.retrieve_attendance_data()

        for attendance in attendance_data:
            user_id = attendance.user_id
            status = attendance.status
            punch = str(attendance.punch)
            teacher = Teachers.get(Teachers.id == user_id)
            member = Members.get(Members.id == teacher.members_id)
            user_name = member.fName + ' ' + member.sName + ' ' + member.tName + ' ' + member.lName
            timestamp = attendance.timestamp.strftime('%m')
            full_timestamp = attendance.timestamp.strftime('%Y-%m-%d')
            # today = datetime.monthname(datetime.today().month).today().strftime('%Y-%m-%d')
            today = str(datetime.today().month)
            # today = datetime.today().month
            if attendance_time == 'هذا الشهر':
                if timestamp == today:
                    self.data_month = True
                    current_row = self.ui.tblLoadAttendence.rowCount()
                    self.ui.tblLoadAttendence.insertRow(current_row)
                    self.ui.tblLoadAttendence.setItem(current_row, 0, QTableWidgetItem(str(user_id)))
                    self.ui.tblLoadAttendence.setItem(current_row, 1, QTableWidgetItem(user_name))
                    self.ui.tblLoadAttendence.setItem(current_row, 2, QTableWidgetItem(full_timestamp))
                    self.ui.tblLoadAttendence.setItem(current_row, 3, QTableWidgetItem(status))
                    self.ui.tblLoadAttendence.setItem(current_row, 4, QTableWidgetItem(punch))
        if not self.data_month:
            QMessageBox.critical(self.ui, "خطأ", "لا يوجد بيانات حضور في هذا الشهر ")

    def show_previous_month_attendance_data(self):
        attendance_time = self.ui.comboAddendenceTime.currentText()
        today = datetime.today()
        start_of_month = today.replace(day=1)
        end_of_previous_month = start_of_month - timedelta(days=1)
        start_of_previous_month = end_of_previous_month.replace(day=1)
        start_date_str = start_of_previous_month.strftime('%Y-%m-%d')
        end_date_str = end_of_previous_month.strftime('%Y-%m-%d')
        attendance_retriever = AttendanceRetriever(self.ip)
        attendance_data = attendance_retriever.retrieve_attendance_data()
        if attendance_data:
            for attendance in attendance_data:
                user_id = attendance.user_id
                status = attendance.status
                punch = str(attendance.punch)
                teacher = Teachers.get(Teachers.id == user_id)
                member = Members.get(Members.id == teacher.members_id)
                user_name = member.fName + ' ' + member.sName + ' ' + member.tName + ' ' + member.lName
                timestamp = attendance.timestamp.strftime('%m')
                full_timestamp = attendance.timestamp.strftime('%Y-%m-%d')
                if attendance_time == 'الشهر الماضي' and start_date_str <= full_timestamp <= end_date_str:
                    self.data_previous_month = True
                    current_row = self.ui.tblLoadAttendence.rowCount()
                    self.ui.tblLoadAttendence.insertRow(current_row)
                    self.ui.tblLoadAttendence.setItem(current_row, 0, QTableWidgetItem(str(user_id)))
                    self.ui.tblLoadAttendence.setItem(current_row, 1, QTableWidgetItem(user_name))
                    self.ui.tblLoadAttendence.setItem(current_row, 2, QTableWidgetItem(full_timestamp))
                    self.ui.tblLoadAttendence.setItem(current_row, 3, QTableWidgetItem(status))
                    self.ui.tblLoadAttendence.setItem(current_row, 4, QTableWidgetItem(punch))
        if not self.data_previous_month:
            QMessageBox.critical(self.ui, "خطأ", "لا يوجد بيانات حضور في الشهر الماضي ")


class AttendanceSearchThread(QThread):
    def __init__(self, callback, parent=None):
        super().__init__(parent)
        self.callback = callback
        self.ip = '192.168.1.201'
        self.port = 4370
        self.last_inserted_device = Device.select(peewee.fn.Max(Device.id)).scalar()
        # self.device = Device.get(Device.id == self.last_inserted_device)

    def run(self):
        attendance_retriever = AttendanceRetriever('192.168.1.201')
        attendance_data = attendance_retriever.retrieve_attendance_data()
        self.callback(attendance_data)
