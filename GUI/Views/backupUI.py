import datetime
import os
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QWidget


class Backup_UI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui
        self.backup_file = ""
        self.parent_widget = QWidget()

    def use_ui_elements(self):
        self.ui.btnBackup.clicked.connect(self.create_backup)
        self.ui.btnRestoreBackup.clicked.connect(self.restore_backup)

    def open_dailogfile(self):
        self.file_dialog = QFileDialog(self.parent_widget)
        self.file_dialog.setAcceptMode(QFileDialog.AcceptOpen)
        self.file_dialog.setNameFilter("SQL Files (*.sql)")
        self.file_dialog.fileSelected.connect(self.backup_file_selected)
        self.file_dialog.exec_()

    def backup_file_selected(self, file):
        self.backup_file = file

    def restore_backup(self):
        self.open_dailogfile()
        if not self.backup_file:
            QMessageBox.warning(self.parent_widget, "Backup File Not Selected", "Please select a backup file.")
            return

        confirmation = QMessageBox.question(self.parent_widget, "Confirm Restore",
                                            "Are you sure you want to restore the backup?")
        if confirmation == QMessageBox.Yes:
            command = f"mysql -u root -h localhost -P 3306  edutrackingsystemdb2 < {self.backup_file}"
            os.system(command)
            QMessageBox.information(self.parent_widget, "Restore Completed", "Backup restored successfully.")

    def create_backup(self):
        backup_folder = r"C:\Users\User15\Desktop\aws"
        backup_file = os.path.join(backup_folder, f"backup_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql")

        command = f"mysqldump -u root -h localhost -P 3306 --databases edutrackingsystemdb2 > {backup_file}"
        os.system(command)

        if os.path.exists(backup_file):
            QMessageBox.information(self.parent_widget, "Backup Created", f"تم انشاء النسخة الاحتياطية بنجاح{backup_folder}")
        else:
            QMessageBox.warning(self.parent_widget, "Backup Error", "حدث خطأ اثناء النسخ الاحتياطي")
