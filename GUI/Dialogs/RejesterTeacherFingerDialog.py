from itertools import count

from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QPushButton
from PyQt5.QtCore import Qt, QEvent
from PyQt5.uic import loadUi
from zk import ZK
from zk.finger import Finger
from zk.user import User
from zk.exception import ZKErrorResponse

from models.Members import Members
from models.Teachers import Teachers


class RejesterTeacherFingerDialog(QDialog):
    def __init__(self, selected_user, parent=None):
        super().__init__(parent)
        loadUi("RejesterTeacherFingerDialog2.ui", self)
        self.zk = None
        self.conn = None
        self.selected_user = selected_user
        self.selected_finger = None
        self.selected_btn_style = "QPushButton { background-color:rgb(202, 202, 0); color: rgb(255, 255, 255); border-radius: 10%; font: 75 14pt 'Motken K Sina'; }"
        self.finger_styles = {
            0: self.btnLeftHandFinger0,
            1: self.btnLeftHandFinger1,
            2: self.btnLeftHandFinger2,
            3: self.btnLeftHandFinger3,
            4: self.btnLeftHandFinger4,
            5: self.btnRightHandFinger5,
            6: self.btnRightHandFinger6,
            7: self.btnRightHandFinger7,
            8: self.btnRightHandFinger8,
            9: self.btnRightHandFinger9
        }
        self.label_styles = {
            0: self.label_0,
            1: self.label_1,
            2: self.label_2,
            3: self.label_3,
            4: self.label_4,
            5: self.label_5,
            6: self.label_6,
            7: self.label_7,
            8: self.label_8,
            9: self.label_9
        }
        self.fingers_check_boxes = {
            0: self.cbFinger0,
            1: self.cbFinger1,
            2: self.cbFinger2,
            3: self.cbFinger3,
            4: self.cbFinger4,
            5: self.cbFinger5,
            6: self.cbFinger6,
            7: self.cbFinger7,
            8: self.cbFinger8,
            9: self.cbFinger9
        }

        self.zk = ZK('192.168.1.201', port=4370, timeout=5)
        self.conn = self.zk.connect()
        self.default_style = "QPushButton {   background-color:rgb(208, 153, 131); color: rgb(255, 255, 255); border-radius: 10%; font: 75 14pt 'Motken K Sina'; }"
        self.finger_ready_style = "QPushButton { background-color: green; color: rgb(255, 255, 255); border-radius: 10%; font: 75 14pt 'Motken K Sina'; }"
        self.setup_ui()

    def setup_ui(self):
        self.btnLeftHandFinger0.clicked.connect(self.on_finger_button_clicked)
        self.btnLeftHandFinger1.clicked.connect(self.on_finger_button_clicked)
        self.btnLeftHandFinger2.clicked.connect(self.on_finger_button_clicked)
        self.btnLeftHandFinger3.clicked.connect(self.on_finger_button_clicked)
        self.btnLeftHandFinger4.clicked.connect(self.on_finger_button_clicked)
        self.btnRightHandFinger5.clicked.connect(self.on_finger_button_clicked)
        self.btnRightHandFinger6.clicked.connect(self.on_finger_button_clicked)
        self.btnRightHandFinger7.clicked.connect(self.on_finger_button_clicked)
        self.btnRightHandFinger8.clicked.connect(self.on_finger_button_clicked)
        self.btnRightHandFinger9.clicked.connect(self.on_finger_button_clicked)
        self.btnRejesterFinger.clicked.connect(self.start_enrollment)
        self.cbFinger0.stateChanged.connect(self.on_finger_checkbox_state_changed)
        self.cbFinger1.stateChanged.connect(self.on_finger_checkbox_state_changed)
        self.cbFinger2.stateChanged.connect(self.on_finger_checkbox_state_changed)
        self.cbFinger3.stateChanged.connect(self.on_finger_checkbox_state_changed)
        self.cbFinger4.stateChanged.connect(self.on_finger_checkbox_state_changed)
        self.cbFinger5.stateChanged.connect(self.on_finger_checkbox_state_changed)
        self.cbFinger6.stateChanged.connect(self.on_finger_checkbox_state_changed)
        self.cbFinger7.stateChanged.connect(self.on_finger_checkbox_state_changed)
        self.cbFinger8.stateChanged.connect(self.on_finger_checkbox_state_changed)
        self.cbFinger9.stateChanged.connect(self.on_finger_checkbox_state_changed)
        self.btnSaveTeacherTemplates.clicked.connect(self.reject)
        self.btnCancelRejesteringFingers.clicked.connect(self.reject)
        self.btnDeleteFingersData.clicked.connect(self.delete_fingers_data)
        # self.comboTeacherName.currentIndexChanged.connect(self.select_user)
        # self.load_users()

    def on_finger_button_clicked(self):
        sender = self.sender()
        finger = sender.text()
        if self.selected_finger == finger:
            self.selected_finger = None
            sender.setStyleSheet(self.default_style)
        else:
            self.selected_finger = finger
            sender.setStyleSheet(self.selected_btn_style)

        print("Selected finger ", self.selected_finger)

    def load_users(self):
        teacher_list = Teachers.select()
        for teacher in teacher_list:
            member = Members.get_by_id(teacher.member_id)
            self.comboTeacherName.addItem(member.fName + ' ' + member.lName)
            index = self.comboTeacherName.count() - 1
            self.comboTeacherName.setItemData(index, member.id, role=Qt.UserRole)

    def delete_fingers_data(self):
        try:
            conn = self.zk.connect()
            if conn:
                if self.selected_user is not None:
                    delete_user = conn.delete_user(uid=self.selected_user, user_id=str(self.selected_user))
                    add_user = conn.set_user(uid=self.selected_user, user_id=str(self.selected_user),
                                             name=self.lblUserName.text())
                    for i in range(len(self.fingers_check_boxes.items())):
                        self.label_styles[i].setVisible(False)
                        self.fingers_check_boxes[i].setVisible(True)
        except Exception as e:
            QMessageBox.critical(self, "خطأ", "لقد انتهى الوقت" + str(e))

    def verify_user(self):
        result = self.conn.verify_user()
        return result

    def enroll_user_fingers(self):
        if self.conn:
            try:
                if self.selected_finger is not None and self.selected_user is not None:
                    result = self.conn.enroll_user(uid=self.selected_user, user_id=str(self.selected_user),
                                                   temp_id=int(self.selected_finger))
                    cancel_c = self.conn.cancel_capture()
                    if cancel_c:
                        print("cnacel cap", cancel_c)
                    else:
                        print("cancel er cap ", cancel_c)
                    if result:
                        return int(self.selected_finger)
                    else:
                        return False
                else:
                    return False
            except Exception as e:
                return False

    def start_enrollment(self):
        if not self.selected_user:
            self.show_error_message(" قم بأختيار الاصبع أولاً")
        checked_fingers = []
        for i in range(len(self.fingers_check_boxes.items())):
            if self.fingers_check_boxes[i].isChecked():
                checked_fingers.append(i)
        if checked_fingers is not None:
            for i in checked_fingers:
                if not self.conn.is_enabled:
                    self.conn.enable_device()
                result = self.conn.enroll_user(uid=self.selected_user, user_id=str(self.selected_user),
                                               temp_id=i)
                if result:
                    self.change_style(i)
                else:
                    self.change_style(i)

    def change_style(self, i):
        self.label_styles[i].setVisible(True)
        self.fingers_check_boxes[i].setVisible(False)
        self.finger_styles[i].setStyleSheet(self.finger_ready_style)
        self.conn.test_voice(0)

    def reset_enrollment(self):
        self.selected_user = None
        self.selected_finger = None
        # self.update_ui()

    # def get_templates(self):
    #     try:
    #         conn = self.zk.connect()
    #         template = conn.get_user_template(uid=32, user_id=32, temp_id=6)
    #         print("Size     : %s" % template.size)
    #         print("UID      : %s" % template.uid)
    #         print("FID      : %s" % template.fid)
    #         print("Valid    : %s" % template.valid)
    #         print("Template : %s" % template.json_pack())
    #         print("Mark     : %s" % template.mark)
    #     except Exception as e:
    #         print("Process terminate : {}".format(e))
    #     finally:
    #         if self.conn:
    #             self.conn.disconnect()

    def show_success_message(self, message):
        QMessageBox.information(self, "Success", message)

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def on_finger_checkbox_state_changed(self, state):
        checked_box = self.sender()
        name = checked_box.objectName()
        striped_name = name.lstrip('cbFinger')
        if state == 2:
            self.finger_styles.get(int(striped_name)).setStyleSheet(self.selected_btn_style)
        else:
            self.finger_styles.get(int(striped_name)).setStyleSheet(self.default_style)

    def cancel_enrollment(self, button_name):
        self.selected_user = None
        self.selected_finger = None
        button_name.setStyleSheet(self.default_style)

    def find_user_temp(self, user_id, user_password, user_name):
        try:
            conn = self.zk.connect()
            if conn:
                temps = conn.get_templates()
                temps_found = False
                template_found = False
                if temps:
                    temps_found = True
                if temps_found:
                    for temp in temps:
                        if temp.uid == user_id:
                            template_found = True
                    if template_found:
                        self.mesage_box(int(user_id), user_password, user_name, 'نعم', 'لا', 'معلومة',
                                        'هذا الموظف لدية بصمة بالفعل هل تريد تعديلها', 'dialog')

                    else:
                        self.btnDeleteFingersData.setVisible(False)
                        for i in range(len(self.fingers_check_boxes.items())):
                            self.label_styles[i].setVisible(False)
                            self.fingers_check_boxes[i].setVisible(True)
                        self.exec()
                        # self.add_fingers(int(user_id))
                else:
                    QMessageBox.warning(self, "خطأ", "نرجو تحميل البصمات من الجهاز اولاً")
            else:
                QMessageBox.warning(self, "خطأ", "قم بتوصيل الجهاز اولاً")
                # if temp.fid in finger_styles:
                #     print('finger of the users is', temp.fid)
                # else:
                #     for finger_style in finger_styles.values():
                #         finger_style.setStyleSheet(self.default_style)
                #     print("Invalid finger ID:", temp.fid)
                # if not template_found:
                #     users = conn.get_users()
                #     user_found = False
                #     for user in users:
                #         if user.user_id == str(user_id):
                #             user_found = True
                #             QMessageBox.warning(self, "تحدير", "هذا الموظف لدية بصمة بالفعل هل تريد تعديلها")
                #             # for finger_style in finger_styles.values():
                #             #     finger_style.setStyleSheet(self.default_style)
                # #             print("There is no template for this user:", user_id)
                #     if not user_found:
                #         self.exec_()
                # for finger_style in finger_styles.values():
                # finger_style.setStyleSheet(self.default_style)
                # print('user has not fingers data ')
                # QMessageBox.warning(self, "خطأ", "هذا الموظف لم يتم إضافته الى جهاز البصمة")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))

    def mesage_box(self, user_id, user_password, user_name, ok_button_text, cancel_button_text, message_title,
                   message_context, parent_type):
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
        message_box.setIcon(QMessageBox.Information)
        message_box.exec_()
        clicked_button = message_box.clickedButton()
        if parent_type == 'dialog':
            if clicked_button == ok_button:
                self.lblUserName.setText(user_name.text())
                self.txtTeacherDevicePassword.setText(user_password)
                self.btnDeleteFingersData.setVisible(True)
                for i in range(10):
                    self.fingers_check_boxes[i].setVisible(False)
                self.update_user(user_id, user_password)
                self.exec_()
            elif clicked_button == cancel_button:
                self.btnDeleteFingersData.setVisible(False)
                return

    def update_user(self, selected_id, user_password):
        try:
            conn = self.zk.connect()
            if conn:
                for i in range(len(self.label_styles.items())):
                    self.label_styles[i].setVisible(False)
                for i in range(10):
                    user_temps = conn.get_user_template(uid=selected_id, temp_id=i,
                                                        user_id=selected_id)
                    if user_temps:
                        if user_temps.size > 0:
                            self.label_styles[i].setVisible(True)
                        else:
                            self.fingers_check_boxes[i].setVisible(True)
                            self.label_styles[i].setVisible(False)
                    else:
                        self.fingers_check_boxes[i].setVisible(True)
                        self.label_styles[i].setVisible(False)
                # for i in range(10):
                #     temps = conn.get_user_template(uid=selected_id, temp_id=i, user_id=selected_id)
                #     if temps:
                #         self.label_styles[i].setVisible(True)
                #     else:
                #         self.fingers_check_boxes[i].setVisible(True)
                #         self.label_styles[i].setVisible(False)
                if user_password:
                    self.txtTeacherDevicePassword.setText(user_password)
            else:
                QMessageBox.warning(self, "خطأ", "فشل الاتصال بجهاز البصمة")
        except Exception as e:
            QMessageBox.critical(self, "خطأ", str(e))


from icons_rc import icons
