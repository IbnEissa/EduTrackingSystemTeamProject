import locale
import peewee
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem
from zk import ZK

# !/usr/bin/env python2
# # -*- coding: utf-8 -*-
import sys
import traceback
import argparse
import time
import datetime
import codecs
from builtins import input

from GUI.Dialogs.RejesterTeacherFingerDialog import RejesterTeacherFingerDialog
from models.fingerPrintData import FingerPrintData

# sys.path.append("zk")

from zk import ZK, const
from zk.user import User
from zk.finger import Finger
from zk.attendance import Attendance
from zk.exception import ZKErrorResponse, ZKNetworkError

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeachersWidget, chickedButton, unchickedButton
# from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeachersWidget
from GUI.Dialogs.TeacherDialog import TeacherDialog
from GUI.Views.CommonFunctionality import Common
from GUI.Views.DeviceUI import DeviceUI
from models.Device import Device
from models.Members import Members
from models.School import School
from models.Teachers import Teachers
from models.Shifts import Shifts


class TeachersUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ip = ''
        self.port = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedTeacherId = 0
        self.teacher_name = ''
        self.finger_button_state = True
        self.deviceState = False
        self.ui.tblTeachers.setColumnHidden(2, True)
        self.ui.tblTeachers.setColumnHidden(12, True)
        self.ui.tblTeachers.setColumnHidden(13, True)
        self.ui.tblTeachers.setColumnHidden(0, True)
        self.ui.tblTeachers.setColumnHidden(7, True)
        self.ui.tblTeachers.setColumnHidden(8, True)
        self.ui.tblTeachers.setColumnHidden(5, True)
        locale.setlocale(locale.LC_TIME, 'ar')
        self.teacher_uid = 0
        self.teacher_user_id = 0

    def use_ui_elements(self):
        self.ui.tblTeachers.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblTeachers.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblTeachers.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnRegesterTeacherFinger.clicked.connect(self.rejester_finger)
        self.ui.btnAddNewTeacher.clicked.connect(self.add_new_teacher_data)
        self.ui.txtTeachersSearch.textChanged.connect(self.search_by_name)
        self.ui.btnRefresh_teachers.clicked.connect(self.refresh_teacher_data)
        self.ui.btnLoadFingersData.clicked.connect(self.load_fingers_to_db)

    def search_by_name(self):
        search_item = self.ui.txtTeachersSearch.text().lower()
        self.ui.tblTeachers.setRowCount(0)  # Clear existing rows in the table
        Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
        members_data = Members.select().where(peewee.fn.LOWER(Members.fName).contains(search_item))
        for member in members_data:
            teacher = Teachers.get_or_none(member_id=member.id)
            if teacher:
                shift_id = teacher.shift_id
                shift_name = Shifts.get_by_id(shift_id)
                has_fingers_data = FingerPrintData.get_teacher_fingers(self.ui, teacher.member_id)
                row = self.ui.tblTeachers.rowCount()
                self.ui.tblTeachers.insertRow(row)
                self.ui.tblTeachers.setItem(row, 0, QTableWidgetItem(str(member.id)))
                self.ui.tblTeachers.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
                self.ui.tblTeachers.setItem(row, 3, QTableWidgetItem(str(member.gender)))
                self.ui.tblTeachers.setItem(row, 4, QTableWidgetItem(str(teacher.cities)))
                self.ui.tblTeachers.setItem(row, 5, QTableWidgetItem(str(member.dateBerth)))
                self.ui.tblTeachers.setItem(row, 6, QTableWidgetItem(str(member.phone)))
                self.ui.tblTeachers.setItem(row, 7, QTableWidgetItem(teacher.qualification))
                self.ui.tblTeachers.setItem(row, 8, QTableWidgetItem(str(teacher.date_qualification)))
                self.ui.tblTeachers.setItem(row, 9, QTableWidgetItem(str(shift_name.name)))
                self.ui.tblTeachers.setItem(row, 10, QTableWidgetItem(str(teacher.major)))
                self.ui.tblTeachers.setItem(row, 11, QTableWidgetItem(str(member.type)))
                self.ui.tblTeachers.setItem(row, 12, QTableWidgetItem(str(teacher.exceperiance_years)))
                self.ui.tblTeachers.setItem(row, 13, QTableWidgetItem(teacher.state))
                self.ui.tblTeachers.setCellWidget(row, 15, DeleteUpdateButtonTeachersWidget(
                    table_widget=self.ui.tblTeachers).get_buttons('Old'))
                if has_fingers_data is not True:
                    no_finger = unchickedButton(table_widget=self.ui.tblTeachers)
                    self.ui.tblTeachers.setCellWidget(row, 14, no_finger)
                    Common.style_table_widget(self.ui, self.ui.tblTeachers)
                elif has_fingers_data is True:
                    finger = chickedButton(table_widget=self.ui.tblTeachers)
                    self.ui.tblTeachers.setCellWidget(row, 14, finger)
                    Common.style_table_widget(self.ui, self.ui.tblTeachers)
                self.ui.tblTeachers.setColumnWidth(row, 60)
                self.ui.tblTeachers.setRowHeight(row, 150)

    def connect_device(self):
        rowsCount = self.ui.tblDiveceData.rowCount()
        for row in range(rowsCount):
            state = self.ui.tblDiveceData.item(row, 4)
            ip = self.ui.tblDiveceData.item(row, 2)
            port = self.ui.tblDiveceData.item(row, 3)
            if state.text() == 'متصل الان':
                device_state = True
                device_ip = ip.text()
                device_port = port.text()
                return device_state, device_ip, device_port
            else:
                device_state = False
                device_ip = None
                device_port = None
                return device_state, device_ip, device_port

    def rejester_finger(self):
        # self.load_fingers_data()
        row = self.ui.tblTeachers.currentRow()
        state, ip, port = self.connect_device()
        if row > -1:
            if state:
                if ip is not None and port is not None:
                    user_id = self.ui.tblTeachers.item(row, 0)
                    user_name = self.ui.tblTeachers.item(row, 1)
                    try:
                        zk = ZK(ip=ip, port=int(port), timeout=5)
                        conn = zk.connect()
                        users = conn.get_users()
                        user_password = None
                        exists_user = False
                        for user in users:
                            if user.uid == int(user_id.text()):
                                exists_user = True
                                user_password = user.password
                        if exists_user:
                            rejester_fingers = RejesterTeacherFingerDialog(int(user_id.text()))
                            rejester_fingers.find_user_temp(int(user_id.text()), user_password, user_name)
                        else:
                            no_user = RejesterTeacherFingerDialog(int(user_id.text()))
                            label_styles = {
                                0: no_user.label_0,
                                1: no_user.label_1,
                                2: no_user.label_2,
                                3: no_user.label_3,
                                4: no_user.label_4,
                                5: no_user.label_5,
                                6: no_user.label_6,
                                7: no_user.label_7,
                                8: no_user.label_8,
                                9: no_user.label_9
                            }
                            for i in range(10):
                                label_styles[i].setVisible(False)
                            try:
                                conn.set_user(uid=int(user_id.text()),
                                              user_id=str(user_id.text()),
                                              name=user_name.text())
                                no_user.find_user_temp(int(user_id.text()), user_password, user_name)
                            except ZKErrorResponse as e:
                                QMessageBox.warning(self.ui, "تحذير", str(e) + "تم قطع الاتصال")
                    except ZKErrorResponse as e:
                        QMessageBox.warning(self.ui, "تحذير", str(e) + "تم قطع الاتصال")
            else:
                QMessageBox.warning(self.ui, 'خطأ', 'يجب الاتصال بالجهاز اولاً')

        else:
            QMessageBox.warning(self.ui, 'خطأ', 'يجب تحديد صف اولاً')

    # except Exception as e:
    # QMessageBox.warning(self.ui, "تحذير", str(e) + "هناك خطأ")
    # rejester_teacher_finger = RejesterTeacherFingerDialog()
    # rejester_teacher_finger.exec_()
    def refresh_teacher_data(self):
        self.ui.tblTeachers.setRowCount(0)
        teachers_data = Teachers.select()
        for teacher in teachers_data:
            member = Members.get_by_id(teacher.member_id)
            teacher = Teachers.get_by_id(teacher.member_id)
            shift = Shifts.get_by_id(teacher.shift_id)
            has_fingers_data = FingerPrintData.get_teacher_fingers(self.ui, member.id)
            row = self.ui.tblTeachers.rowCount()
            self.ui.tblTeachers.insertRow(row)
            self.ui.tblTeachers.setItem(row, 0, QTableWidgetItem(str(member.id)))
            self.ui.tblTeachers.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
            self.ui.tblTeachers.setItem(row, 3, QTableWidgetItem(str(member.gender)))
            self.ui.tblTeachers.setItem(row, 4, QTableWidgetItem(str(teacher.cities)))
            self.ui.tblTeachers.setItem(row, 5, QTableWidgetItem(str(member.dateBerth)))
            self.ui.tblTeachers.setItem(row, 6, QTableWidgetItem(str(member.phone)))
            self.ui.tblTeachers.setItem(row, 7, QTableWidgetItem(teacher.qualification))
            self.ui.tblTeachers.setItem(row, 8, QTableWidgetItem(str(teacher.date_qualification)))
            self.ui.tblTeachers.setItem(row, 9, QTableWidgetItem(str(shift.name)))
            self.ui.tblTeachers.setItem(row, 10, QTableWidgetItem(str(teacher.major)))
            self.ui.tblTeachers.setItem(row, 11, QTableWidgetItem(str(member.type)))
            self.ui.tblTeachers.setItem(row, 12, QTableWidgetItem(str(teacher.exceperiance_years)))
            self.ui.tblTeachers.setItem(row, 13, QTableWidgetItem(teacher.state))
            self.ui.tblTeachers.setCellWidget(row, 15, DeleteUpdateButtonTeachersWidget(
                table_widget=self.ui.tblTeachers).get_buttons('Old'))
            if has_fingers_data is not True:
                no_finger = unchickedButton(table_widget=self.ui.tblTeachers)
                self.ui.tblTeachers.setCellWidget(row, 14, no_finger)
                Common.style_table_widget(self.ui, self.ui.tblTeachers)
            elif has_fingers_data is True:
                finger = chickedButton(table_widget=self.ui.tblTeachers)
                self.ui.tblTeachers.setCellWidget(row, 14, finger)
                Common.style_table_widget(self.ui, self.ui.tblTeachers)
            self.ui.tblTeachers.setColumnWidth(row, 60)
            self.ui.tblTeachers.setRowHeight(row, 150)

    # self.load_fingerprints_data()
    # def refresh_teacher_data(self):
    #     self.ui.tblTeachers.setRowCount(0)
    #     teachers_data = Teachers.select()
    #     #     rows = len(teachers_data)
    #     #     self.ui.tblTeachers.setRowCount(rows)  # Set the total number of rows at once
    #     for row, teacher in enumerate(teachers_data):
    #         member = Members.get_by_id(teacher.member_id)
    #         shift = Shifts.get_by_id(teacher.shift_id)
    #         new_instance = DeleteUpdateButtonTeachersWidget(table_widget=self.ui.tblTeachers)
    #         row = self.ui.tblTeachers.rowCount()
    #         self.ui.tblTeachers.insertRow(row)
    #         self.ui.tblTeachers.setItem(row, 0, QTableWidgetItem(str(member.id)))
    #         self.ui.tblTeachers.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
    #         self.ui.tblTeachers.setItem(row, 3, QTableWidgetItem(str(teacher.gender)))
    #         self.ui.tblTeachers.setItem(row, 4, QTableWidgetItem(str(teacher.cities)))
    #         self.ui.tblTeachers.setItem(row, 5, QTableWidgetItem(str(member.dateBerth)))
    #         self.ui.tblTeachers.setItem(row, 6, QTableWidgetItem(str(member.phone)))
    #         self.ui.tblTeachers.setItem(row, 7, QTableWidgetItem(teacher.qualification))
    #         self.ui.tblTeachers.setItem(row, 8, QTableWidgetItem(str(teacher.date_qualification)))
    #         self.ui.tblTeachers.setItem(row, 9, QTableWidgetItem(str(shift.name)))
    #         self.ui.tblTeachers.setItem(row, 10, QTableWidgetItem(str(teacher.major)))
    #         self.ui.tblTeachers.setItem(row, 11, QTableWidgetItem(str(teacher.task)))
    #         self.ui.tblTeachers.setItem(row, 12, QTableWidgetItem(str(teacher.exceperiance_years)))
    #         self.ui.tblTeachers.setItem(row, 13, QTableWidgetItem(teacher.state))
    #         self.ui.tblTeachers.setCellWidget(row, 15, new_instance)
    #         self.ui.tblTeachers.setColumnWidth(row, 60)
    #         self.ui.tblTeachers.setRowHeight(row, 150)
    #         print ("the finger state is : ", teacher.fingerPrintData)
    #         if teacher.fingerPrintData == ' ':
    #             self.ui.tblTeachers.setCellWidget(row, 14, new_instance.get_buttons('NoFinger'))
    #             Common.style_table_widget(self.ui, self.ui.tblTeachers)
    #         else:
    #             self.ui.tblTeachers.setCellWidget(row, 14, new_instance.get_buttons('Finger'))
    #             Common.style_table_widget(self.ui, self.ui.tblTeachers)

    def load_templates_data(self, teacher_uid, ip, port):
        zk = ZK(ip, port=port, timeout=5)
        conn = zk.connect()
        temps = conn.get_templates()
        for temp in temps:
            if temp.uid == teacher_uid:
                return temp.fid
            else:
                return None

    def get_connected_device(self, teacher_name, lastInsertedTeacherId):

        rows = self.ui.tblDiveceData.rowCount()
        for row in range(rows):
            state = self.ui.tblDiveceData.item(row, 4).text()
            ip = self.ui.tblDiveceData.item(row, 2).text()
            port = self.ui.tblDiveceData.item(row, 3).text()
            if state is not None:
                if state == "متصل الان":
                    zk = ZK(ip, port=int(port), timeout=5)
                    conn = zk.connect()
                    users = conn.get_users()
                    lastInsertedTeacherId = lastInsertedTeacherId
                    if users:
                        for user in users:
                            if user.user_id == lastInsertedTeacherId:
                                result = self.load_templates_data(self, teacher_uid=lastInsertedTeacherId, ip=ip,
                                                                  port=port)
                                if result is not None:
                                    print("the temps fid is : ", result)
                                else:
                                    print("there is no temp fid for this emp please add his template")
                            else:
                                conn.set_user(uid=int(lastInsertedTeacherId), user_id=str(lastInsertedTeacherId),
                                              name=teacher_name)
                                print(" please add his template")

    def load_fingers_tos_db(self):
        try:
            state, ip, port = self.connect_device()
            if state:
                if ip is not None and port is not None:
                    zk = ZK(ip=ip, port=int(port), timeout=5)
                    try:
                        conn = zk.connect()
                        temps = conn.get_templates()
                        finger_not_added = []
                        temps_uids = []
                        if temps:
                            for temp in temps:
                                temps_uids.append(temp.uid)
                                fingers_data_exists = FingerPrintData.get_teacher_fingers(self.ui, temp.uid)
                                if fingers_data_exists is False:
                                    print("true is returned ")
                                    finger_not_added.append(temp.uid)
                                    if finger_not_added:
                                        fids = []
                                        for finger in finger_not_added:
                                            for i in range(10):
                                                user_temps = conn.get_user_template(uid=finger, temp_id=i,
                                                                                    user_id=finger)
                                                if user_temps is not None:
                                                    fids.append(i)
                                                else:
                                                    fids.append('')
                                            FingerPrintData.insert({
                                                FingerPrintData.teacher_id: finger,
                                                FingerPrintData.card_id: 'card_number',
                                                FingerPrintData.password: 'password',
                                                FingerPrintData.f0: fids[0],
                                                FingerPrintData.f1: fids[1],
                                                FingerPrintData.f2: fids[2],
                                                FingerPrintData.f3: fids[3],
                                                FingerPrintData.f4: fids[4],
                                                FingerPrintData.f5: fids[5],
                                                FingerPrintData.f6: fids[6],
                                                FingerPrintData.f7: fids[7],
                                                FingerPrintData.f8: fids[8],
                                                FingerPrintData.f9: fids[9],
                                            }).execute()
                                # print("finger_not_added", finger_not_added)
                                elif fingers_data_exists == 'First':
                                    print(" First is returned ")
                                    fids = []
                                    for i in range(10):
                                        user_temps = conn.get_user_template(uid=temp.uid, temp_id=i,
                                                                            user_id=temp.uid)
                                        if user_temps is not None:
                                            fids.append(i)
                                        else:
                                            fids.append('')
                                    FingerPrintData.insert({
                                        FingerPrintData.teacher_id: temp.uid,
                                        FingerPrintData.card_id: 0,
                                        FingerPrintData.password: 'password',
                                        FingerPrintData.f0: fids[0],
                                        FingerPrintData.f1: fids[1],
                                        FingerPrintData.f2: fids[2],
                                        FingerPrintData.f3: fids[3],
                                        FingerPrintData.f4: fids[4],
                                        FingerPrintData.f5: fids[5],
                                        FingerPrintData.f6: fids[6],
                                        FingerPrintData.f7: fids[7],
                                        FingerPrintData.f8: fids[8],
                                        FingerPrintData.f9: fids[9],
                                    }).execute()
                                else:
                                    print("false is returned ")
                            # print(finger_not_added)
                            # fids = []
                            # for i in range(10):
                            #     user_temps = conn.get_user_template(uid=finger_not_added, temp_id=i,
                            #                                         user_id=finger_not_added)
                            #     if user_temps is not None:
                            #         fids.append(i)
                            #     else:
                            #         fids.append('')
                            # print(fids)

                        # password = ''
                        # card_number = ''
                        # for temp in temps:
                        #     has_fingers_data = FingerPrintData.get_teacher_fingers(self.ui, temp.uid)
                        #     if has_fingers_data is not True:
                        #         for i in range(10):
                        #             temps = conn.get_user_template(uid=temp.uid, temp_id=i, user_id=temp.uid)
                        #             if temps:
                        #                 fids.append(temps.fid)
                        #             else:
                        #                 fids.append('')
                        #         print(fids)
                        # users = conn.get_users()
                        # for user in users:
                        #     if user.uid == temp.uid:
                        #         if user.password:
                        #             password = user.password
                        #         if user.card:
                        #             card_number = user.card
                        # FingerPrintData.insert({
                        #     FingerPrintData.teacher_id: temp.uid,
                        #     FingerPrintData.card_id: 'card_number',
                        #     FingerPrintData.password: 'password',
                        #     FingerPrintData.f0: fids[0],
                        #     FingerPrintData.f1: fids[1],
                        #     FingerPrintData.f2: fids[2],
                        #     FingerPrintData.f3: fids[3],
                        #     FingerPrintData.f4: fids[4],
                        #     FingerPrintData.f5: fids[5],
                        #     FingerPrintData.f6: fids[6],
                        #     FingerPrintData.f7: fids[7],
                        #     FingerPrintData.f8: fids[8],
                        #     FingerPrintData.f9: fids[9],
                        # }).execute()
                    except ZKErrorResponse as e:
                        QMessageBox.warning(self.ui, "تحذير", str(e) + "تم قطع الاتصال")
                else:
                    QMessageBox.warning(self.ui, 'خطأ', 'يجب الاتصال بالجهاز اولاً')
        except ZKErrorResponse as e:
            QMessageBox.warning(self.ui, "تحذير", str(e) + "تم قطع الاتصال")

    def load_fingers_to_db(self):
        try:
            state, ip, port = self.connect_device()
            if state:
                if ip is not None and port is not None:
                    zk = ZK(ip=ip, port=int(port), timeout=5)
                    try:
                        conn = zk.connect()
                        temps = conn.get_templates()
                        finger_not_added = []
                        temps_uids = []
                        if temps:
                            for temp in temps:
                                if temp.uid not in temps_uids:
                                    temps_uids.append(temp.uid)
                            if temps_uids is not None:
                                for temps_uid in temps_uids:
                                    fingers_data_exists = FingerPrintData.get_teacher_fingers(self.ui, temps_uid)
                                    if fingers_data_exists:
                                        temps_fid = []
                                        for i in range(10):
                                            user_temps = conn.get_user_template(uid=temps_uid, temp_id=i,
                                                                                user_id=temps_uid)
                                            if user_temps:
                                                if user_temps.size > 0:
                                                    temps_fid.append(user_temps.fid)
                                                else:
                                                    temps_fid.append('')
                                            else:
                                                temps_fid.append('')
                                        print("the temp number : " + str(temps_fid) + " for the user " + str(
                                            temps_uid))
                                        password = ''
                                        card_id = ''
                                        users = conn.get_users()
                                        for user in users:
                                            if user.uid == temps_uid:
                                                if user.password:
                                                    password = user.password
                                                if user.card:
                                                    card_id = user.card
                                        FingerPrintData.update({
                                            FingerPrintData.teacher_id: temps_uid,
                                            FingerPrintData.card_id: card_id,
                                            FingerPrintData.password: password,
                                            FingerPrintData.f0: temps_fid[0],
                                            FingerPrintData.f1: temps_fid[1],
                                            FingerPrintData.f2: temps_fid[2],
                                            FingerPrintData.f3: temps_fid[3],
                                            FingerPrintData.f4: temps_fid[4],
                                            FingerPrintData.f5: temps_fid[5],
                                            FingerPrintData.f6: temps_fid[6],
                                            FingerPrintData.f7: temps_fid[7],
                                            FingerPrintData.f8: temps_fid[8],
                                            FingerPrintData.f9: temps_fid[9],
                                        }).execute()
                                    elif not fingers_data_exists:
                                        temps_fid = []
                                        for i in range(10):
                                            user_temps = conn.get_user_template(uid=temps_uid, temp_id=i,
                                                                                user_id=temps_uid)
                                            if user_temps:
                                                if user_temps.size > 0:
                                                    temps_fid.append(user_temps.fid)
                                                else:
                                                    temps_fid.append('')
                                            else:
                                                temps_fid.append('')
                                        print(" 2 the temp number : " + str(temps_fid) + " for the user " + str(
                                            temps_uid))
                                        password = ''
                                        card_id = ''
                                        users = conn.get_users()
                                        for user in users:
                                            if user.uid == temps_uid:
                                                if user.password:
                                                    password = user.password
                                                if user.card:
                                                    card_id = user.card

                                        FingerPrintData.insert({
                                            FingerPrintData.teacher_id: temps_uid,
                                            FingerPrintData.card_id: card_id,
                                            FingerPrintData.password: password,
                                            FingerPrintData.f0: temps_fid[0],
                                            FingerPrintData.f1: temps_fid[1],
                                            FingerPrintData.f2: temps_fid[2],
                                            FingerPrintData.f3: temps_fid[3],
                                            FingerPrintData.f4: temps_fid[4],
                                            FingerPrintData.f5: temps_fid[5],
                                            FingerPrintData.f6: temps_fid[6],
                                            FingerPrintData.f7: temps_fid[7],
                                            FingerPrintData.f8: temps_fid[8],
                                            FingerPrintData.f9: temps_fid[9],
                                        }).execute()

                            # print("Users Who have temps are : ", temps_uids)
                            # if temps_uids:
                            #     for temp_uid in temps_uids:
                            #         fingers_data_exists = FingerPrintData.get_teacher_fingers(self.ui, temp_uid)
                            #         if fingers_data_exists:
                            #             fingers_data_exists = True
                            #         elif not fingers_data_exists:
                            #             fingers_data_exists = False
                            #         elif fingers_data_exists == 'First':
                            #             fingers_data_exists = 'First'
                            #
                            #         if fingers_data_exists:
                            #             temps_fid = []
                            #             print("true is returned ")
                            #             for i in range(10):
                            #                 user_temps = conn.get_user_template(uid=temp_uid, temp_id=i,
                            #                                                     user_id=temp_uid)
                            #                 if user_temps:
                            #                     if user_temps.size > 0:
                            #                         temps_fid.append(user_temps.fid)
                            #                     # else:
                            #                     #     temps_fid.append('')
                            #                 else:
                            #                     temps_fid.append('')
                            #             # print("the temp number : " + str(temps_fid) + " for the user " + str(
                            #             #         temp_uid))
                            #             # if user_temps is not None:
                            #             #     temps_fid.append(i)
                            #             # else:
                            #             #     temps_fid.append('')
                            #             FingerPrintData.update({
                            #                 FingerPrintData.teacher_id: temp_uid,
                            #                 FingerPrintData.card_id: 'card_number',
                            #                 FingerPrintData.password: 'password',
                            #                 FingerPrintData.f0: temps_fid[0],
                            #                 FingerPrintData.f1: temps_fid[1],
                            #                 FingerPrintData.f2: temps_fid[2],
                            #                 FingerPrintData.f3: temps_fid[3],
                            #                 FingerPrintData.f4: temps_fid[4],
                            #                 FingerPrintData.f5: temps_fid[5],
                            #                 FingerPrintData.f6: temps_fid[6],
                            #                 FingerPrintData.f7: temps_fid[7],
                            #                 FingerPrintData.f8: temps_fid[8],
                            #                 FingerPrintData.f9: temps_fid[9],
                            #             }).execute()
                            #         # print("finger_not_added", finger_not_added)
                            #         elif fingers_data_exists == 'First':
                            #             print(" First is returned ")
                            #
                            #         elif not fingers_data_exists:
                            #             temps_fid2 = []
                            #             print("false is returned ")
                            #             for i in range(10):
                            #                 user_temps = conn.get_user_template(uid=temp_uid, temp_id=i,
                            #                                                     user_id=temp_uid)
                            #                 if user_temps:
                            #                     if user_temps.size > 0:
                            #                         temps_fid2.append(user_temps.fid)
                            #                     # else:
                            #                     #     temps_fid2.append('')
                            #                 else:
                            #                     temps_fid2.append('')
                            #             FingerPrintData.insert({
                            #                 FingerPrintData.teacher_id: temp_uid,
                            #                 FingerPrintData.card_id: 'card_number',
                            #                 FingerPrintData.password: 'password',
                            #                 FingerPrintData.f0: temps_fid2[0],
                            #                 FingerPrintData.f1: temps_fid2[1],
                            #                 FingerPrintData.f2: temps_fid2[2],
                            #                 FingerPrintData.f3: temps_fid2[3],
                            #                 FingerPrintData.f4: temps_fid2[4],
                            #                 FingerPrintData.f5: temps_fid2[5],
                            #                 FingerPrintData.f6: temps_fid2[6],
                            #                 FingerPrintData.f7: temps_fid2[7],
                            #                 FingerPrintData.f8: temps_fid2[8],
                            #                 FingerPrintData.f9: temps_fid2[9],
                            #             }).execute()

                            #     fids = []
                            #     for i in range(10):
                            #         user_temps = conn.get_user_template(uid=temp_uid, temp_id=i,
                            #                                             user_id=temp_uid)
                            #         if user_temps is not None:
                            #             fids.append(i)
                            #         else:
                            #             fids.append('')
                            #     FingerPrintData.insert({
                            #         FingerPrintData.teacher_id: temp.uid,
                            #         FingerPrintData.card_id: 0,
                            #         FingerPrintData.password: 'password',
                            #         FingerPrintData.f0: fids[0],
                            #         FingerPrintData.f1: fids[1],
                            #         FingerPrintData.f2: fids[2],
                            #         FingerPrintData.f3: fids[3],
                            #         FingerPrintData.f4: fids[4],
                            #         FingerPrintData.f5: fids[5],
                            #         FingerPrintData.f6: fids[6],
                            #         FingerPrintData.f7: fids[7],
                            #         FingerPrintData.f8: fids[8],
                            #         FingerPrintData.f9: fids[9],
                            #     }).execute()
                            # else:
                            #     print("false is returned ")
                            # print(finger_not_added)
                            # fids = []
                            # for i in range(10):
                            #     user_temps = conn.get_user_template(uid=finger_not_added, temp_id=i,
                            #                                         user_id=finger_not_added)
                            #     if user_temps is not None:
                            #         fids.append(i)
                            #     else:
                            #         fids.append('')
                            # print(fids)

                        # password = ''
                        # card_number = ''
                        # for temp in temps:
                        #     has_fingers_data = FingerPrintData.get_teacher_fingers(self.ui, temp.uid)
                        #     if has_fingers_data is not True:
                        #         for i in range(10):
                        #             temps = conn.get_user_template(uid=temp.uid, temp_id=i, user_id=temp.uid)
                        #             if temps:
                        #                 fids.append(temps.fid)
                        #             else:
                        #                 fids.append('')
                        #         print(fids)
                        # users = conn.get_users()
                        # for user in users:
                        #     if user.uid == temp.uid:
                        #         if user.password:
                        #             password = user.password
                        #         if user.card:
                        #             card_number = user.card
                        # FingerPrintData.insert({
                        #     FingerPrintData.teacher_id: temp.uid,
                        #     FingerPrintData.card_id: 'card_number',
                        #     FingerPrintData.password: 'password',
                        #     FingerPrintData.f0: fids[0],
                        #     FingerPrintData.f1: fids[1],
                        #     FingerPrintData.f2: fids[2],
                        #     FingerPrintData.f3: fids[3],
                        #     FingerPrintData.f4: fids[4],
                        #     FingerPrintData.f5: fids[5],
                        #     FingerPrintData.f6: fids[6],
                        #     FingerPrintData.f7: fids[7],
                        #     FingerPrintData.f8: fids[8],
                        #     FingerPrintData.f9: fids[9],
                        # }).execute()
                    except ZKErrorResponse as e:
                        QMessageBox.warning(self.ui, "تحذير", str(e) + "تم قطع الاتصال")
                else:
                    QMessageBox.warning(self.ui, 'خطأ', 'يجب الاتصال بالجهاز اولاً')
        except ZKErrorResponse as e:
            QMessageBox.warning(self.ui, "تحذير", str(e) + "تم قطع الاتصال")

    def add_new_teacher_data(self):
        teacher_dialog = TeacherDialog()
        try:
            lastInsertedSchoolId = School.select(peewee.fn.Max(School.id)).scalar()
            if teacher_dialog.exec_() == QDialog.Accepted:
                FName, LName, Gender, Cities, DOB, Phone, Qualification, DOQualification, ShiftsType, Major, Task, ExceperianceYears, state = teacher_dialog.save_data()
                has_finger_print_data = ''
                teacher = [FName, LName, Gender, Cities, DOB, Phone, Qualification, DOQualification, ShiftsType,
                           Major, Task,
                           ExceperianceYears, state, has_finger_print_data]
                if ShiftsType:
                    self.teacher_name = teacher[0] + ' ' + teacher[1]
                    id = Shifts.get_shift_id_from_name(self.ui, ShiftsType)
                    lastInsertedMemberId = Members.insert({
                        Members.school_id: lastInsertedSchoolId,
                        Members.fName: FName,
                        Members.lName: LName,
                        Members.dateBerth: DOB,
                        Members.phone: Phone,
                        Members.type: Task,
                        Members.gender: Gender,
                    }).execute()
                    Teachers.insert({
                        Teachers.member_id: lastInsertedMemberId,
                        Teachers.shift_id: id,
                        Teachers.cities: Cities,
                        Teachers.major: Major,
                        Teachers.exceperiance_years: ExceperianceYears,
                        Teachers.qualification: Qualification,
                        Teachers.date_qualification: DOQualification,
                        Teachers.state: state,
                    }).execute()
                    self.add_new_teacher_to_table_widget(lastInsertedMemberId, teacher)
                    QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                    Common.style_table_widget(self.ui, self.ui.tblTeachers)
                else:
                    QMessageBox.warning(self.ui, "خطأ", "يجب تحديد نوع الدوام")
        except ValueError as e:
            QMessageBox.critical(self.ui, "خطأ", f" فشلت العملية  : {str(e)}")

    def add_new_teacher_to_table_widget(self, teacher_id, teacher):
        try:
            current_row = self.ui.tblTeachers.rowCount()
            self.ui.tblTeachers.insertRow(current_row)
            self.ui.tblTeachers.setItem(current_row, 0, QTableWidgetItem(str(teacher_id)))
            self.ui.tblTeachers.setItem(current_row, 1, QTableWidgetItem(teacher[0] + ' ' + teacher[1]))
            self.ui.tblTeachers.setItem(current_row, 2, QTableWidgetItem(teacher[1]))
            self.ui.tblTeachers.setItem(current_row, 3, QTableWidgetItem(teacher[2]))
            self.ui.tblTeachers.setItem(current_row, 4, QTableWidgetItem(teacher[3]))
            self.ui.tblTeachers.setItem(current_row, 5, QTableWidgetItem(str(teacher[4])))
            self.ui.tblTeachers.setItem(current_row, 6, QTableWidgetItem(teacher[5]))
            self.ui.tblTeachers.setItem(current_row, 7, QTableWidgetItem(teacher[6]))
            self.ui.tblTeachers.setItem(current_row, 8, QTableWidgetItem(str(teacher[7])))
            self.ui.tblTeachers.setItem(current_row, 9, QTableWidgetItem(teacher[8]))
            self.ui.tblTeachers.setItem(current_row, 10, QTableWidgetItem(teacher[9]))
            self.ui.tblTeachers.setItem(current_row, 11, QTableWidgetItem(teacher[10]))
            self.ui.tblTeachers.setItem(current_row, 12, QTableWidgetItem(teacher[11]))
            self.ui.tblTeachers.setItem(current_row, 13, QTableWidgetItem(teacher[12]))
            self.ui.tblTeachers.setCellWidget(current_row, 15, DeleteUpdateButtonTeachersWidget(
                table_widget=self.ui.tblTeachers).get_buttons('Old'))
            if teacher[13] == '':
                no_finger = unchickedButton(table_widget=self.ui.tblTeachers)
                self.ui.tblTeachers.setCellWidget(current_row, 14, no_finger)
                Common.style_table_widget(self.ui, self.ui.tblTeachers)
            else:
                finger = chickedButton(table_widget=self.ui.tblTeachers)
                self.ui.tblTeachers.setCellWidget(current_row, 14, finger)
                Common.style_table_widget(self.ui, self.ui.tblTeachers)
            self.ui.tblTeachers.setColumnWidth(current_row, 60)
            self.ui.tblTeachers.setRowHeight(current_row, 150)
        except Exception as e:
            error_message = "حدث خطأ:\n\n" + str(e)
            QMessageBox.critical(self.ui, "خطأ", error_message)
