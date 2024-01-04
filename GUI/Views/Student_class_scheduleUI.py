import base64

import peewee
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidgetItem, QRadioButton, QComboBox, QButtonGroup, QMessageBox
from weasyprint import HTML

from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import pdfkit
import datetime

from models.School import School
from models.Teachers_Schedule import Teachers_Schedule


class Student_class_scheduleUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.get_classes()
        # self.get_session()
        # self.get_subject()
        # self.get_days()

    def use_ui_elements(self):
        self.ui.tblStudentSchedule.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblStudentSchedule.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblStudentSchedule.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # self.ui.btnAddNewStudentSchedule.clicked.connect(self.add_new_student_schedule)
        self.ui.btnShowScheduleStudents.clicked.connect(self.get_data_schedule_students)
        self.ui.btnReportAddNewStudentSchedule.clicked.connect(self.generate_pdf_schedule_student_report)

    def get_classes(self):
        classes = ClassRoom.select(ClassRoom.name)
        for classe in classes:
            self.ui.combClassStudentSelected.addItem(classe.name)

    #
    # def get_session(self):
    #     session = Common.get_sessions(self.ui)
    #     self.ui.combChosseSession.clear()
    #     self.ui.combChosseSession.addItems(session)
    #
    # def get_subject(self):
    #     subject = Common.get_subjects(self.ui)
    #     self.ui.combChosseSubject.clear()
    #     self.ui.combChosseSubject.addItems(subject)
    #
    # def get_days(self):
    #     subject = Common.get_days(self.ui)
    #     self.ui.combChosseDay.clear()
    #     self.ui.combChosseDay.addItems(subject)

    # def add_new_student_schedule(self):
    #     selected_class = self.ui.combChosseClass.currentText()
    #     selected_session = self.ui.combChosseSession.currentText()
    #     selected_subject = self.ui.combChosseSubject.currentText()
    #     selected_day = self.ui.combChosseDay.currentText()
    #     current_row = self.ui.tblStudentSchedule.rowCount()
    #     self.ui.tblStudentSchedule.insertRow(current_row)
    #     self.ui.tblStudentSchedule.setItem(current_row, 0, QTableWidgetItem(selected_class))
    #     self.ui.tblStudentSchedule.setItem(current_row, 1, QTableWidgetItem(selected_session))
    #     self.ui.tblStudentSchedule.setItem(current_row, 2, QTableWidgetItem(selected_subject))
    #     self.ui.tblStudentSchedule.setItem(current_row, 3, QTableWidgetItem(selected_day))

    def get_data_schedule_students(self):
        selected_name_class = self.ui.combClassStudentSelected.currentText()
        if selected_name_class == "الاول" or selected_name_class == "الثاني" or selected_name_class == "الثالث" \
                or selected_name_class == "الرابع" or selected_name_class == "الخامس" or selected_name_class == "السادس" or selected_name_class == "السابع" \
                or selected_name_class == "الثامن":
            query = Teachers_Schedule.select().where(
                Teachers_Schedule.Class_Name == selected_name_class
            ).order_by(
                Teachers_Schedule.Day,
                Teachers_Schedule.session
            )

            # Create a mapping of session values to column indices
            session_mapping = {
                'الاولى': 0,
                'الثانية': 1,
                'الثالثة': 2,
                'الرابعة': 3,
                'الخامسة': 4,
                'السادسة': 5,
                'السابعة': 6,
            }

            # Create a mapping of day values to row indices
            day_mapping = {
                'السبت': 0,
                'الاحد': 1,
                'الاثنين': 2,
                'الثلاثاء': 3,
                'الاربعاء': 4,
                'الخميس': 5,
            }

            table_widget = self.ui.tblStudentSchedule  # Replace "tblShowScheduleStudents" with the actual name of your QTableWidget

            # Clear the table widget
            table_widget.clearContents()

            # Iterate over the query results and populate the table widget
            for schedule in query:
                day_index = day_mapping.get(schedule.Day)
                if day_index is None:
                    continue  # Skip rows with invalid 'Day' values

                # Determine the column index based on the value of 'session'
                session_index = session_mapping.get(schedule.session)
                if session_index is None:
                    continue  # Skip columns with invalid 'session' values

                item_subject = QTableWidgetItem(schedule.Subject)
                table_widget.setItem(day_index, session_index, item_subject)

        else:
            table_widget = self.ui.tblStudentSchedule  # Replace "tblShowScheduleStudents" with the actual name of your QTableWidget
            table_widget.clearContents()

    ##############################################################################
    # this code to show subject with name teacher

    # selected_name_class = self.ui.combClassStudentSelected.currentText()
    # if selected_name_class == "الثالث" or selected_name_class == "الرابع":
    #     query = Teachers_Schedule.select().where(
    #         Teachers_Schedule.Class_Name == selected_name_class
    #     ).order_by(
    #         Teachers_Schedule.Day,
    #         Teachers_Schedule.session
    #     )
    #
    #     # Create a mapping of session values to column indices
    #     session_mapping = {
    #         'الاولى': 0,
    #         'الثانية': 1,
    #         'الثالثة': 2,
    #         'الرابعة': 3,
    #         'الخامسة': 4,
    #         'السادسة': 5,
    #         'السابعة': 6,
    #     }
    #
    #     # Create a mapping of day values to row indices
    #     day_mapping = {
    #         'السبت': 0,
    #         'الاحد': 1,
    #         'الاثنين': 2,
    #         'الثلاثاء': 3,
    #         'الاربعاء': 4,
    #         'الخميس': 5,
    #     }
    #
    #     table_widget = self.ui.tblShowScheduleStudents  # Replace "tblShowScheduleStudents" with the actual name of your QTableWidget
    #
    #     # Clear the table widget
    #     table_widget.clearContents()
    #
    #     # Iterate over the query results and populate the table widget
    #     for schedule in query:
    #         day_index = day_mapping.get(schedule.Day)
    #         if day_index is None:
    #             continue  # Skip rows with invalid 'Day' values
    #
    #         # Determine the column index based on the value of 'session'
    #         session_index = session_mapping.get(schedule.session)
    #         if session_index is None:
    #             continue  # Skip columns with invalid 'session' values
    #
    #         subject_teacher = f"{schedule.Subject} - {schedule.Teacher_Name}"
    #         item_subject = QTableWidgetItem(subject_teacher)
    #         table_widget.setItem(day_index, session_index, item_subject)
    #
    # else:
    #     table_widget = self.ui.tblShowScheduleStudents  # Replace "tblShowScheduleStudents" with the actual name of your QTableWidget
    #     table_widget.clearContents()

    def generate_pdf_schedule_student_report(self):
        table_widget = self.ui.tblStudentSchedule
        school_name = School.select(peewee.fn.Max(School.school_name)).scalar()

        # Read the image file and encode it as base64
        image_path = "C:/Users/User15/PycharmProjects/last version of school project/Team Version/EduTrackingSystemTeamProject/icons_rc/ministry.png"
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Get the column names
        column_names = ['الاولى', 'الثانية', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة']

        # Additional column names for days of the week
        days_week = ['السبت', 'الاحد', 'الاثنين', 'الثلاثاء', 'الاربعاء', 'الخميس']
        name_class = self.ui.combClassStudentSelected.currentText()

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
                   top: 50%;
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
                       <td>مدرسة {school_name}</td>
                   </tr>
               </table>
           </div>
           <hr style=" transform: scale(1.2);"><br><br><br>  
           <table class="second-table">
               <caption><center><font size='5' color='black'<italc>جدول الحصص الاسبوعية للصف {name_class}</italc> </font></center></caption>
               <tr>
           """

        # Add the header row
        html_table += "<tr>"
        html_table += "<th>اليوم</th>"  # Header for the first column
        for name in column_names:
            html_table += f"<th>{name}</th>"
        html_table += "</tr>"

        # Add the data rows
        for row in range(table_widget.rowCount()):
            html_table += "<tr>"
            html_table += f"<td><b>{days_week[row]}</b></td>"  # Day of the week column
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                if item is not None:
                    value = item.text()
                else:
                    value = ""
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
        #     QMessageBox.information(self.ui, "معلومة", "ليس لديك بيانات لتصديرها")
