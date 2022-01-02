import sys

from gui.ui_Manager import Ui_Manager

from pytube import YouTube
import time
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import (
    Qt,
    QObject,
    QSettings,
    QLibraryInfo,
    QRect,
    QSize,
    QLocale,
    QTranslator,
    QThread,
    Signal)
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QFrame,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QProgressBar,
    QToolButton,
    QScrollArea,
    QWidget)


# Manager.
class Manager(QMainWindow, Ui_Manager):
    def __init__(self, u_list):
        super(Manager, self).__init__()

        self.setupUi(self)

        self.urls = u_list

        # Get user settings.
        self.get_settings()

        # Fetch downloads. Creates a list (urls_list)
        self.search_downloads()

        # If there are downloads in the list:
        if len(self.urls_list) > 0:
            self.show_downloads()
        # If there are no downloads in the list:
        else:
            self.no_downloads()

        # GUI Buttons.
        self.accept_button.clicked.connect(self.close)
        self.resume_all_button.clicked.connect(self.resume_all)
        self.stop_all_button.clicked.connect(self.stop_all)
        self.cancel_all_button.clicked.connect(self.cancel_all)

    def get_settings(self):
        # Get registry values.
        self.theme = QSettings("PyDownload", "Theme")
        self.downloads = QSettings("PyDownload", "Downloads")
        self.preferences = QSettings("PyDownload", "Preferences")
        self.languages = QSettings("PyDownload", "Languages")

        self.formats = {1: "mp4", 2: "3gpp", 3: "webm"}
        self.resolutions = {1: "144p", 2: "360p", 3: "480p",
                            4: "720p", 5: "1080p", 6: "1440p", 7: "2160p"}
        self.frequencies = {"1": "48kbps", "2": "50kbps",
                            "3": "70kbps", "4": "128kbps", "5": "160kbps"}

        self.download_path = self.downloads.value("downloads-path")
        self.preferred_video_format = self.formats[self.preferences.value(
            "preferred-video-format")]
        self.preferred_video_quality = self.resolutions[self.preferences.value(
            "preferred-video-quality")]

    def search_downloads(self):
        self.urls_list = []
        if self.url is not "":
            self.urls_list.append(self.url)

    def no_downloads(self):
        self.verticalLayout_3.takeAt(0)
        self.manager_scroll_area = QScrollArea(self.manager_frame)
        self.manager_scroll_area.setObjectName(u"manager_scroll_area")
        self.manager_scroll_area.setStyleSheet(u"QScrollArea#manager_scroll_area{\n"
                                               "	background: #F0F0F0;\n"
                                               "	border-radius: 20px;\n"
                                               "	padding: 5px;\n"
                                               "}")
        self.manager_scroll_area.setFrameShape(QFrame.NoFrame)
        self.manager_scroll_area.setWidgetResizable(True)
        self.manager_content_widget = QWidget()
        self.manager_content_widget.setObjectName(
            u"manager_content_widget")
        self.manager_content_widget.setGeometry(QRect(0, 0, 942, 547))
        self.manager_scroll_area.setWidget(self.manager_content_widget)
        self.verticalLayout_3.addWidget(self.manager_scroll_area)
        VBox = QVBoxLayout()
        VBox.setAlignment(Qt.AlignCenter)
        image = QLabel()
        image.setPixmap(QPixmap("../res/images/location_search.png"))
        image.setScaledContents(True)
        image.setMaximumWidth(700)
        image.setMaximumHeight(480)
        VBox.addWidget(image)
        no_downloads_label = QLabel()
        no_downloads_label.setText(
            "No hay ninguna descarga en curso en este momento.")
        no_downloads_label.setAlignment(Qt.AlignCenter)
        no_downloads_label.setFont("Araboto Normal")
        no_downloads_label.setStyleSheet("""
            font-size: 16px;
            color: darkblue;""")
        VBox.addWidget(no_downloads_label)
        self.manager_content_widget.setLayout(VBox)

    def show_downloads(self):
        print(self.urls_list)

    def resume_all(self):
        # You can only resume all downloads if there are any present.
        print("Cancelando todas las descargas...")
        # for i in self.worker:
        #     worker[i].run()

    def stop_all(self):
        # You can only stop all downloads if there are any present.
        print("Pausando todas las descargas...")
        # for i in self.worker:
        #     worker[i].stop()

    def cancel_all(self):
        # You can only cancel all downloads if there are any present.
        if len(self.urls_list) > 0:
            answer = QMessageBox.question(self, "PyDownload | Cancelar descargas",
                                          "¿Está seguro de que desea cancelar todas las descargas?")
            if answer == QMessageBox.Yes:
                print("Cancelando todas las descargas...")
                # for i in self.worker:
                #     worker[i].deleteLater()
