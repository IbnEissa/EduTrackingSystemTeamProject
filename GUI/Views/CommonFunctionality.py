import sys

import peewee
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView, QMessageBox, QApplication, QAbstractItemView

from GUI.Dialogs.UserLoginDialog import UserLoginDialog
from models.Permissions import Permissions
from models.School import School
from models.Users import Users


class Common:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        lastInsertedSchoolId = 0
        self.ui = self.submain.ui
        # self.make_school_name()
        self.make_user_name()
        # self.connect_device()
        self.state = None
        self.ip = None
        self.port = None


    def use_ui_elements(self):
        self.ui.btnMainTeachers.clicked.connect(self.teachers_button_clicked)
        self.ui.btnMainStudents.clicked.connect(self.students_button_clicked)
        self.ui.btnMainTeachersSchedual.clicked.connect(self.teachers_schedual_button_clicked)
        self.ui.btnShiftsHome.clicked.connect(self.shifts_button_clicked)
        # self.ui.btnArchive.clicked.connect(self.archive_button_clicked)
        # self.ui.btnSettings.clicked.connect(self.settings_button_clicked)
        self.ui.tabMainTab.setCurrentIndex(0)
        self.ui.tabMainTab.tabBar().setVisible(False)
        self.ui.tabEmpsMovement.tabBar().setVisible(False)
        self.ui.tabSettings.tabBar().setVisible(False)
        self.ui.tabDataManagement.tabBar().setVisible(False)
        self.ui.tabTeachersReports.tabBar().setVisible(False)
        self.ui.tabMainTab.setCurrentIndex(0)
        # self.ui.setWindowFlags(self.ui.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.ui.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint)

    # def connect_device(self):
    #     rowsCount = self.ui.tblDiveceData.rowCount()
    #     for row in range(rowsCount):
    #         state = self.ui.tblDiveceData.item(row, 4)
    #         ip = self.ui.tblDiveceData.item(row, 2)
    #         port = self.ui.tblDiveceData.item(row, 3)
    #         print("the state is : ", state.text())
    #         if state.text() == 'متصل الان':
    #             device_state = True
    #             device_ip = ip.text()
    #             device_port = port.text()
    #             return device_state, device_ip, device_port
    #         else:
    #             device_state = False
    #             device_ip = None
    #             device_port = None
    #             return device_state, device_ip, device_port

    def return_data(self):
        state = self.state
        ip = self.ip
        port = self.port
        return state, ip, port

    def home_button_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(0)

    def students_button_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(1)
        self.ui.tabDataManagement.setCurrentIndex(1)

    def teachers_schedual_button_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(1)
        self.ui.tabDataManagement.setCurrentIndex(2)

    def shifts_button_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(4)
        self.ui.tabSettings.setCurrentIndex(5)

    def teachers_button_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(1)
        self.ui.tabDataManagement.setCurrentIndex(0)

    def make_user_name(self):
        self.ui.btnUserDetails.setText(Users.get_name_with_true_state())

    def settings_button_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(4)
        self.ui.tabSettings.setCurrentIndex(0)

    def update_state_to_false(self):
        Users.update_all_states_to_false()
        self.ui.close()
        user_login = UserLoginDialog()
        user_login.use_ui_elements()
        user_login.exec_()
        result = user_login.login()
        if result is True:
            app = QApplication(sys.argv)
            sys.exit(app.exec_())

    # def grant_permission_tab_to_user(self, permission, tab):
    #     name = Users.get_name_with_true_state()
    #     print("grant permission tab to ", name)
    #     user = Users.get(Users.userName == name)
    #     permissions = (
    #         Permissions.select()
    #         .join(Users, on=(Permissions.users_id == Users.id))
    #         .where(Users.id == user.id)
    #         .get()
    #     )
    #     print(permission)
    #     if getattr(permissions, permission) == True:
    #         tab.show()
    #     else:
    #
    #         # tab.hide()
    #         QMessageBox.information(self.ui, "الصلاحية", "ليس لديك الصلاحية")

    def grant_permission_to_clicked_button(self, permission):
        name = Users.get_name_with_true_state()
        print("grant permission button to ", name)
        # selected_user = "moh"  # Replace with your logic to get the selected user
        user = Users.get(Users.Name == name)
        permissions = (
            Permissions.select()
            .join(Users, on=(Permissions.users_id == Users.id))
            .where(Users.id == user.id)
            .get()
        )
        print(permission)
        if getattr(permissions, permission) == True:
            return True
        else:
            return False

    def btn_management_clicked(self):
        self.ui.tabMainTab.setCurrentIndex(1)
        self.ui.tabDataManagement.setCurrentIndex(0)

    def btn_emp_movement(self):
        self.ui.tabMainTab.setCurrentIndex(2)
        self.ui.tabEmpsMovement.setCurrentIndex(0)

    def get_subjects(self):
        subjects = ["الرياضيات",
                    "العلوم",
                    "اللغة العربية",
                    "اللغة الإنجليزية",
                    "التاريخ",
                    "الجغرافيا",
                    "الفيزياء",
                    "الكيمياء",
                    "الأحياء",
                    "القران الكريم",
                    "التربية الوطنية",
                    "التربية الاسلامية",
                    "الاجتماعيات"
                    ]
        return subjects

    def get_classes(self):
        classes = ["الاول",
                   "الثاني",
                   "الثالث",
                   "الرابع",
                   "الخامس",
                   "السادس",
                   "السابع",
                   "الثامن",
                   "التاسع",
                   "الاول الثانوي",
                   "الثاني الثانوي",
                   "الثالث الثانوي",

                   ]
        return classes

    def get_days(self):
        days = ["السبت",
                "الاحد",
                "الاثنين",
                "الثلاثاء",
                "الاربعاء",
                "الخميس",
                ]
        return days

    def get_sessions(self):
        sessions = ["الاولى",
                    "الثانية",
                    "الثالثة",
                    "الرابعة",
                    "الخامسة",
                    "السادسة",
                    "السابعة",

                    ]
        return sessions

    def get_combo_box_data(self, table_model, column_name, where_clause=None):
        query = table_model.select(getattr(table_model, column_name)).distinct()
        print(f"The where clause is: {where_clause}")
        if where_clause is not None:
            query = query.where(where_clause)
        items = []
        for data in query:
            item_value = getattr(data, column_name)
            items.append(str(item_value))
        return items

    def get_cities(self):
        cities = {
            "صنعاء": [
                "أمانة العاصمة",
                "أرحب",
                "الطيال",
                "بني ضبيان",
                "صعفان",
                "الحصن",
                "بلاد الروس",
                "جحانة",
                "مناخة",
                "الحيمة الخارجية",
                "بني حشيش",
                "خولان",
                "نهم",
                "الحيمة الداخلية",
                "بني مطر",
                "سنحان وبني بهلول",
                "همدان"
            ],
            "عدن": [
                "خور مكسر",
                "صيرة",
                "المعلا",
                "التواهي",
                "البريقة",
                "المنصورة",
                "الشيخ عثمان",
                "دارس سعد"
            ],
            "المحويت": [
                "شبام كوكبان",
                "الطويلة",
                "الرجم",
                "الخبت",
                "ملحان",
                "حفاش",
                "بني سعد",
                "مدينة المحويت",
                "المحويت"
            ],
            "ذمار": [
                "الحداء",
                "جهران",
                "جبل الشرق",
                "مغرب عنس",
                "عتمة",
                "وصاب العالي",
                "وصاب السافل",
                "مدينة ذمار",
                "ميفعة عنس",
                "عنس",
                "ضوران أنس",
                "المنار"
            ],
            "الجوف": [
                "الخب والشعف",
                "الحميدات",
                "المطه",
                "الزاهر",
                "الحزم",
                "المتون",
                "المصلوب",
                "الغيل",
                "الخلق",
                "برط العنان",
                "رجوزه",
                "خراب المراشي"
            ], "عمران": [
                "السود",
                "السودة",
                "العشة",
                "المدان",
                "بني صريم",
                "ثلاء",
                "جبل عيال يزيد",
                "حرف سفيان",
                "حوث",
                "خارف",
                "ذيبين",
                "ريدة",
                "شهارة",
                "صوير",
                "ظليمة حبور",
                "عمران",
                "عيال سريح",
                "قفلة عذر",
                "مسور"
            ],
            "البيضاء": [
                "البيضاء",
                "الرياشيه",
                "الزاهر",
                "السواديه",
                "الشرية",
                "الصومعه",
                "الطفة",
                "العرش",
                "القريشيه",
                "الملاجم",
                "ذي ناعم",
                "رداع",
                "ردمان",
                "صباح",
                "البيضاء",
                "مسورة",
                "مكيراس",
                "ناطع",
                "نعمان",
                "ولد ربيع"
            ],
            "حضرموت": [
                "الديس",
                "الريدة وقصيعر",
                "السوم",
                "الشحر",
                "الضليعه",
                "العبر",
                "القطن",
                "القف",
                "المكلا",
                "بروم ميفع",
                "تريم",
                "ثمود",
                "حجر",
                "حجر الصيعر",
                "حديبو",
                "حريضة",
                "دوعن",
                "رخيه",
                "رماه",
                "زمنخ ومنوخ",
                "ساه",
                "سيئون",
                "شبام",
                "عمد",
                "غيل با وزير",
                "غيل بن يمين",
                "قلنسية وعبد الكوري",
                "المكلا",
                "وادي العين",
                "يبعث"
            ],
            "صعدة": [
                "باقم",
                "قطابر",
                "منبه",
                "غمر",
                "رازح",
                "شداء",
                "الظاهر",
                "حيدان",
                "ساقين",
                "مجز",
                "سحار",
                "الصفراء",
                "الحشوه",
                "كتاف والبقع",
                "صعده"
            ],
            "شبوة": [
                "دهر",
                "الطلح",
                "جردان",
                "عرماء",
                "عسيلان",
                "عين",
                "بيحان",
                "مرخه العليا",
                "مرخه السلفى",
                "نصاب",
                "حطيب",
                "الصعيد",
                "عتق",
                "حبان",
                "الروضه",
                "ميفعه",
                "رضوم"
            ],
            "لحج": [
                "الحد",
                "الحوطة",
                "القبيطة",
                "المسيمير",
                "المضاربة والعارة",
                "المفلحي",
                "المقاطرة",
                "الملاح",
                "تبن",
                "حالمين",
                "جبيل جبر",
                "ردفان",
                "طور الباحة",
                "يافع",
                "يهر"
            ],
            "أرخبيل سقطرى": [
                "حديبو",
                "قلنسية وعبد الكوري"
            ],
            "المهرة": [
                "شحن",
                "حات",
                "حوف",
                "الغيظة",
                "منعر",
                "المسيلة",
                "سيحوت",
                "قشن",
                "حصوين"
            ],
            "الضالع": [
                "الأزرق",
                "الحشاء",
                "الحصين",
                "الشعيب",
                "الضالع",
                "جبن",
                "جحاف",
                "دمت",
                "قعطبة"
            ],
            "أبين": [
                "زنجبار",
                "المحفد",
                "مودية",
                "جيشان",
                "لودر",
                "سباح",
                "رصد",
                "سرار",
                "أحور",
                "خنفر",
                "الوضيع"
            ],
            "ريمة": [
                "بلاد الطعام",
                "السلفية",
                "الجبين",
                "مزهر",
                "كسمة",
                "الجعفرية"
            ],
            "مأرب": [
                "الجوبة",
                "العبدية",
                "بدبدة",
                "جبل مراد",
                "حريب",
                "حريب القرامش",
                "رحبة",
                "رغوان",
                "صرواح",
                "مأرب",
                "ماهلية",
                "مجزر",
                "مدغل الجدعان"
            ],
            "إب": [
                "إب",
                "الرضمة",
                "السبرة",
                "السدة",
                "السياني",
                "الشعر",
                "الظهار",
                "العدين",
                "القفر",
                "المخادر",
                "المشنة",
                "النادرة",
                "بعدان",
                "جبلة",
                "حبيش",
                "حزم العدين",
                "ذي السفال",
                "فرع العدين",
                "مذيخرة",
                "يريم"
            ],
            "حجة": [
                "أسلم",
                "أفلح الشام",
                "أفلح اليمن",
                "الجميمة",
                "الشاهل",
                "الشغادرة",
                "المحابشة",
                "المغربة",
                "المفتاح",
                "بكيل المير",
                "بني العوام",
                "بني قيس الطور",
                "حجة",
                "حرض",
                "حيران",
                "خيران المحرق",
                "شرس",
                "عبس",
                "قارة",
                "قفل شمر",
                "كحلان الشرف",
                "وضرة",
                "كحلان عفار",
                "كشر",
                "كعيدنة",
                "مبين",
                "مدينة حجة",
                "مستباء",
                "ميدي",
                "نجرة",
                "وشحة"
            ],
            "تعز": [
                "التعزية",
                "جبل حبشي",
                "حيفان",
                "خدير",
                "ذباب",
                "سامع",
                "شرعب الرونة",
                "شرعب السلام",
                "الشمايتين",
                "صالة",
                "صبر الموادم",
                "الصلو",
                "القاهرة",
                "ماوية",
                "المخاء",
                "المسراخ",
                "مشرعة وحدنان",
                "المظفر",
                "المعافر",
                "مقبنة",
                "المواسط",
                "موزع",
                "الوازعية"
            ],
            "الحديدة": [
                "الزهرة",
                "اللحية",
                "كمران",
                "الصلي",
                "المنيرة",
                "القناوص",
                "الزيدية",
                "المغلا",
                "الضحى",
                "باجل",
                "الحجيلة",
                "برع",
                "المراوعة",
                "الدريهمي",
                "السخنة",
                "المنصورية",
                "بيت الفقيه",
                "جبل راس",
                "حيس",
                "الخوخة",
                "الحوك",
                "الميناء",
                "الحالي",
                "زبيد",
                "الجراحي",
                "التحيتا"
            ]
        }
        return cities

    def style_table_widget(self, table_widget):
        table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for row in range(table_widget.rowCount()):
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                if item is not None:
                    item.setTextAlignment(Qt.AlignCenter)
