import sys

from gui.ui_About import Ui_About

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtWidgets import QMainWindow, QApplication


class About(QMainWindow, Ui_About):
    def __init__(self):
        super(About, self).__init__()

        self.setupUi(self)

        self.accept_push_button.clicked.connect(self.close)


def main():
    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load("qtbase_" + QLocale.system().name(),
                    QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)

    gui = About()
    gui.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
