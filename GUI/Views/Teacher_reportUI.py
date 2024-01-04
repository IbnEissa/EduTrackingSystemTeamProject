from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
from weasyprint import HTML

from GUI.Dialogs.TableWedgetOpertaionsHandeler import chickedButton, unchickedButton
from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
# from GUI.Views.DeviceUI import DeviceUI
from models.Members import Members
from models.School import School
from models.Teachers import Teachers
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import peewee
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore
import pdfkit
import base64
import datetime

from models.Weekly_class_schedule import WeeklyClassSchedule
from models.fingerPrintData import FingerPrintData


class Teacher_reportUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedTeacherId = 0
        self.ui.tabTeachersReport.setColumnHidden(0, True)
        self.get_cities_combo_data()

    def use_ui_elements(self):

        self.ui.tabTeachersReport.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tabTeachersReport.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tabTeachersReport.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.txtNameTeacher.textChanged.connect(self.get_report_teacher_data)
        self.ui.combReportCities.currentTextChanged.connect(self.get_report_teacher_by_cities)
        self.ui.combReportGender.currentTextChanged.connect(self.get_report_teacher_by_gender)
        self.ui.txtReportMajor.textChanged.connect(self.get_report_teacher_by_major)
        self.ui.txtReportTask.textChanged.connect(self.get_report_teacher_by_task)
        self.ui.radioHasPrintData.clicked.connect(self.get_report_teacher_has_finger_data)
        self.ui.radioNotHasPrintData.clicked.connect(self.get_report_teacher_not_has_finger_data)

        self.ui.btnReportTeacher.clicked.connect(self.generate_pdf_teacher_report)
        # self.ui.combReportClass.currentTextChanged.connect(self.get_report_class_data)

    def get_cities_combo_data(self):
        cities = Common.get_cities(self.ui)
        self.ui.combReportCities.clear()
        self.ui.combReportCities.addItems(cities)

    def get_report_teacher_data(self):
        search_item = self.ui.txtNameTeacher.text().lower()
        self.ui.tabTeachersReport.setRowCount(0)  # Clear existing rows in the table
        Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
        members_data = Members.select().where(peewee.fn.LOWER(Members.fName).contains(search_item))

        for member in members_data:
            teacher = Teachers.get_or_none(member_id=member.id)
            if teacher:
                no_finger = unchickedButton(table_widget=self.ui.tabTeachersReport)
                finger = chickedButton(table_widget=self.ui.tabTeachersReport)
                has_fingers_data = FingerPrintData.get_teacher_fingers(self.ui, member.id)
                row = self.ui.tabTeachersReport.rowCount()
                self.ui.tabTeachersReport.insertRow(row)
                self.ui.tabTeachersReport.setItem(row, 0, QTableWidgetItem(str(member.id)))
                self.ui.tabTeachersReport.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
                self.ui.tabTeachersReport.setItem(row, 2, QTableWidgetItem(str(member.phone)))
                self.ui.tabTeachersReport.setItem(row, 3, QTableWidgetItem(str(member.gender)))
                self.ui.tabTeachersReport.setItem(row, 4, QTableWidgetItem(str(teacher.cities)))
                self.ui.tabTeachersReport.setItem(row, 5, QTableWidgetItem(str(teacher.major)))
                self.ui.tabTeachersReport.setItem(row, 6, QTableWidgetItem(str(teacher.task)))
                if has_fingers_data is not True:
                    self.ui.tabTeachersReport.setCellWidget(row, 7, no_finger)
                    Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
                    self.ui.tabTeachersReport.setColumnWidth(row, 60)
                    self.ui.tabTeachersReport.setRowHeight(row, 150)
                else:
                    self.ui.tabTeachersReport.setCellWidget(row, 7, finger)
                    Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
                    self.ui.tabTeachersReport.setColumnWidth(row, 60)
                    self.ui.tabTeachersReport.setRowHeight(row, 150)
            Common.style_table_widget(self.ui, self.ui.tabTeachersReport)

    def get_report_teacher_by_cities(self):
        # selected_cities = self.ui.combReportCities.currentText()
        selected_cities = self.ui.combReportCities.currentText().lower()
        self.ui.tabTeachersReport.setRowCount(0)  # Clear existing rows in the table
        Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
        teachers_data = Teachers.select().where(peewee.fn.LOWER(Teachers.cities).contains(selected_cities))
        for teacher in teachers_data:
            member = Members.get_by_id(teacher.member_id)
            has_fingers_data = FingerPrintData.get_teacher_fingers(self.ui, member.id)
            row = self.ui.tabTeachersReport.rowCount()
            self.ui.tabTeachersReport.insertRow(row)
            self.ui.tabTeachersReport.setItem(row, 0, QTableWidgetItem(str(member.id)))
            self.ui.tabTeachersReport.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
            self.ui.tabTeachersReport.setItem(row, 2, QTableWidgetItem(str(member.phone)))
            self.ui.tabTeachersReport.setItem(row, 3, QTableWidgetItem(str(member.gender)))
            self.ui.tabTeachersReport.setItem(row, 4, QTableWidgetItem(str(teacher.cities)))
            self.ui.tabTeachersReport.setItem(row, 5, QTableWidgetItem(str(teacher.major)))
            self.ui.tabTeachersReport.setItem(row, 6, QTableWidgetItem(str(teacher.task)))
            if has_fingers_data is not True:
                item_value = 'لا'
            else:
                item_value = 'نعم'
            self.ui.tabTeachersReport.setItem(row, 7, QTableWidgetItem(item_value))
            Common.style_table_widget(self.ui, self.ui.tabTeachersReport)

    def get_report_teacher_by_major(self):
        # try:
        selected_major = self.ui.txtReportMajor.text().lower()
        self.ui.tabTeachersReport.setRowCount(0)  # Clear existing rows in the table
        Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
        teachers_data = Teachers.select().where(peewee.fn.LOWER(Teachers.major).contains(selected_major))

        for teacher in teachers_data:
            member = Members.get_by_id(teacher.member_id)
            has_fingers_data = FingerPrintData.get_teacher_fingers(self.ui, member.id)
            row = self.ui.tabTeachersReport.rowCount()
            self.ui.tabTeachersReport.insertRow(row)
            self.ui.tabTeachersReport.setItem(row, 0, QTableWidgetItem(str(member.id)))
            self.ui.tabTeachersReport.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
            self.ui.tabTeachersReport.setItem(row, 2, QTableWidgetItem(str(member.phone)))
            self.ui.tabTeachersReport.setItem(row, 3, QTableWidgetItem(str(member.gender)))
            self.ui.tabTeachersReport.setItem(row, 4, QTableWidgetItem(str(teacher.cities)))
            self.ui.tabTeachersReport.setItem(row, 5, QTableWidgetItem(str(teacher.major)))
            self.ui.tabTeachersReport.setItem(row, 6, QTableWidgetItem(str(teacher.task)))
            if has_fingers_data is not True:
                item_value = 'لا'
            else:
                item_value = 'نعم'
            self.ui.tabTeachersReport.setItem(row, 7, QTableWidgetItem(item_value))
            Common.style_table_widget(self.ui, self.ui.tabTeachersReport)

    def get_report_teacher_by_task(self):
        # try:
        selected_task = self.ui.txtReportTask.text().lower()
        self.ui.tabTeachersReport.setRowCount(0)  # Clear existing rows in the table
        Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
        teachers_data = Teachers.select().where(peewee.fn.LOWER(Teachers.task).contains(selected_task))

        for teacher in teachers_data:

            member = Members.get_by_id(teacher.member_id)
            has_fingers_data = FingerPrintData.get_teacher_fingers(self.ui, member.id)
            row = self.ui.tabTeachersReport.rowCount()
            self.ui.tabTeachersReport.insertRow(row)
            self.ui.tabTeachersReport.setItem(row, 0, QTableWidgetItem(str(member.id)))
            self.ui.tabTeachersReport.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
            self.ui.tabTeachersReport.setItem(row, 2, QTableWidgetItem(str(member.phone)))
            self.ui.tabTeachersReport.setItem(row, 3, QTableWidgetItem(str(member.gender)))
            self.ui.tabTeachersReport.setItem(row, 4, QTableWidgetItem(str(teacher.cities)))
            self.ui.tabTeachersReport.setItem(row, 5, QTableWidgetItem(str(teacher.major)))
            self.ui.tabTeachersReport.setItem(row, 6, QTableWidgetItem(str(teacher.task)))
            if has_fingers_data is not True:
                item_value = 'لا'
            else:
                item_value = 'نعم'
            self.ui.tabTeachersReport.setItem(row, 7, QTableWidgetItem(item_value))
            Common.style_table_widget(self.ui, self.ui.tabTeachersReport)

    def get_report_teacher_by_gender(self):
        # try:
        selected_gender = self.ui.combReportGender.currentText().lower()
        self.ui.tabTeachersReport.setRowCount(0)  # Clear existing rows in the table
        Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
        members = Members.select().where(peewee.fn.LOWER(Members.gender).contains(selected_gender))

        for member in members:
            teachers = Teachers.select().where(member.id == Teachers.member_id)
            if teachers:
                for teacher in teachers:
                    has_fingers_data = FingerPrintData.get_teacher_fingers(self.ui, member.id)
                    row = self.ui.tabTeachersReport.rowCount()
                    self.ui.tabTeachersReport.insertRow(row)
                    self.ui.tabTeachersReport.setItem(row, 0, QTableWidgetItem(str(member.id)))
                    self.ui.tabTeachersReport.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
                    self.ui.tabTeachersReport.setItem(row, 2, QTableWidgetItem(str(member.phone)))
                    self.ui.tabTeachersReport.setItem(row, 3, QTableWidgetItem(str(member.gender)))
                    self.ui.tabTeachersReport.setItem(row, 4, QTableWidgetItem(str(teacher.cities)))
                    self.ui.tabTeachersReport.setItem(row, 5, QTableWidgetItem(str(teacher.major)))
                    self.ui.tabTeachersReport.setItem(row, 6, QTableWidgetItem(str(teacher.task)))
                    if has_fingers_data is not True:
                        item_value = 'لا'
                    else:
                        item_value = 'نعم'
                    self.ui.tabTeachersReport.setItem(row, 7, QTableWidgetItem(item_value))
                    Common.style_table_widget(self.ui, self.ui.tabTeachersReport)

    def get_report_teacher_has_finger_data(self):
        # try:
        if self.ui.radioHasPrintData.isChecked():
            self.ui.tabTeachersReport.setRowCount(0)  # Clear existing rows in the table
            Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
            has_fingers_data = FingerPrintData.select()
            for finger in has_fingers_data:
                member = Members.get_by_id(finger.teacher_id)
                teacher = Teachers.get(Teachers.member_id == finger.teacher_id)
                row = self.ui.tabTeachersReport.rowCount()
                self.ui.tabTeachersReport.insertRow(row)
                self.ui.tabTeachersReport.setItem(row, 0, QTableWidgetItem(str(member.id)))
                self.ui.tabTeachersReport.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
                self.ui.tabTeachersReport.setItem(row, 2, QTableWidgetItem(str(member.phone)))
                self.ui.tabTeachersReport.setItem(row, 3, QTableWidgetItem(str(member.gender)))
                self.ui.tabTeachersReport.setItem(row, 4, QTableWidgetItem(str(teacher.cities)))
                self.ui.tabTeachersReport.setItem(row, 5, QTableWidgetItem(str(teacher.major)))
                self.ui.tabTeachersReport.setItem(row, 6, QTableWidgetItem(str(teacher.task)))
                item_value = 'نعم'
                self.ui.tabTeachersReport.setItem(row, 7, QTableWidgetItem(item_value))
                Common.style_table_widget(self.ui, self.ui.tabTeachersReport)

    def get_report_teacher_not_has_finger_data(self):
        # try:
        if self.ui.radioNotHasPrintData.isChecked():
            self.ui.tabTeachersReport.setRowCount(0)  # Clear existing rows in the table
            Common.style_table_widget(self.ui, self.ui.tabTeachersReport)
            fingers_data = FingerPrintData.select()
            fingers = []
            for finger in fingers_data:
                teacher_id = finger.teacher_id
                fingers.append(teacher_id)
            # print("the fingers array is ", fingers)
            teachers = Teachers.select().where(Teachers.member_id not in fingers)
            print("the teacher is ", teachers)
            for teacher in teachers:
                member = Members.get_by_id(teacher.member_id)
                row = self.ui.tabTeachersReport.rowCount()
                self.ui.tabTeachersReport.insertRow(row)
                self.ui.tabTeachersReport.setItem(row, 0, QTableWidgetItem(str(member.id)))
                self.ui.tabTeachersReport.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
                self.ui.tabTeachersReport.setItem(row, 2, QTableWidgetItem(str(member.phone)))
                self.ui.tabTeachersReport.setItem(row, 3, QTableWidgetItem(str(member.gender)))
                self.ui.tabTeachersReport.setItem(row, 4, QTableWidgetItem(str(teacher.cities)))
                self.ui.tabTeachersReport.setItem(row, 5, QTableWidgetItem(str(teacher.major)))
                self.ui.tabTeachersReport.setItem(row, 6, QTableWidgetItem(str(teacher.task)))
                item_value = 'لا'
                self.ui.tabTeachersReport.setItem(row, 7, QTableWidgetItem(item_value))
                Common.style_table_widget(self.ui, self.ui.tabTeachersReport)

        # def get_report_class_data(self):
        #     try:
        #         search_item = self.ui.combReportClass.currentText().lower()
        #         column = ['id', 'fName', 'sName', 'tName', 'lName', 'phone', 'major', 'task']
        #
        #         members_query = (
        #                 Teachers
        #                 .select(Teachers, Members)
        #                 .join(WeeklyClassSchedule)
        #                 .join(Members, on=(Members.id == WeeklyClassSchedule.teacher_id))
        #                 .where(
        #                     WeeklyClassSchedule.class_room_id == ClassRoom.id) & (ClassRoom.name == search_item))
        #
        #         self.ui.tabTeachersReport.setRowCount(0)  # Clear existing rows in the table
        #
        #         for row, member_data in enumerate(members_query):
        #             table_items = []
        #             for column_name in column:
        #                 try:
        #                     item_value = getattr(member_data, column_name)
        #
        #                 except AttributeError:
        #                     report_data = Teachers.get(Teachers.members_id == member_data.id)
        #                     item_value = getattr(report_data, column_name)
        #
        #                 table_item = QTableWidgetItem(str(item_value))
        #                 table_items.append(table_item)
        #
        #             self.ui.tabTeachersReport.insertRow(row)
        #             for col, item in enumerate(table_items):
        #                 self.ui.tabTeachersReport.setItem(row, col, item)
        #
        #     except Exception as e:
        #         error_message = "حدث خطأ:\n\n" + str(e)
        # QMessageBox.critical(self.ui, "خطأ", error_message)

    def generate_pdf_teacher_report(self):
        # Get the table widget
        table_widget = self.ui.tabTeachersReport
        school_name = School.select(peewee.fn.Max(School.school_name)).scalar()

        # Get the column names
        column_names = ['الرقم', 'الاسم ', 'التلفون', 'الجنس', 'المحافظة', 'المؤهل', 'التخصص',
                        'هل لدية بيانات بصمة']

        # Read the image file and encode it as base64
        image_path = "C:/Users/User15/PycharmProjects/last version of school project/Team Version/EduTrackingSystemTeamProject/icons_rc/ministry.png"
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        # if table_widget.rowCount() > 0:
        # Create the HTML table and CSS styles
        html_table = f"""
                    <html>
                    <head><br>
                    <h3 style="text-align: center; margin-top: 0px;">بسم الله الرحمن الرحيم</h3>
                    <style>
                        @page {{
                            size: auto;
                            margin-top: 0;
                        }}
                        .container {{
                            width: 100%;
                            margin: 0px 65px 65px 65px;
                        }}
                        .container table {{
                            border-collapse: collapse;
                            width: 100%;
                        }}
                        .container th, .container td {{
                            border: 1px solid black;
                            padding: 8px;
                            text-align: right;
                        }}
                        .first-table {{
                            direction: ltr;
                            transform-origin: top right;
                            transform: scale(1.2);
                            border-collapse: separate;
                            border-spacing: 0;
                            border: none;
    
                        }}
                        .first-table td {{
                            position: relative;
                            padding: 0;
                        }}
                        .first-table img {{
                            max-width: 80px;
    
                            position: absolute;
                            left: 0;
                            center: 0;
                            transform: translate(20%, -50%);
                        }}
                        .second-table {{
                            border-collapse: collapse;
                            direction: rtl;
                            width: 100%;
                        }}
                        .second-table th, .second-table td {{
                            border: 1px solid black;
                            padding: 8px;
                            direction: rtl;
                            text-align: center;
                             }}
                        .first-table td:first-child,
                        .first-table td:first-child + td,
                        .first-table td:first-child + td + td {{
                            border: none;
                        }}
    
    
                    </style>
                    </head>
                    <body>
                    <div class="container">
                        <table class="first-table">
                            <tr>
                                <td></td>
                                <td rowspan="3"><img src="data:image/png;base64,{encoded_image}"></td>
                                <td>الجمهورية اليمنية</td>
                            </tr>
                            <tr>
                                <td></td>
                                <td>وزارة التربية والتعليم</td>
                            </tr>
                            <tr>
                                <td style="text-align: left;">التاريخ: {datetime.datetime.now().strftime("%d-%m-%Y")}</td>
                                <td>مدرسة {school_name} </td>
                            </tr>
    
                        </table>
    
    
                    </div>
                    <hr style=" transform: scale(1.2);"><br><br><br>  
    
                    <table class="second-table">
                <caption class="table-caption">
                    <center>
                        <font size='5' color='black'><i> تقرير أسماء المعلمين </i></font>
                    </center>
                </caption>  
                            <tr>
                    """

        # Add the header row
        for name in column_names:
            html_table += f"<th>{name}</th>"
        html_table += "</tr>"

        # Add data rows
        for row in range(table_widget.rowCount()):
            html_table += "<tr>"
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                value = item.text() if item else ""
                html_table += f"<td>{value}</td>"
            html_table += "</tr>"

        html_table += """
                    </table>
                    </body>
                    </html>
                    """

        # Specify the path and filename for the PDF file
        output_file = 'output.pdf'

        # Generate the PDF from the HTML content
        HTML(string=html_table).write_pdf(output_file)

        # Open a file dialog to select the output PDF file path
        filename, _ = QFileDialog.getSaveFileName(None, 'Save PDF Report', '', 'PDF Files (*.pdf)')
        if filename:
            # Move the generated PDF file to the desired output location
            os.rename(output_file, filename)

            # Show a success message
            QMessageBox.information(self.ui, "نجاح", "تم حفظ التقرير PDF بنجاح!")
    # # Add the data rows
    # for row in range(table_widget.rowCount()):
    #     html_table += "<tr>"
    #     for col in range(table_widget.columnCount()):
    #         if col == 0:  # Add values from the sixth column onwards
    #             item = table_widget.item(row, col)
    #             if item is not None:
    #                 value = item.text()
    #             else:
    #                 value = ""
    #             html_table += f"<td>{value}</td>"
    #         elif col == 1:  # Combine values from second, third, fourth, and fifth columns
    #             combined_value = ""
    #             for sub_col in range(1, 5):  # Combine values from columns 1, 2, 3, and 4 (0-indexed)
    #                 item = table_widget.item(row, sub_col)
    #                 if item is not None:
    #                     value = item.text()
    #                     combined_value += value + " "
    #             html_table += f"<td>{combined_value.strip()}</td>"
    #         elif col >= 5:  # Add values from the sixth column onwards
    #             item = table_widget.item(row, col)
    #             if item is not None:
    #                 value = item.text()
    #             else:
    #                 value = ""
    #             html_table += f"<td>{value}</td>"
    #     html_table += "</tr>"
