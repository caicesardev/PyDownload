import sys

from gui.ui_History import Ui_History

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QLibraryInfo, QLocale, QTranslator
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QMessageBox


class History(QMainWindow, Ui_History):
    def __init__(self):
        super(History, self).__init__()

        self.setupUi(self)

        self.search_downloads()

        if self.downloads_count <= 0:
            VBox = QVBoxLayout()
            VBox.setAlignment(Qt.AlignCenter)
            image = QLabel()
            image.setPixmap(QPixmap("../res/images/location_search.png"))
            image.setScaledContents(True)
            image.setMaximumWidth(700)
            image.setMaximumHeight(480)
            VBox.addWidget(image)
            no_downloads_history = QLabel()
            no_downloads_history.setText(
                "No hay ninguna descarga registrada en el historial de descargas.")
            no_downloads_history.setAlignment(Qt.AlignCenter)
            no_downloads_history.setFont("Araboto Normal")
            no_downloads_history.setStyleSheet("""
            font-size: 16px;
            color: darkblue;""")
            VBox.addWidget(no_downloads_history)
            self.history_content_widget.setLayout(VBox)

        self.accept_button.clicked.connect(self.close)
        self.clean_button.clicked.connect(self.clean_history)

    def search_downloads(self):
        self.downloads_count = 0

    def clean_history(self):
        answer = QMessageBox.question(self, "PyDownload | Limpiar Historial",
                                      "¿Está seguro de que desea limpiar el historial?")
        if answer == QMessageBox.Yes:
            print("Limpiando historial...")


def main():
    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load("qtbase_" + QLocale.system().name(),
                    QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)

    gui = History()
    gui.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
