import sys
from PySide6.QtWidgets import QPushButton, QApplication, QLineEdit, QWidget, QDialog, QMessageBox, QLineEdit


class NewWidget(QDialog):
    def __init__(self, parent=None):
        super(NewWidget, self).__init__(parent)

        self.lineEdit = QLineEdit('new window', self)
        self.resize(200, 50)
        self.show()

    def closeEvent(self, ev):

        self.Exit = QMessageBox.question(self,
                                         "Confirm Exit...",
                                         "Are you sure you want to exit ?",
                                         QMessageBox.Yes | QMessageBox.No)
        ev.ignore()

        if self.Exit == QMessageBox.Yes:
            ev.accept()


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        self.button = QPushButton("button", self)
        self.button.clicked.connect(self.open_new)
        self._subwindow = None

    def open_new(self):
        if self._subwindow is None:
            self._subwindow = NewWidget(self)
            self._subwindow.resize(200, 50)
            # move it next to the main window
            pos = self.frameGeometry().topLeft()
            self._subwindow.move(pos.x() - 250, pos.y())
        self._subwindow.show()
        self._subwindow.activateWindow()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    main = MainWidget()
    main.resize(200, 50)
    main.show()
    sys.exit(app.exec_())
