import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout

from GUI.Dialogs.shift_timeDialog import Shift_timedialog
from PyQt5.QtCore import QTime, Qt

from models.Periods import Periods
from models.Shifts import Shifts
from GUI.Views.CommonFunctionality import Common
from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonShiftsWidget, DeleteUpdateButtonPeriodsWidget


class Shift_timeUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ui.tblshifttime.setColumnHidden(0, True)
        for num in range(6, 15):
            self.ui.tblshifttime.setColumnHidden(num, True)

    def shift_ui_elements(self):
        self.ui.tblshifttime.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblshifttime.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblshifttime.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewshift_time.clicked.connect(self.add_new_shift_time)
        self.ui.txtShiftSearch.textChanged.connect(self.get_shift_data)
        self.ui.btnShowPeriods.clicked.connect(self.get_period_data)

    def add_new_shift_time(self):
        self.ui.tblshifttime.setRowCount(0)
        for num in range(6, 15):
            self.ui.tblshifttime.setColumnHidden(num, True)

        for num in range(1, 7):
            self.ui.tblshifttime.setColumnHidden(num, False)

        shift_dialog = Shift_timedialog()
        if shift_dialog.exec_() == QDialog.Accepted:
            try:
                name, start_shift, end_shift = shift_dialog.save_data_shift()
                lastInsertedshifttime = Shifts.insert({
                    Shifts.name: name,
                    Shifts.start_date_shift: start_shift,
                    Shifts.end_date_shift: end_shift,

                }).execute()

                print("the last insert", lastInsertedshifttime)
                shift = Shifts.get_by_id(lastInsertedshifttime)
                creation_date = shift.created_at
                update_date = shift.updated_at
                print("created", creation_date)
                print("updated", update_date)
                shift = [lastInsertedshifttime, name, start_shift, end_shift, creation_date, update_date]

                self.add_new_shift_time_to_table_widget(shift)
                Common.style_table_widget(self.ui, self.ui.tblshifttime)

                QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
            except ValueError as e:
                QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")

    def add_new_shift_time_to_table_widget(self, shifts):
        self.ui.tblshifttime.setRowCount(0)
        try:
            operationsButtons = DeleteUpdateButtonShiftsWidget(table_widget=self.ui.tblshifttime)

            current_row = self.ui.tblshifttime.rowCount()  # Get the current row index
            self.ui.tblshifttime.insertRow(current_row)  # Insert a new row at the current row index
            self.ui.tblshifttime.setItem(current_row, 0, QTableWidgetItem(str(shifts[0])))
            self.ui.tblshifttime.setItem(current_row, 1, QTableWidgetItem(shifts[1]))
            self.ui.tblshifttime.setItem(current_row, 2, QTableWidgetItem(str(shifts[2])))
            self.ui.tblshifttime.setItem(current_row, 3, QTableWidgetItem(str(shifts[3])))
            self.ui.tblshifttime.setItem(current_row, 4, QTableWidgetItem(str(shifts[4])))
            self.ui.tblshifttime.setItem(current_row, 5, QTableWidgetItem(str(shifts[5])))
            self.ui.tblshifttime.setCellWidget(current_row, 6, operationsButtons)
            self.ui.tblshifttime.setColumnWidth(current_row, 40)
            self.ui.tblshifttime.setRowHeight(current_row, 150)
            Common.style_table_widget(self.ui, self.ui.tblshifttime)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def get_shift_data(self):
        for num in range(6, 15):
            self.ui.tblshifttime.setColumnHidden(num, True)

        for num in range(1, 7):
            self.ui.tblshifttime.setColumnHidden(num, False)

        try:
            columns = ['id', 'name', 'start_date_shift', 'end_date_shift', 'created_at', 'updated_at']

            search_item = self.ui.txtShiftSearch.toPlainText().lower()
            shift_query = Shifts.select().where(
                peewee.fn.LOWER(Shifts.name).contains(search_item)).distinct()
            self.ui.tblshifttime.setRowCount(0)  # Clear existing rows in the table
            for row, shift in enumerate(shift_query):
                table_items = []
                for column_name in columns:
                    try:
                        item_value = getattr(shift, column_name)
                    except AttributeError:
                        shift_data = Shifts.get(Shifts.id)
                        item_value = getattr(shift_data, column_name)

                    table_item = QTableWidgetItem(str(item_value))
                    table_items.append(table_item)

                self.ui.tblshifttime.insertRow(row)
                for col, item in enumerate(table_items):
                    self.ui.tblshifttime.setItem(row, col, item)

                self.ui.tblshifttime.setColumnWidth(row, 40)
                self.ui.tblshifttime.setRowHeight(row, 150)

                operations_buttons = DeleteUpdateButtonShiftsWidget(table_widget=self.ui.tblshifttime)
                self.ui.tblshifttime.setCellWidget(row, 6, operations_buttons)
                Common.style_table_widget(self.ui, self.ui.tblshifttime)


        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def get_period_data(self):
        self.ui.tblshifttime.setRowCount(0)  # Clear existing rows in the table
        for num in range(6, 15):
            self.ui.tblshifttime.setColumnHidden(num, False)
        self.ui.tblshifttime.setColumnHidden(1, False)

        for num in range(2, 8):
            self.ui.tblshifttime.setColumnHidden(num, True)

        periods = Periods.select()
        for period in periods:
            # shift = Shifts.get(Shifts.id == period.shift_id)
            shift_id = period.shift_id
            shift_name = Shifts.get_by_id(shift_id)
            row = self.ui.tblshifttime.rowCount()
            self.ui.tblshifttime.insertRow(row)
            attendance_time = QTableWidgetItem(period.attendance_time.strftime("%H:%M"))
            departure_time = QTableWidgetItem(period.departure_time.strftime("%H:%M"))
            self.ui.tblshifttime.setItem(row, 1, QTableWidgetItem(str(shift_name.name)))
            self.ui.tblshifttime.setItem(row, 7, QTableWidgetItem(str(period.id)))
            self.ui.tblshifttime.setItem(row, 8, QTableWidgetItem(str(period.name)))
            self.ui.tblshifttime.setItem(row, 9, attendance_time)
            self.ui.tblshifttime.setItem(row, 10, departure_time)
            self.ui.tblshifttime.setItem(row, 11, QTableWidgetItem(str(period.period_price)))
            self.ui.tblshifttime.setItem(row, 12, QTableWidgetItem(str(period.time_allowed_for_late)))
            self.ui.tblshifttime.setItem(row, 13, QTableWidgetItem(str(period.time_allowed_for_leaving)))
            self.ui.tblshifttime.setColumnWidth(row, 40)
            self.ui.tblshifttime.setRowHeight(row, 150)
            self.ui.tblshifttime.setCellWidget(row, 14,
                                               DeleteUpdateButtonPeriodsWidget(table_widget=self.ui.tblshifttime))
            Common.style_table_widget(self.ui, self.ui.tblshifttime)
