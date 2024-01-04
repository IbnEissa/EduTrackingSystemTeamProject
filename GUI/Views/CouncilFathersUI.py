from datetime import datetime
import datetime
import logging
import peewee
from PyQt5.QtCore import QDate, Qt

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
# from zk import ZK

# from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonCouncilFathersWidget
from GUI.Dialogs.CouncilFathersDialog import CouncilFathersDialog
from GUI.Dialogs.InitializingTheProject.showInitializeData import ShowInitialData
from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonCouncilFathersWidget
from GUI.Views.CommonFunctionality import Common
from GUI.Views.DeviceUI import DeviceUI
from models.CouncilFathers import CouncilFathers
from models.Members import Members
# from models.BoardFathers import BoardFathers
from models.School import School


class CouncilFathersUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedCouncilFathersId = 0
        self.lastInsertedSchoolId = 0
        self.ui.tblCouncilFathers.setColumnHidden(0, True)
        self.ui.tblCouncilFathers.setColumnHidden(2, True)

    def use_ui_elements(self):
        self.ui.tblCouncilFathers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblCouncilFathers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblCouncilFathers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewCouncilFathers.clicked.connect(self.add_council_fathers_database)
        self.ui.txtCouncilFathersSearch.textChanged.connect(self.get_council_fathers_data)

    def add_council_fathers_database(self):
        # result = ShowInitialData.find_the_device_is_connected(self.ui)
        # if result is True:
        # self.ui.tblCouncilFathers.setRowCount(0)
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_save_fathers")
        if result_condition is True:
            CouncilFathers_dialog = CouncilFathersDialog()
            if CouncilFathers_dialog.exec_() == QDialog.Accepted:
                # try:
                lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
                CouncilFatherfName, CouncilLName, CouncilGender, CouncilPhone, CouncilDOB, CouncilSocialStatus, CouncilAddrress, CouncilOrgaincStatus = CouncilFathers_dialog.save_data()
                lastInsertedMemberId = Members.insert({
                    Members.school_id: lastInsertedSchoolId,
                    Members.fName: CouncilFatherfName,
                    Members.lName: CouncilLName,
                    Members.dateBerth: CouncilDOB,
                    Members.phone: CouncilPhone,
                    Members.type: "عضو مجلس الأباء",
                    Members.gender: CouncilGender,

                }).execute()
                # self.lastInsertedMemberId = Members.select(peewee.fn.Max(Members.id)).scalar()
                print("this foreign key", lastInsertedMemberId)
                CouncilFathers.insert({
                    CouncilFathers.members_id: lastInsertedMemberId,
                    CouncilFathers.social_status: CouncilSocialStatus,
                    CouncilFathers.address: CouncilAddrress,
                    CouncilFathers.organic_status: CouncilOrgaincStatus,
                }).execute()

                councilFathers = [CouncilFatherfName, CouncilLName, CouncilGender, CouncilPhone,
                                  CouncilDOB, CouncilSocialStatus, CouncilAddrress, CouncilOrgaincStatus]
                self.lastInsertedCouncilFathersId = CouncilFathers.select(
                    peewee.fn.Max(CouncilFathers.members_id)).scalar()
                self.add_new_council_fathers_to_table_widget(self.lastInsertedCouncilFathersId, councilFathers)
                QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                # except ValueError as e:
                #     QMessageBox.critical(self.ui, "خطأ", f"لم يتم الحفظ بنجاح: {str(e)}")
        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

    def add_new_council_fathers_to_table_widget(self, council_fathers_id, council_fathers):
        try:
            operations_buttons = DeleteUpdateButtonCouncilFathersWidget(table_widget=self.ui.tblCouncilFathers)
            current_row = self.ui.tblCouncilFathers.rowCount()
            self.ui.tblCouncilFathers.insertRow(current_row)
            self.ui.tblCouncilFathers.setItem(current_row, 0, QTableWidgetItem(str(council_fathers_id)))
            self.ui.tblCouncilFathers.setItem(current_row, 1,
                                              QTableWidgetItem(council_fathers[0] + ' ' + council_fathers[1]))
            self.ui.tblCouncilFathers.setItem(current_row, 2, QTableWidgetItem(council_fathers[1]))
            self.ui.tblCouncilFathers.setItem(current_row, 3, QTableWidgetItem(str(council_fathers[2])))
            self.ui.tblCouncilFathers.setItem(current_row, 4, QTableWidgetItem(str(council_fathers[3])))
            self.ui.tblCouncilFathers.setItem(current_row, 5, QTableWidgetItem(str(council_fathers[4])))
            self.ui.tblCouncilFathers.setItem(current_row, 6, QTableWidgetItem(council_fathers[5]))
            self.ui.tblCouncilFathers.setItem(current_row, 7, QTableWidgetItem(council_fathers[6]))
            self.ui.tblCouncilFathers.setItem(current_row, 8, QTableWidgetItem(council_fathers[7]))
            self.ui.tblCouncilFathers.setCellWidget(current_row, 9, operations_buttons)
            self.ui.tblCouncilFathers.setColumnWidth(current_row, 40)
            self.ui.tblCouncilFathers.setRowHeight(current_row, 150)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)

    def get_council_fathers_data(self):
        result_condition = Common.grant_permission_to_clicked_button(self.ui, permission="bt_search_fathers")
        if result_condition is True:
            self.ui.tblCouncilFathers.setRowCount(0)
            fathers_data = CouncilFathers.select()
            for father in fathers_data:
                operations_buttons = DeleteUpdateButtonCouncilFathersWidget(table_widget=self.ui.tblCouncilFathers)
                member = Members.get_by_id(father.members_id)
                father = CouncilFathers.get_by_id(father.members_id)
                row = self.ui.tblCouncilFathers.rowCount()
                self.ui.tblCouncilFathers.insertRow(row)
                self.ui.tblCouncilFathers.setItem(row, 0, QTableWidgetItem(str(member.id)))
                self.ui.tblCouncilFathers.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
                self.ui.tblCouncilFathers.setItem(row, 2, QTableWidgetItem(str(member.lName)))
                self.ui.tblCouncilFathers.setItem(row, 3, QTableWidgetItem(str(member.gender)))
                self.ui.tblCouncilFathers.setItem(row, 4, QTableWidgetItem(str(member.phone)))
                self.ui.tblCouncilFathers.setItem(row, 5, QTableWidgetItem(str(member.dateBerth)))
                self.ui.tblCouncilFathers.setItem(row, 6, QTableWidgetItem(str(father.social_status)))
                self.ui.tblCouncilFathers.setItem(row, 7, QTableWidgetItem(str(father.address)))
                self.ui.tblCouncilFathers.setItem(row, 8, QTableWidgetItem(str(father.organic_status)))
                self.ui.tblCouncilFathers.setColumnWidth(row, 40)
                self.ui.tblCouncilFathers.setRowHeight(row, 150)
                self.ui.tblCouncilFathers.setCellWidget(row, 9, operations_buttons)
                Common.style_table_widget(self.ui, self.ui.tblCouncilFathers)
        else:
            QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")
