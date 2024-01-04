from PyQt5.QtWidgets import QMessageBox


class LoginState:

    def show_user_details_tab(self, selected_option):

        if selected_option == 'تسجيل الخروج':
            Main(1, False)
        if selected_option == 'الحساب':
            QMessageBox.information(self, 'تحذير', 'لم يتم اضافة الواجهه بعد')
