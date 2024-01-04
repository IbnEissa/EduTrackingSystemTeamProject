from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
from zk import ZK

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonSchoolWidget, DeleteUpdateButtonDeviceWidget, \
    DeleteUpdateButtonInitDeviceWidget, DeleteUpdateButtonInitClassRoomWidget
from models.School import School
from models.ClassRoom import ClassRoom
from models.Device import Device
from GUI.Views.CommonFunctionality import Common
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout, QToolButton
from GUI.Views.CommonFunctionality import Common


class ShowInitialData:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ui.tblSchoolData.setColumnHidden(0, True)
        # self.ui.tblDiveceData.setColumnHidden(0, True)
        self.ui.tblClassRoomData.setColumnHidden(0, True)
        self.get_school_data()
        self.get_device_data()
        self.get_classroom_data()
        # self.get_subjects_data()

    def use_ui_elements(self):
        self.ui.btnConnectDivice.clicked.connect(self.connect_default_device)
        self.ui.btn_delete_device.clicked.connect(self.delete_device)

    def delete_device(self):
        current_row = self.ui.tblDiveceData.currentRow()
        if current_row == 0:
            QMessageBox.warning(self.ui, "تحذير", "هذا الجهاز هو الجهاز الافتراضي ولا يمكن حذفه .")
        elif current_row > 0:
            device_id = self.ui.tblDiveceData.item(current_row, 0).text()
            device = Device.get(Device.id == device_id)
            device.delete_instance()
            self.get_device_data()
        elif current_row == -1:
            QMessageBox.warning(self.ui, "تحذير", "الرجاء تحديد الجهاز المراد حذفه .")

    def get_school_data(self):
        columns = ['id', 'school_name', 'city', 'directorate', 'village', 'academic_level', 'student_gender_type',
                   'created_at', 'updated_at']

        school_query = School.select()

        self.ui.tblSchoolData.setRowCount(0)  # Clear existing rows in the table
        for row, school_data in enumerate(school_query):
            table_items = []
            for column_name in columns:
                item_value = getattr(school_data, column_name)
                table_item = QTableWidgetItem(str(item_value))
                table_items.append(table_item)

            self.ui.tblSchoolData.insertRow(row)
            for col, item in enumerate(table_items):
                self.ui.tblSchoolData.setItem(row, col, item)

            self.ui.tblSchoolData.setColumnWidth(row, 40)
            self.ui.tblSchoolData.setRowHeight(row, 150)
            operations_buttons = DeleteUpdateButtonSchoolWidget(table_widget=self.ui.tblSchoolData)
            self.ui.tblSchoolData.setCellWidget(row, 9, operations_buttons)
            Common.style_table_widget(self.ui, self.ui.tblSchoolData)

    def disconnect_device(self):
        row = self.ui.tblDiveceData.currentRow()
        ip = self.ui.tblDiveceData.item(row, 2)
        port = self.ui.tblDiveceData.item(row, 3)
        print("the ip is : ", ip.text())
        print("the port is : ", port.text())

        zk = ZK(ip.text(), port=int(port.text()), timeout=5)
        result = zk.disconnect()

    # def get_device_data(self):
    #     columns = ['id', 'name', 'ip', 'port', 'status']
    #
    #     device_query = Device.select()
    #
    #     self.ui.tblDiveceData.setRowCount(0)  # Clear existing rows in the table
    #     for row, device_data in enumerate(device_query):
    #         table_items = []
    #         for column_name in columns:
    #             item_value = getattr(device_data, column_name)
    #             table_item = QTableWidgetItem(str(item_value))
    #             table_items.append(table_item)
    #
    #         self.ui.tblDiveceData.insertRow(row)
    #         for col, item in enumerate(table_items):
    #             self.ui.tblDiveceData.setItem(row, col, item)
    #
    #         self.ui.tblDiveceData.setColumnWidth(row, 40)
    #         self.ui.tblDiveceData.setRowHeight(row, 150)
    #         operations_buttons = DeleteUpdateButtonInitDeviceWidget(table_widget=self.ui.tblDiveceData)
    #         self.ui.tblDiveceData.setCellWidget(row, 5, operations_buttons)
    #         Common.style_table_widget(self.ui, self.ui.tblDiveceData)

    def get_device_data(self):
        columns = ['id', 'name', 'ip', 'port', 'status']

        device_query = Device.select()

        self.ui.tblDiveceData.setRowCount(0)
        for row, device_data in enumerate(device_query):
            table_items = []
            for column_name in columns:
                item_value = getattr(device_data, column_name)
                table_item = QTableWidgetItem(str(item_value))
                table_items.append(table_item)

            self.ui.tblDiveceData.insertRow(row)
            for col, item in enumerate(table_items):
                self.ui.tblDiveceData.setItem(row, col, item)

            self.ui.tblDiveceData.setColumnWidth(row, 40)
            self.ui.tblDiveceData.setRowHeight(row, 80)
            operations_buttons = ConnectionButtonDeviceInitWidget(table_widget=self.ui.tblDiveceData)
            self.ui.tblDiveceData.setCellWidget(row, 5, operations_buttons)
            Common.style_table_widget(self.ui, self.ui.tblDiveceData)

    def get_classroom_data(self):
        columns = ['id', 'name', 'Name_major']

        classroom_query = ClassRoom.select()

        self.ui.tblClassRoomData.setRowCount(0)  # Clear existing rows in the table
        for row, classroom_data in enumerate(classroom_query):
            table_items = []
            for column_name in columns:
                item_value = getattr(classroom_data, column_name)
                table_item = QTableWidgetItem(str(item_value))
                table_items.append(table_item)

            self.ui.tblClassRoomData.insertRow(row)
            for col, item in enumerate(table_items):
                self.ui.tblClassRoomData.setItem(row, col, item)

            self.ui.tblClassRoomData.setColumnWidth(row, 40)
            self.ui.tblClassRoomData.setRowHeight(row, 150)
            operations_buttons = DeleteUpdateButtonInitClassRoomWidget(table_widget=self.ui.tblClassRoomData)
            self.ui.tblClassRoomData.setCellWidget(row, 3, operations_buttons)
            Common.style_table_widget(self.ui, self.ui.tblClassRoomData)

    def connect_default_device(self):
        ip = ''
        port = ''
        current_row = self.ui.tblDiveceData.currentRow()
        if current_row > -1:
            ip = self.ui.tblDiveceData.item(current_row, 2)
            port = self.ui.tblDiveceData.item(current_row, 3)
        else:
            ip = self.ui.tblDiveceData.item(0, 2)
            port = self.ui.tblDiveceData.item(0, 3)
        connection_buttons = ConnectionButtonDeviceInitWidget(table_widget=self.ui.tblDiveceData)
        clicked_button = connection_buttons.connect_button
        try:

            zk = ZK(ip.text(), port=int(port.text()), timeout=3)
            if zk.is_connect:
                QMessageBox.warning(self.ui, "تحذير", "الجهاز متصل فعلاً11")
            else:
                try:
                    conn = zk.connect()
                    if clicked_button:
                        if clicked_button.text() == "توصيل":
                            try:
                                if conn:
                                    connection_buttons.switch_disconnected_design_button(clicked_button, 0)
                            except Exception as e:
                                QMessageBox.warning(self.ui, "تحذير", str(e) + "فشل الاتصال")
                                Common.style_table_widget(self.ui, self.ui.tblDiveceData)
                        elif clicked_button.text() == "تعطيل":
                            if conn.is_connect:
                                try:
                                    conn.disable_device()
                                    conn.disconnect()
                                    connection_state = conn.is_enabled
                                    if connection_state is not True:
                                        connection_buttons.switch_to_connected_design(clicked_button, 0)
                                except Exception as e:
                                    connection_buttons.switch_to_connected_design(clicked_button, 0, e)
                                    conn.disable_device()
                            else:
                                QMessageBox.warning(self.ui, "تحذير", "الجهاز غير متصل فعلاً")
                except Exception as e:
                    QMessageBox.warning(self.ui, 'خطأ', "لا يوجد جهاز بصمة متصل")
        except Exception as e:
            QMessageBox.warning(self.ui, 'خطأ', "لا يوجد جهاز بصمة متصل")


