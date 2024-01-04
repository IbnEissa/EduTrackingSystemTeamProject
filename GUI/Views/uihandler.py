from PyQt5.uic import loadUi


class UIHandler:
    def __init__(self, ui_file):
        self.ui = loadUi(ui_file)

    def get_ui(self):
        return self.ui
