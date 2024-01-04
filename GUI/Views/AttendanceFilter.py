import datetime
import locale

import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem, QCheckBox

from GUI.Views.CommonFunctionality import Common
from models.Attendance import AttendanceModel
from models.Members import Members
from models.Shifts import Shifts
from models.Teachers import Teachers
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionButton, QStyle, QTableWidgetItem, QApplication


class AttendanceFilter:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.lastInsertedShift = 0
        self.arrival_time = ''
        self.leaving_time = ''
        self.date = ''
        self.state = ''
        self.end_arrival_time = ''
        self.come_time = ''
        self.end_should_come_time = ''
        self.delay_time = ''
        self.item_text = ''

    def use_ui_elements(self):
        self.ui.tblAttendanceFiltering.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblAttendanceFiltering.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblAttendanceFiltering.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnShowAttendance.clicked.connect(self.show_filtered_attendance)

    def show_filtered_attendance(self):
        locale.setlocale(locale.LC_TIME, 'ar')
        attendance_date = self.ui.dateAttendance.date().toPyDate()
        attendance_date = attendance_date.strftime("%A %Y-%m-%d")
        self.lastInsertedShift = Shifts.select(peewee.fn.Max(Shifts.id)).scalar()
        shift = Shifts.get(Shifts.id == self.lastInsertedShift)
        self.end_should_come_time = datetime.datetime.strptime(shift.end_attendance,
                                                               "%H:%M").time()
        startTimeDefined = datetime.datetime.strptime(shift.attending_time, "%H:%M").strftime("%I:%M %p")
        end_time_defined = datetime.datetime.strptime(shift.start_leaving, "%H:%M").strftime("%I:%M %p")
        # delayTimeDefined = shift.delay_times.strftime("%I:%M %p")
        checkoutTimeDefined = datetime.datetime.strptime(shift.end_leaving, "%H:%M").strftime("%I:%M %p")
        endCheckoutTimeDefined = shift.end_leaving
        attendance_data = AttendanceModel.get_all_attendance(self.ui)
        self.ui.tblAttendanceFiltering.setRowCount(0)
        if attendance_data:
            for attendance in attendance_data:
                member = Members.get_by_id(attendance.member_id)
                user_name = member.fName + ' ' + member.lName
                teacher = Teachers.get_by_id(attendance.member_id)
                shift = Shifts.get_by_id(teacher.shift_id)
                shift_type = shift.name
                self.ui.qCheckBox = QCheckBox()
                self.ui.sCheckBox = QCheckBox()
                self.ui.aCheckBox = QCheckBox()
                self.ui.aCheckBox.setEnabled(False)

                self.ui.sCheckBox.setEnabled(False)
                self.ui.qCheckBox.setEnabled(False)
                if attendance.input_time.strftime("%A %Y-%m-%d") == attendance_date:
                    if attendance.punch == "وصول":
                        late_check = startTimeDefined + shift.time_allowed_for_late
                        if attendance.input_time.strftime("%I:%M %p") > late_check:
                            self.ui.qCheckBox.setChecked(True)
                        else:
                            self.ui.qCheckBox.setChecked(False)
                        self.arrival_time = attendance.input_time.strftime("%I:%M %p")
                        self.come_time = datetime.datetime.strptime(self.arrival_time, "%I:%M %p").time()
                        self.delay_time = datetime.datetime.combine(datetime.datetime.min,
                                                                    self.end_should_come_time) - datetime.datetime.combine(
                            datetime.datetime.min, self.come_time)
                        hours = self.delay_time.seconds // 3600
                        minutes = (self.delay_time.seconds // 60) % 60

                        self.item_text = f"{hours} س , {minutes} د"
                        self.state = "وصول"
                        self.date = attendance.input_time.strftime("%A %Y-%m-%d")
                    elif attendance.punch == "خروج":
                        self.state = "خروج"
                        if attendance.out_time.strftime("%I:%M %p") < end_time_defined:
                            self.ui.sCheckBox.setChecked(True)
                        else:
                            self.ui.qCheckBox.setChecked(False)
                        self.leaving_time = attendance.out_time.strftime("%I:%M %p")
                        self.date = attendance.out_time.strftime("%A %Y-%m-%d")
                    current_row = self.ui.tblAttendanceFiltering.rowCount()
                    self.ui.tblAttendanceFiltering.insertRow(current_row)
                    self.ui.tblAttendanceFiltering.setItem(current_row, 0, QTableWidgetItem(user_name))
                    self.ui.tblAttendanceFiltering.setItem(current_row, 1, QTableWidgetItem(str(self.arrival_time)))
                    self.ui.tblAttendanceFiltering.setItem(current_row, 2, QTableWidgetItem(str(self.leaving_time)))
                    self.ui.tblAttendanceFiltering.setItem(current_row, 3, QTableWidgetItem(self.item_text))
                    self.ui.tblAttendanceFiltering.setItem(current_row, 4, QTableWidgetItem(shift_type))
                    self.ui.tblAttendanceFiltering.setCellWidget(current_row, 5, self.ui.qCheckBox)
                    self.ui.tblAttendanceFiltering.setCellWidget(current_row, 6, self.ui.sCheckBox)
                    self.ui.tblAttendanceFiltering.setItem(current_row, 8, QTableWidgetItem(self.date))

                    Common.style_table_widget(self.ui, self.ui.tblAttendanceFiltering)
                else:
                    self.ui.aCheckBox.setChecked(True)
                    self.ui.aCheckBox.setEnabled(False)
                    self.ui.aCheckBox.setStyleSheet("QCheckBox { background-color: red; text-align: center; }")
                    current_row = self.ui.tblAttendanceFiltering.rowCount()
                    self.ui.tblAttendanceFiltering.insertRow(current_row)
                    self.ui.tblAttendanceFiltering.setItem(current_row, 0, QTableWidgetItem(user_name))
                    self.ui.tblAttendanceFiltering.setItem(current_row, 4, QTableWidgetItem(shift_type))
                    # self.ui.tblAttendanceFiltering.setCellWidget(current_row, 7, self.ui.aCheckBox)
                    self.ui.tblAttendanceFiltering.setItem(current_row, 8, QTableWidgetItem(self.date))

                    # Create the delegate and set it for the checkbox column
                    delegate = CheckBoxDelegate()
                    self.ui.tblAttendanceFiltering.setItemDelegateForColumn(7, delegate)
                    item = QTableWidgetItem()
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    item.setCheckState(Qt.Checked)
                    self.ui.tblAttendanceFiltering.setItem(current_row, 7, item)

                    Common.style_table_widget(self.ui, self.ui.tblAttendanceFiltering)


class CheckBoxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.column() == 7 or index.column() == 5:  # Assuming the checkbox is in column 7
            # Get the checkbox state
            value = index.data(Qt.CheckStateRole)
            if value is not None and value == Qt.Checked:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off

            # Create a QStyleOptionButton to draw the checkbox
            style = QApplication.style()
            checkbox_rect = style.subElementRect(QStyle.SE_CheckBoxIndicator, option, None)
            checkbox_rect.moveCenter(option.rect.center())
            checkbox_option = QStyleOptionButton()
            checkbox_option.rect = checkbox_rect
            checkbox_option.state = option.state

            # Draw the checkbox
            style.drawControl(QStyle.CE_CheckBox, checkbox_option, painter)
        else:
            # For other columns, delegate to the base class
            super().paint(painter, option, index)