class ConnectionButtonDeviceInitWidget(QWidget):
    def __init__(self, table_widget=None, parent=None):
        super().__init__(parent)
        self.table_widget = table_widget
        layout = QVBoxLayout()
        self.connect_button = QPushButton("توصيل")
        self.connect_button.setFixedSize(110, 40)
        icon = QIcon("icons_rc/play.png")
        self.connect_button.setStyleSheet(
            "QPushButton { background-color: none; color:white;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        # self.connect_button.setStyleSheet(
        #     "color: white; background-color: red; font: 12pt 'Motken K Sina'; text-align: left; padding-left: 20px;")
        self.connect_button.setLayoutDirection(Qt.LeftToRight)
        self.connect_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.connect_button.setIcon(icon)
        layout.addSpacing(3)
        layout.addWidget(self.connect_button)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.connect_button.clicked.connect(self.on_connection_button_clicked)
        self.status = ''

    def on_connection_button_clicked(self):
        ip_address_item = ''
        port_number_item = ''
        clicked_button = self.sender()
        row = 0
        cell_widget = clicked_button.parentWidget()
        if cell_widget and self.table_widget:
            row = self.table_widget.indexAt(cell_widget.pos()).row()
            ip_address_item = self.table_widget.item(row, 2)
            port_number_item = self.table_widget.item(row, 3)
        zk = ZK(ip_address_item.text(), port=int(port_number_item.text()), timeout=5)
        if zk.is_connect:
            QMessageBox.warning(self, "تحذير", "الجهاز متصل فعلاً11")
        else:
            try:
                conn = zk.connect()
                if clicked_button:
                    if clicked_button.text() == "توصيل":
                        try:
                            if conn:
                                self.status = 'متصل الان'
                                self.switch_disconnected_design_button(clicked_button, row)
                        except Exception as e:
                            QMessageBox.warning(self, "تحذير", str(e) + "فشل الاتصال")
                            Common.style_table_widget(self, self.table_widget)
                    elif clicked_button.text() == "تعطيل":
                        if conn.is_connect:
                            try:
                                conn.disable_device()
                                conn.disconnect()
                                print("the is_connect3  is : ", conn.is_connect)
                                connection_state = conn.is_enabled
                                if connection_state is not True:
                                    self.switch_to_connected_design(clicked_button, row)
                            except Exception as e:
                                self.switch_to_connected_design(clicked_button, row, e)
                                conn.disable_device()
                        else:
                            QMessageBox.warning(self, "تحذير", "الجهاز غير متصل فعلاً")
            except Exception as e:
                QMessageBox.warning(self, "تحذير", str(e) + "الجهاز غير متصل ")

    def switch_disconnected_design_button(self, QPushButton, row):
        self.table_widget.setItem(row, 4, QTableWidgetItem('متصل الان'))
        QPushButton.setText("تعطيل")
        QPushButton.setStyleSheet(
            "QPushButton { background-color: none; color:white;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        icon = QIcon("icons_rc/stop-button.png")
        QPushButton.setIcon(icon)
        QMessageBox.information(self, "نجاح", "نجح الاتصال")
        Common.style_table_widget(self, self.table_widget)

    def switch_to_connected_design(self, QPushButton, row, e=None):
        QPushButton.setText("توصيل")
        self.table_widget.setItem(row, 4, QTableWidgetItem('غير متصل'))
        icon = QIcon("icons_rc/play.png")
        QPushButton.setStyleSheet(
            "QPushButton { background-color: none; color:white;font: 75 12pt 'Motken K Sina'; border-radius: 10%; } QPushButton:hover{ background-color:none; color:rgb(255, 255, 255); font: 75 10pt 'Motken K Sina'; }")
        QPushButton.setIcon(icon)
        if e is not None:
            QMessageBox.warning(self, "تحذير", str(e) + "تم قطع الاتصال")
        else:
            QMessageBox.information(self, "نجاح", "تم قطع الاتصال")
        Common.style_table_widget(self, self.table_widget)
