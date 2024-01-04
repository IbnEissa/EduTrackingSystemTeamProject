import sys
import peewee
from PyQt5.QtCore import QPoint, QTimer, QDateTime, Qt
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from zk import ZK
import mysql.connector
from GUI.Dialogs.InitializingTheProject.CreateDataBaseDialog import CreateDataBaseDialog
from GUI.Dialogs.InitializingTheProject.ListOptions import OptionUI, OptionDialog
from GUI.Dialogs.InitializingTheProject.SchoolDialog import SchoolDialog
from GUI.Dialogs.InitializingTheProject.TermSessionsInit import TermSessionsInit
from GUI.Dialogs.InitializingTheProject.showInitializeData import ShowInitialData
from GUI.Dialogs.RejesterTeacherFingerDialog import RejesterTeacherFingerDialog
from GUI.Dialogs.UserDialog import UserDialog
from GUI.Dialogs.UserLoginDialog import UserLoginDialog
from GUI.Dialogs.UserLogoutDialog import UserLogoutDialog
from GUI.Views.AttendanceFilter import AttendanceFilter
from GUI.Views.AttendanceUI import AttendanceUI
from GUI.Views.CommonFunctionality import Common
from GUI.Views.ConnectWithPreviousDatabaseUI import ConnectWithPreviousDatabaseUI
from GUI.Views.CouncilFathersUI import CouncilFathersUI
from GUI.Views.DeviceUI import DeviceUI
from GUI.Views.ExecutionsUI import ExecutionsUI
from GUI.Views.PermissionUI import PermissionUI
from GUI.Views.Student_class_scheduleUI import Student_class_scheduleUI
from GUI.Views.Student_reportUI import Student_reportUI
from GUI.Views.StudentsUI import StudentsUI
from GUI.Views.Teacher_class_scheduleUI import Teacher_class_scheduleUI
from GUI.Views.Teacher_reportUI import Teacher_reportUI
from GUI.Views.TeachersUI import TeachersUI
from GUI.Views.TermSessionInitializeUI import TermSessionInitializeUI
from GUI.Views.UsersUI import UsersUI
from GUI.Views.backupUI import Backup_UI
from GUI.Views.shiftsUI import Shift_timeUI
from GUI.Views.uihandler import UIHandler
from GUI.Views.PersonBasicDataUI import SubMain
from models.Device import Device
from models.Permissions import Permissions
from models.School import School
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from models.Users import Users


