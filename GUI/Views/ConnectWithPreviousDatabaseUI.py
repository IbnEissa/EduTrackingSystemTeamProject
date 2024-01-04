from PyQt5.QtWidgets import QMessageBox, QApplication

from GUI.Dialogs.InitializingTheProject.CreateDataBaseDialog import CreateDataBaseDialog

app = QApplication([])


class ConnectWithPreviousDatabaseUI:
    def __init__(self, submain_instance):
        self.submain = submain_instance
        self.ui = self.submain.ui

    def use_ui_elements(self):
        self.ui.btnShowPreviousDataBases.clicked.connect(self.connect_with_database)

    #
    def connect_with_database(self):
        connection_data_base = CreateDataBaseDialog()
        connection_data_base.combDataBaseInitialize.setEditable(False)
        connection_data_base.btnCreateDataBase.hide()
        connection_data_base.checkShowDatabaseExists.show()
        connection_data_base.btnConnectoinDataBase.show()
        connection_data_base.btnCancelConnectDatabase.show()
        connection_data_base.use_ui_elements()
        connection_data_base.exec_()

