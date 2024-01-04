import peewee
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem

from GUI.Dialogs.InitializingTheProject.CreateDataBaseDialog import CreateDataBaseDialog
from GUI.Dialogs.InitializingTheProject.TermSessionsInit import TermSessionsInit
from GUI.Dialogs.InitializingTheProject.classesDialog import ClassesDialog
from GUI.Dialogs.PeriodDialog import PeriodDialog
from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonInitClassRoomWidget
from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
from models.School import School


class TermSessionInitializeUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.lastInsertedSchoolId = 0

    def use_ui_elements(self):
        self.ui.btnAddInilialTermSessions.clicked.connect(self.show_term_session_initialize)
        self.ui.btnAddNewClassroom.clicked.connect(self.add_new_classroom_time)
        # self.ui.btnAddPeriod.clicked.connect(self.show_period)

    # def show_period(self):
    #     period_dialog = PeriodDialog()
    #     period_dialog.exec_()

    def add_new_classroom_time(self):
        class_dialog = ClassesDialog()
        class_dialog.btnSaveClasses.show()
        class_dialog.btnCancelAddingClasses.show()
        if class_dialog.exec_() == QDialog.Accepted:
            try:
                lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                class_name, major_name = class_dialog.save_data()
                ClassRoom.insert({
                    ClassRoom.school_id: lastInsertedSchoolId,
                    ClassRoom.name: class_name,
                    ClassRoom.Name_major: major_name,

                }).execute()

                self.lastInsertedClassroomId = ClassRoom.select(peewee.fn.Max(ClassRoom.id)).scalar()
                classroom = [class_name, major_name]
                self.add_new_classroom_to_table_widget(self.lastInsertedClassroomId, classroom)
                QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")

            except ValueError as e:
                QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")

    def add_new_classroom_to_table_widget(self, class_id, classroom):
        try:
            operationsButtons = DeleteUpdateButtonInitClassRoomWidget(table_widget=self.ui.tblClassRoomData)

            current_row = self.ui.tblshifttime.rowCount()  # Get the current row index
            self.ui.tblClassRoomData.insertRow(current_row)  # Insert a new row at the current row index
            self.ui.tblClassRoomData.setItem(current_row, 0, QTableWidgetItem(str(class_id)))
            self.ui.tblClassRoomData.setItem(current_row, 1, QTableWidgetItem(classroom[0]))
            self.ui.tblClassRoomData.setItem(current_row, 2, QTableWidgetItem(classroom[1]))
            self.ui.tblClassRoomData.setCellWidget(current_row, 3, operationsButtons)
            self.ui.tblClassRoomData.setColumnWidth(current_row, 40)
            self.ui.tblClassRoomData.setRowHeight(current_row, 150)
            Common.style_table_widget(self.ui, self.ui.tblClassRoomData)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def show_term_session_initialize(self):
        term_sessions = TermSessionsInit()
        term_sessions.btnMoveTermSessions.hide()
        term_sessions.btnSkippingTermSessions.hide()
        term_sessions.btnCancel.show()
        term_sessions.use_ui_elements()

        def cancel_session_initialize():
            # print("hello")
            term_sessions.close()

        term_sessions.btnCancel.clicked.connect(cancel_session_initialize)
        term_sessions.exec_()
