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


# Worker Class.
class Worker(QObject,):
    progress = Signal(int)
    stop = Signal()
    finished = Signal()

    def __init__(self, url, download_path, video_quality, video_format) -> None:
        super(Worker).__init__()

        self.url = url
        self.download_path = download_path
        self.video_format = video_format
        self.video_quality = video_quality

        print(f"URL FROM WORKER IS: {self.url}")

    def run(self):
        self.d_video = YouTube(
            self.url, on_progress_callback=self.download_callback)
        self.stream = self.d_video.streams.filter(
            file_extension=f"{self.video_format}",
            resolution=f"{self.video_quality}",
            progressive=True,
        ).first()

        self.stream.download(self.download_path)

    # Download callback.
    def download_callback(self, stream, chunk, bytes_remaining):
        self.progress.emit(
            round((1-bytes_remaining/self.yv.filesize) * 100, 3))
        print(
            round((1-bytes_remaining/self.yv.filesize) * 100, 3), '% done...')


# Manager.
class Manager(QMainWindow, Ui_Manager):
    def __init__(self, url):
        super(Manager, self).__init__()

        self.setupUi(self)

        self.url = url

        # Get user settings.
        self.get_settings()

        # Fetch downloads.
        self.search_downloads()

        # If there are no downloads in the list:
        if len(self.video_urls) <= 0:
            print("No downloads.")
            self.no_downloads()
        # If there are downloads in the list:
        else:
            print("Downloads")
            self.show_downloads()

        # GUI Buttons.
        self.accept_button.clicked.connect(self.close)
        self.resume_all_button.clicked.connect(self.resume_all)
        self.stop_all_button.clicked.connect(self.stop_all)
        self.cancel_all_button.clicked.connect(self.cancel_all)

    def search_downloads(self):
        self.video_urls = []
        self.video_urls.append(self.url)
        self.change_status(
            f"Actualmente hay {len(self.video_urls)} descarga/s en curso.", "darkgreen")

    def show_downloads(self):
        for i in range(len(self.video_urls)):
            self.d_video = YouTube(
                self.url)

            print(f"Download Video: {self.d_video.title}")

            # Try filtering by user preferences.
            try:
                print("Trying")
                self.stream = self.d_video.streams.filter(
                    file_extension=f"{self.formats[self.preferred_video_format]}",
                    resolution=f"{self.resolutions[self.preferred_video_quality]}",
                    progressive=False,
                ).first()
            # If no stream matches user preferences then get the highest resolution.
            except:
                print("Exception try")
                self.stream = self.d_video.streams.get_highest_resolution()

            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker(
                self.url, self.preferred_video_quality, self.preferred_video_format)
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.run)

            self.worker.finished.connect(self.download_finished)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            # Step 6: Start the thread
            self.thread.start()

            # region
            #################### GUI DECLARATION ####################
            self.download_frame = QFrame(self.manager_content_widget)
            self.download_frame.setObjectName(u"download_frame")
            self.verticalLayout_5 = QVBoxLayout(self.download_frame)
            self.verticalLayout_5.setObjectName(u"verticalLayout_5")
            self.head_frame = QFrame(self.download_frame)
            self.head_frame.setObjectName(u"head_frame")
            self.horizontalLayout_3 = QHBoxLayout(self.head_frame)
            self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
            self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
            self.file_title_label = QLabel(self.head_frame)
            self.file_title_label.setObjectName(u"file_title_label")
            font1 = QFont()
            font1.setBold(True)
            self.file_title_label.setFont(font1)
            self.horizontalLayout_3.addWidget(self.file_title_label)
            self.horizontal_spacer = QSpacerItem(
                40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
            self.horizontalLayout_3.addItem(self.horizontal_spacer)
            self.file_type_label = QLabel(self.head_frame)
            self.file_type_label.setObjectName(u"file_type_label")
            font2 = QFont()
            font2.setPointSize(10)
            font2.setBold(False)
            self.file_type_label.setFont(font2)
            self.horizontalLayout_3.addWidget(self.file_type_label)
            self.file_size_label = QLabel(self.head_frame)
            self.file_size_label.setObjectName(u"file_size_label")
            font3 = QFont()
            font3.setPointSize(10)
            self.file_size_label.setFont(font3)
            self.horizontalLayout_3.addWidget(self.file_size_label)
            self.verticalLayout_5.addWidget(self.head_frame)
            self.line = QFrame(self.download_frame)
            self.line.setObjectName(u"line")
            self.line.setStyleSheet(u"background-color: darkgreen;\n"
                                    "margin-left: 15px;\n"
                                    "margin-right: 10px;")
            self.line.setFrameShape(QFrame.HLine)
            self.line.setFrameShadow(QFrame.Sunken)
            self.verticalLayout_5.addWidget(self.line)
            self.mid_frame = QFrame(self.download_frame)
            self.mid_frame.setObjectName(u"mid_frame")
            self.horizontalLayout_6 = QHBoxLayout(self.mid_frame)
            self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
            self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 0)
            self.download_type_image = QLabel(self.mid_frame)
            self.download_type_image.setObjectName(u"download_type_image")
            self.download_type_image.setMaximumSize(QSize(32, 32))
            self.download_type_image.setScaledContents(True)
            self.horizontalLayout_6.addWidget(self.download_type_image)
            self.download_progress_bar = QProgressBar(self.mid_frame)
            self.download_progress_bar.setObjectName(
                u"download_progress_bar")
            self.horizontalLayout_6.addWidget(self.download_progress_bar)
            self.play_tool_button = QToolButton(self.mid_frame)
            self.play_tool_button.setObjectName(u"play_tool_button")
            icon = QIcon()
            icon.addFile(u"../res/images/play.png",
                         QSize(), QIcon.Normal, QIcon.Off)
            self.play_tool_button.setIcon(icon)
            self.play_tool_button.setIconSize(QSize(24, 24))
            self.play_tool_button.setToolTip("Continuar la descarga")
            self.horizontalLayout_6.addWidget(self.play_tool_button)
            self.pause_tool_button = QToolButton(self.mid_frame)
            self.pause_tool_button.setObjectName(u"pause_tool_button")
            icon1 = QIcon()
            icon1.addFile(u"../res/images/pause.png",
                          QSize(), QIcon.Normal, QIcon.Off)
            self.pause_tool_button.setIcon(icon1)
            self.pause_tool_button.setIconSize(QSize(24, 24))
            self.pause_tool_button.setToolTip("Pausar la descarga")
            self.horizontalLayout_6.addWidget(self.pause_tool_button)
            self.cancel_tool_button = QToolButton(self.mid_frame)
            self.cancel_tool_button.setObjectName(u"cancel_tool_button")
            icon2 = QIcon()
            icon2.addFile(u"../res/images/cancel.png",
                          QSize(), QIcon.Normal, QIcon.Off)
            self.cancel_tool_button.setIcon(icon2)
            self.cancel_tool_button.setIconSize(QSize(24, 24))
            self.cancel_tool_button.setToolTip("Cancelar la descarga")
            self.horizontalLayout_6.addWidget(self.cancel_tool_button)
            self.verticalLayout_5.addWidget(self.mid_frame)
            self.bottom_frame = QFrame(self.download_frame)
            self.bottom_frame.setObjectName(u"bottom_frame")
            self.horizontalLayout_9 = QHBoxLayout(self.bottom_frame)
            self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
            self.total_downloaded_label = QLabel(self.bottom_frame)
            self.total_downloaded_label.setObjectName(
                u"total_downloaded_label")
            self.total_downloaded_label.setFont(font3)
            self.horizontalLayout_9.addWidget(self.total_downloaded_label)
            self.estimated_time_label = QLabel(self.bottom_frame)
            self.estimated_time_label.setObjectName(
                u"estimated_time_label")
            self.estimated_time_label.setFont(font3)
            self.estimated_time_label.setAlignment(
                Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
            self.horizontalLayout_9.addWidget(self.estimated_time_label)
            self.verticalLayout_5.addWidget(self.bottom_frame)
            self.verticalLayout_4.addWidget(self.download_frame)
            self.verticalSpacer = QSpacerItem(
                20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.verticalLayout_4.addItem(self.verticalSpacer)
            #################### GUI DECLARATION ####################
            # endregion

            # File name.
            self.file_title_label.setText(
                f"{self.d_video.title}")
            # File type.
            self.file_type_label.setText(
                str(f"{self.formats[self.preferred_video_format]}"))
            # If file is type video set youtube.png as image. <- Not implemented yet.
            self.download_type_image.setPixmap(
                QPixmap(u"../res/images/youtube.png"))
            # Progress bar.
            self.worker.progress.connect(self.reportProgress)
            # File size.
            self.file_size_label.setText(f"{self.stream.filesize}MB")
            # Total downloaded.
            self.total_downloaded_label.setText(
                f"Descargados: 72MB / {self.stream.filesize}MB")
            # Estimated time.
            self.estimated_time_label.setText("Tiempo estimado: 10m")

            self.play_tool_button.clicked.connect(self.worker.run)
            self.pause_tool_button.clicked.connect(self.worker.stop)
            self.cancel_tool_button.clicked.connect(self.worker.deleteLater)

    def report_progress(self, n):
        self.download_progress_bar.setValue(n)

    def download_finished(self):
        self.download_frame.setParent(None)
        self.video_urls.clear()
        QMessageBox.information(
            self, "PyDownload | Éxito", f"""El vídeo "{self.d_video.title}" se ha descargado exitosamente en "{self.download_path}". """)

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
        if len(self.video_urls) > 0:
            answer = QMessageBox.question(self, "PyDownload | Cancelar descargas",
                                          "¿Está seguro de que desea cancelar todas las descargas?")
            if answer == QMessageBox.Yes:
                print("Cancelando todas las descargas...")
                # for i in self.worker:
                #     worker[i].deleteLater()

    # Had to manually create these GUIs.
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

    def get_settings(self):
        # Get registry values.
        self.theme = QSettings("PyDownload", "Theme")
        self.downloads = QSettings("PyDownload", "Downloads")
        self.preferences = QSettings("PyDownload", "Preferences")
        self.languages = QSettings("PyDownload", "Languages")

        self.download_path = self.downloads.value("downloads-path")
        self.preferred_video_quality = self.preferences.value(
            "preferred-video-quality")
        self.preferred_video_format = self.preferences.value(
            "preferred-video-format")

        self.formats = {1: "mp4", 2: "3gpp", 3: "webm"}
        self.resolutions = {1: "144p", 2: "360p", 3: "480p",
                            4: "720p", 5: "1080p", 6: "1440p", 7: "2160p"}

    # Change text of the status label.

    def change_status(self, text, color):
        if color == "default" or color == "Default":
            self.status_label.setText(text)
        else:
            self.status_label.setText(text)
            self.status_label.setStyleSheet(
                "QLabel{ color: %s; }" % color)


def main():
    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load("qtbase_" + QLocale.system().name(),
                    QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)

    gui = Manager()
    gui.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
