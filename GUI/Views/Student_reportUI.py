import base64
from datetime import datetime
import datetime
import logging
import peewee
from PyQt5.QtCore import QDate, Qt
from weasyprint import HTML

from models.ClassRoom import ClassRoom

from PyQt5.QtWidgets import QAbstractItemView, QHeaderView, QDialog, QMessageBox, QTableWidgetItem, QPushButton, \
    QWidget, QHBoxLayout, QVBoxLayout
from GUI.Views.CommonFunctionality import Common
from GUI.Views.DeviceUI import DeviceUI
from models.Members import Members
from models.School import School
from models.Students import Students
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import pdfkit
import datetime
from icons_rc import icons


class Student_reportUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ips = ''
        self.ports = ''
        self.lastInsertedMemberId = 0
        self.lastInsertedTeacherId = 0
        self.finger_button_state = True
        self.ui.tabStudentsReport.setColumnHidden(0, True)
        self.set_data_in_comboSearch()

    def use_ui_elements(self):
        self.ui.combStudentReport.currentTextChanged.connect(self.get_report_student_data)
        self.ui.btnReportStudent.clicked.connect(self.generate_pdf_student_report)

    def set_data_in_comboSearch(self):
        self.ui.combStudentReport.clear()
        data = ClassRoom.select(ClassRoom.id, ClassRoom.name)

        for d in data:
            self.ui.combStudentReport.addItem(d.name, userData=d.id)
            # self.ui.comboStudReport.setItemData(d.id, d.id)

    def get_report_student_data(self):
        current_text = self.ui.combStudentReport.currentText()
        class_room = ClassRoom.select().where(ClassRoom.name == current_text).first()

        if class_room:
            class_room_id = class_room.id
            self.ui.tabStudentsReport.setColumnHidden(8, False)
            self.ui.tabStudentsReport.setRowCount(0)
            Common.style_table_widget(self.ui, self.ui.tabStudentsReport)
            students_data = Students.select().where(Students.class_id == class_room_id)
            for student in students_data:
                member = Members.get_by_id(student.member_id)
                class_name = class_room.name
                row = self.ui.tabStudentsReport.rowCount()
                self.ui.tabStudentsReport.insertRow(row)
                self.ui.tabStudentsReport.setItem(row, 0, QTableWidgetItem(str(member.id)))
                self.ui.tabStudentsReport.setItem(row, 1, QTableWidgetItem(f"{member.fName} {member.lName}"))
                self.ui.tabStudentsReport.setItem(row, 2, QTableWidgetItem(class_name))
                self.ui.tabStudentsReport.setItem(row, 3, QTableWidgetItem(str(member.dateBerth)))
                self.ui.tabStudentsReport.setItem(row, 4, QTableWidgetItem(str(member.phone)))
                Common.style_table_widget(self.ui, self.ui.tabStudentsReport)

        else:
            QMessageBox.information(self.ui, "تحذير", "لا توجد بيانات")

    def generate_pdf_student_report(self):
        # Get the table widget
        table_widget = self.ui.tabStudentsReport
        school_name = School.select(peewee.fn.Max(School.school_name)).scalar()

        # Get the column names
        column_names = ['الرقم', 'الاسم', 'الصف', 'تاريخ الميلاد', 'رقم التلفون']

        # Read the image file and encode it as base64
        # image_path = "/icons/ministry.png"
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
                <font size='5' color='black'><i> تقرير أسماء الطلاب </i></font>
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
        # else:
        #     QMessageBox.information(self.ui, "الصلاحية", "ليس لديك بيانات لتصديرها")

