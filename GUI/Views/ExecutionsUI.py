from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem

from GUI.Dialogs.ExecutionsDialog import ExecutionsDialog
from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonShiftsWidget
from GUI.Views.CommonFunctionality import Common
from models.AbsentExcuse import AbsentExcuse
from models.Members import Members
from models.Teachers import Teachers


class ExecutionsUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ui.tblExecutions.setColumnHidden(0, True)

    def use_ui_elements(self):
        self.ui.tblExecutions.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblExecutions.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblExecutions.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddExecution.clicked.connect(self.add_execution)
        # self.ui.txtSearchTeacherName.textChanged.connect(self.get_execution_data)

    def add_execution(self):
        Common.style_table_widget(self.ui, self.ui.tblExecutions)
        execution = ExecutionsDialog()
        if execution.exec_() == QDialog.Accepted:
            try:
                if execution.radioAllEmps.isChecked():
                    execution_type, absent_date, execution_reason = execution.save_data()
                    if execution_type == 'all':
                        for t in Teachers.select():
                            last_inserted_id = AbsentExcuse.insert({
                                AbsentExcuse.teacher_id: t.member_id,
                                AbsentExcuse.absent_date: absent_date,
                                AbsentExcuse.note: execution_reason
                            }).execute()
                            teacher = Members.get_by_id(t.member_id)
                            current_row = self.ui.tblExecutions.rowCount()
                            self.ui.tblExecutions.insertRow(current_row)
                            self.ui.tblExecutions.setItem(current_row, 0,
                                                          QTableWidgetItem(str(last_inserted_id)))
                            self.ui.tblExecutions.setItem(current_row, 1,
                                                          QTableWidgetItem(str(teacher.fName + ' ' + teacher.lName)))
                            self.ui.tblExecutions.setItem(current_row, 2, QTableWidgetItem(str(absent_date)))
                            self.ui.tblExecutions.setItem(current_row, 3, QTableWidgetItem(execution_reason))
                            operations_buttons = DeleteUpdateButtonShiftsWidget(table_widget=self.ui.tblExecutions)
                            self.ui.tblExecutions.setCellWidget(current_row, 4, operations_buttons)
                            self.ui.tblExecutions.setColumnWidth(current_row, 40)
                            self.ui.tblExecutions.setRowHeight(current_row, 100)
                            Common.style_table_widget(self.ui, self.ui.tblExecutions)
                    QMessageBox.information(self.ui, "نجاح", "تمت اضافة العذر لجميع الموظفين بنجاح")
                else:
                    execution_type, absent_date, teacher_id, teacher_name, execution_reason = execution.save_data()
                    last_inserted_id = AbsentExcuse.insert({
                        AbsentExcuse.teacher_id: teacher_id,
                        AbsentExcuse.absent_date: absent_date,
                        AbsentExcuse.note: execution_reason
                    }).execute()
                    teacher = Members.get_by_id(teacher_id)
                    current_row = self.ui.tblExecutions.rowCount()
                    self.ui.tblExecutions.insertRow(current_row)
                    self.ui.tblExecutions.setItem(current_row, 0,
                                                  QTableWidgetItem(str(last_inserted_id)))
                    self.ui.tblExecutions.setItem(current_row, 1,
                                                  QTableWidgetItem(str(teacher.fName + ' ' + teacher.lName)))
                    self.ui.tblExecutions.setItem(current_row, 2, QTableWidgetItem(str(absent_date)))
                    self.ui.tblExecutions.setItem(current_row, 3, QTableWidgetItem(execution_reason))
                    operations_buttons = DeleteUpdateButtonShiftsWidget(table_widget=self.ui.tblExecutions)
                    self.ui.tblExecutions.setCellWidget(current_row, 4, operations_buttons)
                    self.ui.tblExecutions.setColumnWidth(current_row, 40)
                    self.ui.tblExecutions.setRowHeight(current_row, 100)
                    Common.style_table_widget(self.ui, self.ui.tblExecutions)
                    QMessageBox.information(self.ui, "نجاح", "تمت اضافة العذر لجميع الموظفين بنجاح")
            except ValueError as e:
                QMessageBox.critical(self.ui, "خطأ", f"فشلت العملية  : {str(e)}")

    def show_in_table_widget(self, executions):
        self.ui.tblExecutions.setRowCount(0)
        for row, teacher in enumerate(AbsentExcuse.select()):
            self.ui.tblExecutions.insertRow(row)
            self.ui.tblExecutions.setItem(row, 0, QTableWidgetItem(str(teacher.id)))
            self.ui.tblExecutions.setItem(row, 1, QTableWidgetItem(str(teacher.teacher_id)))
            self.ui.tblExecutions.setItem(row, 2, QTableWidgetItem(str(teacher.absent_date)))
            self.ui.tblExecutions.setItem(row, 3, QTableWidgetItem(str(teacher.execution_reason)))
