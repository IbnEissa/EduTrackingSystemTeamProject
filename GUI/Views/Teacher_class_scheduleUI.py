import base64

import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidgetItem, QRadioButton, QComboBox, QButtonGroup, QMessageBox

from GUI.Dialogs.TableWedgetOpertaionsHandeler import DeleteUpdateButtonTeacherScheduleWidget
from GUI.Views.CommonFunctionality import Common
from models.ClassRoom import ClassRoom
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import pdfkit
import datetime

from models.School import School
from models.Teachers import Teachers
from models.Members import Members
from models.Teachers_Schedule import Teachers_Schedule
from models.term_table import TeacherSubjectClassRoomTermTable


class Teacher_class_scheduleUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.ui.tblTeacherSchedule.setColumnHidden(0, True)
        self.ui.tblTeacherSchedule.setColumnHidden(6, True)
        self.get_classe()
        self.get_session()
        self.get_subject()
        self.get_days()
        self.get_teacher()

    def use_ui_elements(self):
        self.ui.tblStudentSchedule.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tblStudentSchedule.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tblStudentSchedule.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.btnAddNewTeacherSchedule.clicked.connect(self.add_new_teacher_schedule)
        self.ui.btnShowDataTeachers.clicked.connect(self.get_data_schedule_teacher_for_changed)
        self.ui.btnShowScheduleTeachers.clicked.connect(self.get_data_schedule_teacher_for_export)
        self.ui.btnReportAddNewTeacherSchedule.clicked.connect(self.generate_pdf_schedule_teacher_report)
        self.ui.RemveTableTeacher.clicked.connect(self.remove_teacher_schedule)

    def get_classe(self):
        class_ids = TeacherSubjectClassRoomTermTable.select(TeacherSubjectClassRoomTermTable.class_room_id)
        class_names = []
        for class_id in class_ids:
            class_name = ClassRoom.get_class_name_from_id(self.ui, class_id.class_room_id)
            class_names.append(class_name)
        for class_name in class_names:
            self.ui.combTeacherChosseClass.addItem(class_name)

    def get_session(self):
        session = Common.get_sessions(self.ui)
        self.ui.combTeacherChosseSession.clear()
        self.ui.combTeacherChosseSession.addItems(session)

    def get_subject(self):
        selected_class_name = self.ui.combTeacherChosseClass.currentText()
        class_name = ClassRoom.get_class_id_from_name(self.ui, selected_class_name)
        get_subjects = TeacherSubjectClassRoomTermTable.select(TeacherSubjectClassRoomTermTable.subject_id).where(
            TeacherSubjectClassRoomTermTable.class_room_id == class_name
        )
        for subject in get_subjects:
            self.ui.combTeacherChosseSubject.addItem(subject.subject_id)

    def get_days(self):
        subject = Common.get_days(self.ui)
        self.ui.combTeacherChosseDay.clear()
        self.ui.combTeacherChosseDay.addItems(subject)

    def get_teacher(self):
        teacher_list = Teachers.select()
        for teacher in teacher_list:
            member = Members.get_by_id(teacher.member_id)
            self.ui.combChosseTeacher.addItem(member.fName + ' ' + member.lName)
            index = self.ui.combChosseTeacher.count() - 1
            self.ui.combChosseTeacher.setItemData(index, member.id, role=Qt.UserRole)

    def add_new_teacher_schedule(self):
        self.ui.tblTeacherSchedule.setColumnHidden(6, True)
        selected_class = self.ui.combTeacherChosseClass.currentText()
        selected_session = self.ui.combTeacherChosseSession.currentText()
        selected_subject = self.ui.combTeacherChosseSubject.currentText()
        selected_day = self.ui.combTeacherChosseDay.currentText()
        selected_teacher = self.ui.combChosseTeacher.currentText()
        class_name = ClassRoom.get_class_id_from_name(self.ui, selected_class)

        query = TeacherSubjectClassRoomTermTable.select(
            TeacherSubjectClassRoomTermTable.number_of_lessons
        ).where(
            (TeacherSubjectClassRoomTermTable.subject_id == selected_subject) &
            (TeacherSubjectClassRoomTermTable.class_room_id == class_name)
        )

        number_of_lessons = query.get().number_of_lessons
        print(f'Number of lessons: {number_of_lessons}')

        query = (
            Teachers_Schedule
            .select()
            .where(
                (Teachers_Schedule.Subject == selected_subject) &
                (Teachers_Schedule.Class_Name == selected_class)
            )
        )

        number_of_lessons_for_subject = query.count()
        print(f'Number of subjects: {number_of_lessons_for_subject}')
        subject = int(number_of_lessons_for_subject)
        lessons = int(number_of_lessons)
        if subject >= lessons:
            QMessageBox.information(self.ui, "تحذير", "اكتمل عدد الحصص لهذا المادة")

        else:
            # Check if the selected teacher already has the selected session assigned in any class
            query_session_teacher = Teachers_Schedule.select().where(
                Teachers_Schedule.Teacher_Name == selected_teacher,
                Teachers_Schedule.session == selected_session,
                Teachers_Schedule.Day == selected_day,
                Teachers_Schedule.Class_Name != selected_class
            )
            if query_session_teacher.exists():
                QMessageBox.information(self.ui, "تحذير", "تم تعيين الحصة لمعلم آخر")
            else:
                # Check if the selected session is already assigned to any teacher in the selected class
                query_session_class = Teachers_Schedule.select().where(
                    Teachers_Schedule.Class_Name == selected_class,
                    Teachers_Schedule.session == selected_session,
                    Teachers_Schedule.Day == selected_day,
                    Teachers_Schedule.Teacher_Name != selected_teacher
                )
                if query_session_class.exists():
                    QMessageBox.information(self.ui, "تحذير", "تم تعيين الحصة لمعلم آخر")
                else:
                    query_duplicate_session = Teachers_Schedule.select().where(
                        Teachers_Schedule.Teacher_Name == selected_teacher,
                        Teachers_Schedule.Class_Name == selected_class,
                        Teachers_Schedule.session == selected_session,
                        Teachers_Schedule.Day == selected_day
                    )
                    if query_duplicate_session.exists():
                        QMessageBox.information(self.ui, "تحذير", "تم تعيين نفس الحصة للمعلم في نفس الفصل في نفس اليوم")
                    else:
                        # Insert the new entry into the Teachers_Schedule table
                        Teachers_Schedule.create(
                            Teacher_Name=selected_teacher,
                            Day=selected_day,
                            Subject=selected_subject,
                            session=selected_session,
                            Class_Name=selected_class
                        )
                        QMessageBox.information(self.ui, "نجاح", "تم الحفظ بنجاح")
                        current_row = self.ui.tblTeacherSchedule.rowCount()
                        self.ui.tblTeacherSchedule.insertRow(current_row)
                        self.ui.tblTeacherSchedule.setItem(current_row, 1, QTableWidgetItem(selected_day))
                        self.ui.tblTeacherSchedule.setItem(current_row, 2, QTableWidgetItem(selected_subject))
                        self.ui.tblTeacherSchedule.setItem(current_row, 3, QTableWidgetItem(selected_session))
                        self.ui.tblTeacherSchedule.setItem(current_row, 4, QTableWidgetItem(selected_class))
                        self.ui.tblTeacherSchedule.setItem(current_row, 5, QTableWidgetItem(selected_teacher))
                        self.ui.tblTeacherSchedule.setColumnWidth(current_row, 40)
                        self.ui.tblTeacherSchedule.setRowHeight(current_row, 150)
                        Common.style_table_widget(self.ui, self.ui.tblTeacherSchedule)
                        if selected_session == "السابعة":
                            self.ui.tblTeacherSchedule.setRowCount(0)  # Clear existing rows in the table
                            QMessageBox.information(self.ui, "اشعار",
                                                    f"أختار اليوم التالي لأضافة الحصص للصف {selected_class}")
                if self.ui.tblTeacherSchedule.rowCount() == 42:
                    QMessageBox.information(self.ui, "اشعار", f"تم اضافة الجدول الاسبوعي للصف {selected_class}")

    def remove_teacher_schedule(self):
        self.ui.tblTeacherSchedule.setRowCount(0)

    def get_data_schedule_teacher_for_changed(self):
        # self.ui.tblTeacherSchedule.setColumnHidden(0, True)
        self.ui.tblTeacherSchedule.setColumnHidden(6, False)
        try:
            columns = ['id', 'Day', 'Subject', 'session', 'Class_Name', 'Teacher_Name']
            selected_class = self.ui.combTeacherChosseClass.currentText().lower()
            # selected_session = self.ui.combTeacherChosseSession.currentText().lower()
            # selected_subject = self.ui.combTeacherChosseSubject.currentText().lower()
            # selected_day = self.ui.combTeacherChosseDay.currentText().lower()
            # selected_teacher = self.ui.combChosseTeacher.currentText().lower()
            members_query = Teachers_Schedule.select().where(
                # (peewee.fn.LOWER(Teachers_Schedule.Class_Name).contains(selected_class)) |
                # (peewee.fn.LOWER(Teachers_Schedule.session).contains(selected_session)) |
                # (peewee.fn.LOWER(Teachers_Schedule.Subject).contains(selected_subject)) |
                # (peewee.fn.LOWER(Teachers_Schedule.Day).contains(selected_day)) |
                (peewee.fn.LOWER(Teachers_Schedule.Class_Name).contains(selected_class))
            ).distinct()
            self.ui.tblTeacherSchedule.setRowCount(0)  # Clear existing rows in the table
            for row, member_data in enumerate(members_query):
                table_items = []
                for column_name in columns:
                    try:
                        item_value = getattr(member_data, column_name)
                    except AttributeError:
                        teacher_schedule_data = Teachers_Schedule.get(Teachers_Schedule.id == member_data.id)
                        item_value = getattr(teacher_schedule_data, column_name)

                    table_item = QTableWidgetItem(str(item_value))
                    table_items.append(table_item)

                self.ui.tblTeacherSchedule.insertRow(row)
                for col, item in enumerate(table_items):
                    self.ui.tblTeacherSchedule.setItem(row, col, item)

                self.ui.tblTeacherSchedule.setColumnWidth(row, 40)
                self.ui.tblTeacherSchedule.setRowHeight(row, 150)
                operations_buttons = DeleteUpdateButtonTeacherScheduleWidget(table_widget=self.ui.tblTeacherSchedule)
                self.ui.tblTeacherSchedule.setCellWidget(row, 6, operations_buttons)
                Common.style_table_widget(self.ui, self.ui.tblTeacherSchedule)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def get_data_schedule_teacher_for_export(self):
        # استعلم جدول Teachers_Schedule للحصول على البيانات المطلوبة
        query = Teachers_Schedule.select().execute()

        # Clear the existing contents of the table widget
        table_widget = self.ui.tblShowScheduleTeachers
        table_widget.clearContents()

        # Define column mapping for session and table column index
        column_mapping = {
            ('السبت', 'الاولى'): 1,
            ('السبت', 'الثانية'): 2,
            ('السبت', 'الثالثة'): 3,
            ('السبت', 'الرابعة'): 4,
            ('السبت', 'الخامسة'): 5,
            ('السبت', 'السادسة'): 6,
            ('السبت', 'السابعة'): 7,
            ('الاحد', 'الاولى'): 8,
            ('الاحد', 'الثانية'): 9,
            ('الاحد', 'الثالثة'): 10,
            ('الاحد', 'الرابعة'): 11,
            ('الاحد', 'الخامسة'): 12,
            ('الاحد', 'السادسة'): 13,
            ('الاحد', 'السابعة'): 14,
            ('الاثنين', 'الاولى'): 15,
            ('الاثنين', 'الثانية'): 16,
            ('الاثنين', 'الثالثة'): 17,
            ('الاثنين', 'الرابعة'): 18,
            ('الاثنين', 'الخامسة'): 19,
            ('الاثنين', 'السادسة'): 20,
            ('الاثنين', 'السابعة'): 21,
            ('الثلاثاء', 'الاولى'): 22,
            ('الثلاثاء', 'الثانية'): 23,
            ('الثلاثاء', 'الثالثة'): 24,
            ('الثلاثاء', 'الرابعة'): 25,
            ('الثلاثاء', 'الخامسة'): 26,
            ('الثلاثاء', 'السادسة'): 27,
            ('الثلاثاء', 'السابعة'): 28,
            ('الاربعاء', 'الاولى'): 29,
            ('الاربعاء', 'الثانية'): 30,
            ('الاربعاء', 'الثالثة'): 31,
            ('الاربعاء', 'الرابعة'): 32,
            ('الاربعاء', 'الخامسة'): 33,
            ('الاربعاء', 'السادسة'): 34,
            ('الاربعاء', 'السابعة'): 35,
            ('الخميس', 'الاولى'): 36,
            ('الخميس', 'الثانية'): 37,
            ('الخميس', 'الثالثة'): 38,
            ('الخميس', 'الرابعة'): 39,
            ('الخميس', 'الخامسة'): 40,
            ('الخميس', 'السادسة'): 41,
            ('الخميس', 'السابعة'): 42
        }

        # Create a dictionary to store the row index for each teacher name
        teacher_rows = {}

        # Iterate over the query results and populate the table
        for item in query:
            teacher_name = item.Teacher_Name
            day = item.Day
            session = item.session

            # Find the row index for the teacher name
            if teacher_name in teacher_rows:
                row = teacher_rows[teacher_name]
            else:
                row = table_widget.rowCount()
                table_widget.setRowCount(row + 1)
                teacher_name_item = QTableWidgetItem(teacher_name)
                table_widget.setItem(row, 0, teacher_name_item)
                teacher_rows[teacher_name] = row
            if (day, session) in column_mapping:
                column = column_mapping[(day, session)]
                class_name = item.Class_Name
                subject = item.Subject
                combined_text = f"{subject}  ({class_name})"
                subject_item = QTableWidgetItem(combined_text)
                table_widget.setItem(row, column, subject_item)

    def generate_pdf_schedule_teacher_report(self):

        table_widget = self.ui.tblShowScheduleTeachers
        school_name = School.select(peewee.fn.Max(School.school_name)).scalar()

        # Read the image file and encode it as base64
        image_path = "C:/Users/User15/PycharmProjects/last version of school project/Team Version/EduTrackingSystemTeamProject/icons_rc/ministry.png"
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
        # if table_widget.rowCount() > 0:
        # Define the column names
        header_days = ['', "السبت",
                       "الاحد",
                       "الاثنين",
                       "الثلاثاء",
                       "الاربعاء",
                       "الخميس", ]
        # Get the column names
        header_sessions = ['اسم المعلم', 'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة',
                           'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة',
                           'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة',
                           'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة',
                           'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة',
                           'الاولى', 'الثانية ', 'الثالثة', 'الرابعة', 'الخامسة', 'السادسة', 'السابعة']

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
                margin:auto;
                float: left;
                size: auto;
            }}
            .first-table td {{
                position: relative;
                top: 0;
                right: 70px;
            }}
             .first-table img {{
                max-width: 80px;
                position: relative;
                right: 275px;
            }}
            .second-table-container {{
                width: 100%;
                overflow: hidden; /* Added property */
            }}
            .second-table {{
                border-collapse: collapse;
                direction: rtl;
                width: 00%;
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
            <caption><center><font size='5' color='black'<italc>جدول الحصص الاسبوعي للمعلمين </italc> </font></center></caption>
            <tr>
        """
        html_table += "<tr>"
        for i, name in enumerate(header_days):
            if i == 1:
                html_table += "<th colspan='7'>السبت</th>"
            elif i == 2:
                html_table += "<th colspan='7'>الأحد</th>"
            elif i == 3:
                html_table += "<th colspan='7'>الاثنين</th>"
            elif i == 4:
                html_table += "<th colspan='7'>الثلاثاء</th>"
            elif i == 5:
                html_table += "<th colspan='7'>الأربعاء</th>"
            elif i == 6:
                html_table += "<th colspan='7'>الخميس</th>"
            else:
                html_table += f"<th>{name}</th>"

        html_table += "<tr>"
        for name in header_sessions:
            html_table += f"<th>{name}</th>"
        html_table += "</tr>"

        # Add the data rows
        for row in range(table_widget.rowCount()):
            html_table += "<tr>"
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

        # Define the input and output file paths
        input_file = 'temp.html'
        output_file = 'temp.pdf'

        # Write the HTML table to a temporary file with the correct encoding
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(html_table)

        # Configure the path to wkhtmltopdf
        config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

        # Set the options for PDF generation
        options = {
            'page-size': 'A2',
            # 'margin-top': '0mm',
            # 'margin-right': '0mm',
            # 'margin-bottom': '0mm',
            # 'margin-left': '0mm',
            'encoding': 'UTF-8',  # Specify the encoding
            'no-outline': None,  # Show table borders
        }

        # Generate the PDF
        pdfkit.from_file(input_file, output_file, configuration=config, options=options)

        # Open a file dialog to select the output PDF file path
        filename, _ = QFileDialog.getSaveFileName(None, 'Save PDF Report', '', 'PDF Files (*.pdf)')
        if filename:
            try:
                # Move the temporary PDF file to the desired output location
                os.rename(output_file, filename)

                # Show a success message
                QMessageBox.information(self.ui, "نجاح", "تم حفظ التقرير PDF بنجاح!")
            except FileExistsError:
                # Show an error message if the destination file already exists
                QMessageBox.warning(self.ui, "Error", "الملف موجود بالفعل. الرجاء اختيار اسم ملف مختلف.")
        else:
            # Show a message if the user cancels the save dialog
            QMessageBox.warning(self.ui, "Error", "Save operation canceled.")

        # Delete the temporary HTML and PDF files
        os.remove(input_file)

        print('PDF generated successfully.')

        # else:
        #     QMessageBox.information(self.ui, "الصلاحية", "ليس لديك بيانات لتصديرها")
    ### إذا كان الملف موجودًا بالفعل، فإنه يقوم بإلحاق عداد باسم الملف
    # # Generate the PDF
    # pdfkit.from_file(input_file, output_file, configuration=config, options=options)
    #
    # # Open a file dialog to select the output PDF file path
    # filename, _ = QFileDialog.getSaveFileName(None, 'Save PDF Report', '', 'PDF Files (*.pdf)')
    #
    # if filename:
    #     # Rename the file if it already exists
    #     new_filename = filename
    #     counter = 1
    #     while os.path.exists(new_filename):
    #         file_name, file_extension = os.path.splitext(filename)
    #         new_filename = f'{file_name}_{counter}{file_extension}'
    #         counter += 1
    #
    #     # Move the temporary PDF file to the desired output location
    #     os.rename(output_file, new_filename)
    #
    #     # Delete the temporary HTML file
    #     os.remove(input_file)
    #
    #     # Show a success message
    #     QMessageBox.information(self.ui, "Success", "تم حفظ تقرير PDF بنجاح!")
    # else:
    #     # Show a message if the user cancels the save dialog
    #     QMessageBox.warning(None, "Error", "Save operation canceled.")
    #
    # print('PDF generated successfully.')
