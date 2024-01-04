from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget, QTableWidgetItem, \
    QAbstractItemView, QHeaderView, QDialog, QProgressBar, QLabel, QDialogButtonBox
from PyQt5.QtCore import QThread, pyqtSignal
from zk import ZK, const


class ProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.progress_bar = QProgressBar(self)
        self.progress_label = QLabel(self)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.progress_label)
        self.button_box = QDialogButtonBox(self)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel)
        layout.addWidget(self.button_box)
        self.button_box.rejected.connect(self.reject)

    def set_progress(self, value):
        self.progress_bar.setValue(int(value))

    def set_progress_label(self, text):
        self.progress_label.setText(text)


class AttendanceRetrievalThread(QThread):
    progress_updated = pyqtSignal(float)
    complete = pyqtSignal(list)

    def __init__(self, device_ip, device_port, parent=None):
        super().__init__(parent)
        self.device_ip = device_ip
        self.device_port = device_port

    def run(self):
        zk = ZK(self.device_ip, port=self.device_port, timeout=5)
        conn = zk.connect()
        if conn:
            attendances = conn.get_attendance()
            self.complete.emit(attendances)

    def update_progress(self, value):
        self.progress_updated.emit(value)


class AttendanceUI:
    def __init__(self, submain_instance):
        """
        Initializes the `AttendanceUI` class with the given `submain_instance`.
    
        Args:
            submain_instance: An instance of the `submain` class.
    
        Returns:
            None
        """
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.device_ip = '192.168.1.201'
        self.device_port = 4370
        self.progress_dialog = None
        self.attendance_retrieval_thread = None

    def use_ui_elements(self):
        """
        Configures the UI elements for attendance display.
    
        Returns:
            None
        """
        self.ui.tblAttendenceByHand.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblAttendenceByHand.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblAttendenceByHand.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.ui.addNewAttendence.clicked.connect(self.start_attendance_retrieval)
        self.ui.addNewAttendence.clicked.connect(self.check_face_recognition_enabled)

    def get_user_name(self, user_id):
        """
        Retrieves the user name for a given user ID.
    
        Args:
            user_id: The ID of the user.
    
        Returns:
            The name of the user, or 'Unknown' if the user ID is not found.
        """
        zk = ZK(self.device_ip, port=self.device_port, timeout=5)
        conn = zk.connect()
        if conn:
            conn.enable_device()
            users = conn.get_users()
            for user in users:
                if user.user_id == user_id:
                    return user.name
        return 'Unknown'

    def start_attendance_retrieval(self):
        """
        Starts the attendance retrieval process in a separate thread.

        Returns:
            None
        """
        self.progress_dialog = ProgressDialog(self.ui)
        self.progress_dialog.show()

        self.attendance_retrieval_thread = AttendanceRetrievalThread(self.device_ip, self.device_port)
        self.attendance_retrieval_thread.progress_updated.connect(self.update_progress_dialog)
        self.attendance_retrieval_thread.complete.connect(self.handle_attendance_retrieval_complete)
        self.attendance_retrieval_thread.start()

    def update_progress_dialog(self, value):
        """
        Updates the progress dialog with the given value.

        Args:
            value: The progress value.

        Returns:
            None
        """
        self.progress_dialog.set_progress(value)

    def handle_attendance_retrieval_complete(self, attendances):
        """
        Handles the completion of the attendance retrieval process.

        Args:
            attendances: The retrieved attendance data.

        Returns:
            None
        """
        self.progress_dialog.close()
        self.populate_attendance_table(attendances)

    def populate_attendance_table(self, attendances):
        """
        Populates the attendance table with the given attendance data.

        Args:
            attendances: The attendance data.

        Returns:
            None
        """
        self.ui.tblAttendenceByHand.clearContents()
        self.ui.tblAttendenceByHand.setRowCount(0)

        for index, atten in enumerate(attendances):
            user_id = atten.user_id
            timestamp = atten.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            status = atten.status
            punch = atten.punch
            user_name = self.get_user_name(user_id)
            current_row = self.ui.tblAttendenceByHand.rowCount()
            self.ui.tblAttendenceByHand.insertRow(current_row)
            self.ui.tblAttendenceByHand.setItem(current_row, 0, QTableWidgetItem(str(user_id)))
            self.ui.tblAttendenceByHand.setItem(current_row, 1, QTableWidgetItem(user_name))
            self.ui.tblAttendenceByHand.setItem(current_row, 2, QTableWidgetItem(timestamp))
            self.ui.tblAttendenceByHand.setItem(current_row, 3, QTableWidgetItem(status))
            self.ui.tblAttendenceByHand.setItem(current_row, 4, QTableWidgetItem(punch))

    # def add_user(self, user_id, user_name):
    #     zk = ZK(self.device_ip, port=self.device_port, timeout=5)
    #     conn = zk.connect()
    #     if conn:
    #         conn.enable_device()
    #         conn.get_face_fun_on()
    #         zk.captusers_cap = zk.users_cap + 1
    #         user.user_id = user_id
    #         user.name = user_name
    #         user.password = '1234'  # Set a default password
    #         user.privilege = const.USER_DEFAULT
    #         user.group_id = 1  # Set the user group ID
    #         return user.save()
    #     return False

    def check_face_recognition_enabled(self):

        zk = ZK(self.device_ip, port=self.device_port, timeout=5)
        conn = zk.connect()
        state = conn.get_face_fun_on()
        if conn:
            print(state)
            return conn.fingers_cap

        return False