class Main:
    def __init__(self, state):
        self.state = state
        self.initialization = 'False'
        # self.login_state = login_state
        # self.window = None
        self.dialog = OptionDialog()

        self.main_design = 'EduTracMain.ui'
        self.ui_handler = UIHandler(self.main_design)
        self.window = SubMain(self.ui_handler)
        self.app = QApplication([])
        self.system_date_timer = QTimer()
        self.device_timer = QTimer()
        # self.device_timer.timeout.connect(self.find_the_device_connected)
        self.system_date_timer.timeout.connect(self.update_system_date_label)
        self.system_date_timer.start(1000)
        self.device_timer.start(10000)
        self.window.ui.btnExit.clicked.connect(lambda:
                                               self.close_application('موافق', 'إلغاء', 'تحذبر',
                                                                      'هل تريد حقاَ الخروج من النظام ؟', 'app'))
        # self.window.ui.btnRefresh.clicked.connect(self.find_the_device_connected)
        # self.window.ui.btnConnectDivice.clicked.connect(self.connect_device)

    def close_application(self, ok_button_text, cancel_button_text, message_title, message_context, parent_type):
        Users.update_all_states_to_false()
        message_box = QMessageBox()
        message_box.setStyleSheet("QMessageBox { background-color: white; color: black; }")
        ok_button = QPushButton()
        ok_button.setText(ok_button_text)
        cancel_button = QPushButton()
        cancel_button.setText(cancel_button_text)
        message_box.addButton(ok_button, QMessageBox.AcceptRole)
        message_box.addButton(cancel_button, QMessageBox.RejectRole)
        message_box.setWindowTitle(message_title)
        message_box.setText(message_context)
        message_box.setIcon(QMessageBox.Warning)
        message_box.exec_()
        clicked_button = message_box.clickedButton()
        if parent_type == 'app':
            if clicked_button == ok_button:
                self.app.quit()
            elif clicked_button == cancel_button:
                return
        elif parent_type == 'dialog':
            if clicked_button == ok_button:
                RejesterTeacherFingerDialog.exec_()
            elif clicked_button == cancel_button:
                return

    def update_system_date_label(self):
        current_datetime = QDateTime.currentDateTime()
        formatted_datetime = current_datetime.toString("dd/MM/yyyy")
        formatted_time = current_datetime.toString("hh:mm:ss A")
        # formatted_day = current_datetime.toString("I dd")
        self.window.ui.lblCurrentSystemDateAndTime.setText(
            formatted_datetime + "     " + formatted_time)
        # self.window.ui.lblCurrentSystemDateAndTime.setStyleSheet("font-family:Shorooq_N1.ttf;")

    def close_dialog(self):
        print("the school is clicked ")
        if self.dialog.exec_() == QDialog.Accepted:
            self.dialog.reject()

    def main(self):
        if self.state == 1:
            self.method_1()
        # elif self.state == 1:
        #     self.method_1()

        else:
            print("Invalid state value")

    # def create_database(self):
    #     create_data_base = CreateDataBaseDialog()
    #     create_data_base.use_ui_elements()
    #     create_data_base.exec_()

    def initialize(self):
        print("hello in initialize system ")
        QMessageBox.information(self.window.ui, 'اشعار', 'مرحبا بك في تهيئة النظام ')

        school = SchoolDialog()
        school.use_ui_elements()
        school.exec_()

        self.method_1()

    def show_options_user_details(self, btn_name):
        options = [
            ("الحساب", "icons_rc/users.png"),
            ("تبديل المستخدم", "icons_rc/log-out.svg"),
            ("خروج نهائي", "icons_rc/log-out.svg"),
        ]
        self.show_options(options, btn_name)

    def show_options(self, options, btn_name):
        if btn_name == 'btnUserDetails':
            self.dialog.setOptions(options)
            self.dialog.move(50, 100)
            if self.dialog.exec_() == QDialog.Accepted:
                selected_option = self.dialog.selectedOption()
                self.show_user_details_tab(selected_option)

    def show_user_details_tab(self, selected_option):

        if selected_option == 'تبديل المستخدم':
            # self.app.quit()
            user_logout = UserLogoutDialog()
            user_logout.exec_()
        if selected_option == 'خروج نهائي':
            self.app.quit()

        if selected_option == 'الحساب':
            QMessageBox.information(self.window.ui, 'تحذير', 'لم يتم اضافة الواجهه بعد')

    def method_1(self):

        user_login = UserLoginDialog()
        user_login.use_ui_elements()
        # user_login.exec_()
        if user_login.exec_() == QDialog.Accepted:
            result, username = user_login.login()

            # Check if the login was successful
            if result is True and username is not None:
                # Get the user with the given ID
                user = Users.get_or_none(Users.id == 1)

                if user is not None:
                    admin_user_name = user.userName

                    # Check if the username matches
                    if username == admin_user_name:
                        self.main_window()
                    else:
                        # try:
                        if username != admin_user_name:
                            school_data = School.select(peewee.fn.Max(School.id)).scalar()
                            if school_data:
                                self.make_school_name()
                            else:
                                self.initialize()

    def make_school_name(self):
        lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
        id = lastInsertedSchoolId
        school = School.get_by_id(id)
        self.window.ui.btnSchoolName.setText(" مدرسة  " + school.school_name + "  النموذجية ")
        # self.window.ui.btnSchoolName12.setVisible(False)
        self.main_window()

    def main_window(self):
        self.window.ui.comboAddendenceTime.setEnabled(False)
        self.window.ui.comboAddendenceTime.setStyleSheet("QComboBox { background-color: #333333; color: #333333; }")
        self.window.ui.checkFilterWithDate.setChecked(True)
        ShowInitialData(self.window)
        init_data = ShowInitialData(self.window)
        init_data.use_ui_elements()
        Device = DeviceUI(self.window)
        Device.use_ui_elements()
        Teacher = TeachersUI(self.window)
        Teacher.use_ui_elements()
        options = OptionUI(self.window)
        options.use_ui_elements()
        self.window.ui.btnUserDetails.clicked.connect(lambda: self.show_options_user_details('btnUserDetails'))
        attendance = AttendanceUI(self.window)
        attendance.use_ui_elements()
        shift = Shift_timeUI(self.window)
        shift.shift_ui_elements()
        common = Common(self.window)
        common.use_ui_elements()
        students = StudentsUI(self.window)
        students.use_ui_elements()
        permission = PermissionUI(self.window)
        permission.permission_ui_elements()
        council_fathers = CouncilFathersUI(self.window)
        council_fathers.use_ui_elements()
        user = UsersUI(self.window)
        user.use_ui_elements()
        student_reports = Student_reportUI(self.window)
        student_reports.use_ui_elements()
        teacher_reports = Teacher_reportUI(self.window)
        teacher_reports.use_ui_elements()
        student_class_schedule = Student_class_scheduleUI(self.window)
        student_class_schedule.use_ui_elements()
        teacher_class_schedule = Teacher_class_scheduleUI(self.window)
        teacher_class_schedule.use_ui_elements()
        term_session_initialize = TermSessionInitializeUI(self.window)
        term_session_initialize.use_ui_elements()
        backup = Backup_UI(self.window)
        backup.use_ui_elements()
        attendanceFilter = AttendanceFilter(self.window)
        attendanceFilter.use_ui_elements()
        execution = ExecutionsUI(self.window)
        execution.use_ui_elements()
        connect_with_previous_database = ConnectWithPreviousDatabaseUI(self.window)
        connect_with_previous_database.use_ui_elements()
        self.window.ui.setWindowFlags(
            self.window.ui.windowFlags() | Qt.FramelessWindowHint)
        self.window.ui.showMaximized()
        # self.window.ui.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
        )
        if connection.is_connected():
            # QMessageBox.information(None, "نجاح", "تم الاتصال بنجاح بقاعدة البيانات MySQL!")
            cursor = connection.cursor()
            # Execute SQL query to retrieve the list of databases
            cursor.execute("SHOW DATABASES")
            # Fetch all the database names
            databases = [row[0] for row in cursor.fetchall()]
            # print(databases)
            # Fetch database_name from the text file
            with open("database_name.txt", "r") as file:
                database_name = file.read().strip()

            # Check if the specified database exists in the list
            if database_name in databases:
                # QMessageBox.information(None, "نجاح", f"Database '{database_name}' exists in MySQL.")
                state_value = 1
                main = Main(state_value)
                main.main()

            elif database_name.strip() == "":
                create_data_base = CreateDataBaseDialog()
                create_data_base.use_ui_elements()
                create_data_base.exec_()
                state_value = 1
                main = Main(state_value)
                main.main()

    except mysql.connector.Error as e:
        QMessageBox.information(None, "فشل", "فشل الاتصال بقاعدة البيانات MySQL.")
