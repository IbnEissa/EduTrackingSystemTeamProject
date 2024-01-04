from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QApplication, QStackedWidget


class DialogManager:
    def __init__(self):
        self.dialog_stack = []
        self.stacked_widget = QStackedWidget()

    def push_dialog(self, dialog):
        self.dialog_stack.append(dialog)
        self.stacked_widget.addWidget(dialog)
        self.stacked_widget.setCurrentWidget(dialog)

    def pop_dialog(self):
        if self.dialog_stack:
            self.dialog_stack.pop()
            self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
            if self.dialog_stack:
                self.stacked_widget.setCurrentWidget(self.dialog_stack[-1])

    def show_current_dialog(self):
        self.stacked_widget.show()
