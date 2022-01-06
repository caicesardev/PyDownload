import sys

from gui.ui_Manager import Ui_Manager

from pytube import YouTube
import time
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import (
    Qt,
    QSettings,
    QRect,
    QSize,
    QThread,
    Signal)
from PySide6.QtWidgets import (
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


# Worker class.
class ThreadClass(QThread):
    finished = Signal()
    file_title_label = Signal(str)
    file_type_label = Signal(str)
    download_type_image = Signal(QPixmap)
    download_progress_bar = Signal(int)
    file_size_label = Signal(str)
    total_downloaded_label = Signal(str)
    estimated_time_label = Signal(str)

    def __init__(self, url, index):
        super(ThreadClass, self).__init__()

        self.is_running = True
        self.url = url
        self.index = index

        self.get_required_settings()

    def run(self):

        self.yt = YouTube(self.url)

        # Try to filter, if there is no match get the highest resolution.
        try:
            self.stream = self.yt.streams.filter(
                file_extension=self.preferred_video_format,
                resolution=self.preferred_video_quality,
                progressive=True,
            ).first()
            self.file_title_label.emit(str(self.yt.title))
            self.file_type_label.emit(str(self.preferred_video_format))
            self.download_type_image.emit(
                QPixmap(u"../res/images/youtube.png"))
            self.download_progress_bar.emit(0)
            self.file_size_label.emit(str(self.stream.filesize // 120))
            self.total_downloaded_label.emit("25MB/413MB")
            self.estimated_time_label.emit("Tiempo estimado: 10 Minutos")
        except Exception:
            self.stream = self.yt.streams.get_highest_resolution()
            self.file_title_label.emit(str(self.yt.title))
            self.file_type_label.emit(str(self.preferred_video_format))
            self.download_type_image.emit(
                str(u"../res/images/youtube.png"))
            self.download_progress_bar.emit(50)
            self.file_size_label.emit(str(self.stream.filesize // 120))
            self.total_downloaded_label.emit("25MB/413MB")
            self.estimated_time_label.emit("Tiempo estimado: 10 Minutos")

    def stop(self):
        self.is_running = False
        print(f"Stopping thread number: {self.index}")
        self.terminate()

    def get_required_settings(self):
        self.preferences = QSettings("PyDownload", "Preferences")
        self.downloads = QSettings("PyDownload", "Downloads")

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


# Manager.
class Manager(QMainWindow, Ui_Manager):
    def __init__(self, v_list, a_list):
        """[summary]
        Args:
            v_list ([list]): [List of video urls to be downloaded.]
            a_list ([list]): [List of audio urls to be downloaded.]
        """
        super(Manager, self).__init__()

        self.setupUi(self)

        self.v_list = v_list
        self.a_list = a_list

        self.thread = {}

        # Get user settings.
        self.get_settings()

        # If there are downloads in the list:
        if len(self.v_list) > 0 or len(self.a_list) > 0:
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
        i = 0
        for v_url in self.v_list:
            i += 1
            self.create_download_frame(v_url, i)

        for a_url in self.a_list:
            i += 1
            self.create_download_frame(a_url, i)

    def create_download_frame(self, url, i):
        print(f"Working with download number {i} url: {url}")
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

        # Create a QThread object.
        print("Create a QThread object.")
        self.thread[i] = ThreadClass(url, i)
        # Start the thread.
        print("Starting the thread.")
        self.thread[i].start()

        # File Title Label.
        self.thread[i].file_title_label.connect(
            self.update_file_title_label_event)

        # File Type Label.
        self.thread[i].file_type_label.connect(
            self.update_file_type_label_event)

        # Download Type Image.
        self.thread[i].download_type_image.connect(
            self.update_download_type_image_event)

        # Download Progress Bar.
        self.thread[i].download_progress_bar.connect(
            self.update_download_progress_bar_event)

        # File Size Label.
        self.thread[i].file_size_label.connect(
            self.update_file_size_label_event)

        # Total Downloaded Label.
        self.thread[i].total_downloaded_label.connect(
            self.update_total_downloaded_label_event)

        # Estimated Time Label.
        self.thread[i].estimated_time_label.connect(
            self.update_estimated_time_label_event)

        self.play_tool_button.clicked.connect(self.thread[i].run)
        self.pause_tool_button.clicked.connect(self.thread[i].stop)
        self.cancel_tool_button.clicked.connect(self.thread[i].terminate)

    # >- EVENTS -<
    def update_file_title_label_event(self, txt):
        self.file_title_label.setText(txt)

    def update_file_type_label_event(self, txt):
        self.file_type_label.setText(txt)

    def update_download_type_image_event(self, path):
        self.download_type_image.setPixmap(path)

    def update_download_progress_bar_event(self, n):
        self.download_progress_bar.setValue(n)

    def update_file_size_label_event(self, txt):
        self.file_size_label.setText(f"{str(txt)}MB")

    def update_total_downloaded_label_event(self, txt):
        self.total_downloaded_label.setText(str(txt))

    def update_estimated_time_label_event(self, txt):
        self.estimated_time_label.setText(str(txt))
    # >- EVENTS -<

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
        if len(self.v_list) > 0 and len(self.a_list) > 0:
            answer = QMessageBox.question(self, "PyDownload | Cancelar descargas",
                                          "¿Está seguro de que desea cancelar todas las descargas?")
            if answer == QMessageBox.Yes:
                print("Cancelando todas las descargas...")
                # for i in self.worker:
                #     worker[i].deleteLater()
