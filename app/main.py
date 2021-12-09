import sys
import os
import subprocess
import getpass

from pytube import YouTube

from gui.ui_MainWindow import Ui_MainWindow
from gui.ui_Manager import Ui_Manager
from gui.ui_History import Ui_History
from gui.ui_Settings import Ui_Settings
from gui.ui_About import Ui_About

from PySide6 import QtWebEngineWidgets
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt, QSize, QLibraryInfo, QLocale, QThread, QTranslator, QUrl, QSettings, Signal
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMessageBox,
    QMenu,
    QVBoxLayout,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QProgressBar,
    QToolButton)


class WorkerThread(QThread):
    update_labels = Signal()
    search_video = Signal()

    def __init__(self, thread=0):
        super(WorkerThread, self).__init__()

        self.thread = thread
        self.is_running = True

    def run(self):
        self.search_video.emit()
        self.update_labels.emit()

    def stop(self):
        self.is_running = False
        self.terminate()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        # Get user configuration.
        self.get_configuration()

        # Window Variables.
        self.valid_url = False
        self.showing_preview = False
        self.worker = {}

        # Create a QVBoxLayout.
        self.vbox = QVBoxLayout()
        # Create a QWebEngineView instance.
        self.webview = QtWebEngineWidgets.QWebEngineView()
        # Add the QWebEngineView instance to layout.
        self.vbox.addWidget(self.webview)
        # Set the layout to the video_preview_widget.
        self.video_preview_widget.setLayout(self.vbox)

        # Download Button Menu.
        menu = QMenu(self)
        menu.addAction('Vídeo', self.download_video)
        menu.addAction('Audio', self.download_audio)
        self.download_button.setMenu(menu)

        # GUI Buttons.
        self.search_button.clicked.connect(self.search_video)

        self.exit_push_button.clicked.connect(self.on_exit)
        self.restart_push_button.clicked.connect(self.on_restart)

        self.download_manager_button.clicked.connect(
            self.on_download_manager_button_clicked)
        self.download_history_button.clicked.connect(
            self.on_download_history_button_clicked)
        self.settings_button.clicked.connect(self.on_settings_button_clicked)
        self.about_button.clicked.connect(self.on_about_button_clicked)

        self.windows = list()

        # Set browser directly to youtube.
        self.webview.setUrl(QUrl("https://www.youtube.com"))

        self._manager_subwindow = None
        self._history_subwindow = None
        self._settings_subwindow = None
        self._about_subwindow = None

    def get_configuration(self):
        # Get registry values.
        self.theme = QSettings("PyDownload", "Theme")
        self.downloads = QSettings("PyDownload", "Downloads")
        self.preferences = QSettings("PyDownload", "Preferences")
        self.languages = QSettings("PyDownload", "Languages")

    def on_download_manager_button_clicked(self):
        if self._manager_subwindow is None:
            self._manager_subwindow = Manager()
        self._manager_subwindow.show()
        self._manager_subwindow.activateWindow()

    def on_download_history_button_clicked(self):
        if self._history_subwindow is None:
            self._history_subwindow = History()
        self._history_subwindow.show()
        self._history_subwindow.activateWindow()

    def on_settings_button_clicked(self):
        if self._settings_subwindow is None:
            self._settings_subwindow = Settings()
        self._settings_subwindow.show()
        self._settings_subwindow.activateWindow()

    def on_about_button_clicked(self):
        if self._about_subwindow is None:
            self._about_subwindow = About()
        self._about_subwindow.show()
        self._about_subwindow.activateWindow()

    def on_restart(self):
        self.close()
        subprocess.Popen([sys.executable, "./main.py"])
        os.system('cls' if os.name == 'nt' else 'clear')

    def on_exit(self):
        answer = QMessageBox.question(self, "PyDownload | Salir",
                                      "¿Está seguro de que desea salir de la aplicación?")
        if answer == QMessageBox.Yes:
            sys.exit()

    # Search button clicked action.
    def search_video(self):
        self.worker[1] = WorkerThread(thread=1)
        self.worker[1].start()
        self.worker[1].search_video.connect(self.video_search)

    # Search for the video.
    def video_search(self):
        self.url = self.url_input.text()

        try:
            self.yt = YouTube(self.url)

            self.valid_url = True

            # Show details of the video.
            self.show_details()

        except Exception as e:
            self.valid_url = False
            print(e)
            QMessageBox.critical(
                self, "PyDownloader | Error", "Ha habido un problema al resolver el enlace, compruebe que sea válido.")

    # After video is searched action.
    def show_details(self):
        self.worker[2] = WorkerThread(thread=2)
        self.worker[2].start()
        self.worker[2].update_labels.connect(self.update_detail_labels)

    # show details of the searched video.
    def update_detail_labels(self):
        self.title_label.setText(self.yt.title)
        self.lenght_label.setText(str(self.yt.length))
        self.publish_date_label.setText(str(self.yt.publish_date))
        self.rating_label.setText(str(self.yt.rating))
        self.views_label.setText(str(self.yt.views))

    # To download the video.
    def download_video(self):
        if self.valid_url:
            self.change_status("Descargando vídeo...", "grey")

            download_path = self.downloads.value("downloads-path")

            preferred_video_quality = self.preferences.value(
                "preferred-video-quality")
            preferred_video_format = self.preferences.value(
                "preferred-video-format")
            formats = {"1": "mp4", "2": "3gpp", "3": "webm"}
            resolutions = {"1": "144p", "2": "360p", "3": "480p",
                           "4": "720p", "5": "1080p", "6": "1440p", "7": "2160p"}

            print(formats[str(preferred_video_format)])
            print(resolutions[str(preferred_video_quality)])

            # Download filtering by format user preferred resolution.
            yv = self.yt.streams.filter(
                file_extension=f"{formats[str(preferred_video_format)]}",
                resolution=f"{resolutions[str(preferred_video_quality)]}",
                progressive=True).first()

            yv.download(download_path)

            self.change_status("Vídeo descargado", "darkgreen")

    # To download the audio.
    def download_audio(self):
        if self.valid_url:
            self.change_status("Descargando audio...", "grey")

            frequencies = {"1": "48kbps", "2": "50kbps",
                           "3": "70kbps", "4": "128kbps", "5": "160kbps"}

            ya = self.yt(self.url).streams.filter(only_audio=True).all()

            ya.download(QSettings.value("downloads-path"))

            self.change_status("Vídeo descargado correctamente...", "green")

    # Download callback
    def download_callback(self, stream, chunk, file_handle, bytes_remaining):
        fileSize = stream.filesize
        bytes_downloaded = fileSize - bytes_remaining
        percentage = round((bytes_downloaded / fileSize) * 100, 2)
        print(f"{percentage}% Downloaded", end="\r")

    # To change the status bar text with dynamic information.
    def change_status(self, text, color):
        if color == "default" or color == "Default":
            self.status_label.setText(text)
        else:
            self.status_label.setText(text)
            self.status_label.setStyleSheet(
                "QLabel{ color: %s; }" % color)


class Manager(QMainWindow, Ui_Manager):
    def __init__(self):
        super(Manager, self).__init__()

        self.setupUi(self)

        self.search_downloads()

        # Had to manually create the GUI.
        if bool(self.downloads_count) == False:
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
        else:
            for i in range(5):
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

                # File name.
                self.file_title_label.setText(
                    "ROSALÍA - LA FAMA (Official Video) ft. The Weeknd")

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

                # File type.
                self.file_type_label.setText("Archivo: mp4")

                self.horizontalLayout_3.addWidget(self.file_type_label)

                self.file_size_label = QLabel(self.head_frame)
                self.file_size_label.setObjectName(u"file_size_label")
                font3 = QFont()
                font3.setPointSize(10)
                self.file_size_label.setFont(font3)

                self.file_size_label.setText("Tamaño: 300MB")

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

                # If file is type video set youtube.png as image.
                self.download_type_image.setPixmap(
                    QPixmap(u"../res/images/youtube.png"))

                self.download_type_image.setScaledContents(True)

                self.horizontalLayout_6.addWidget(self.download_type_image)

                self.download_progress_bar = QProgressBar(self.mid_frame)
                self.download_progress_bar.setObjectName(
                    u"download_progress_bar")
                self.download_progress_bar.setValue(24)

                self.horizontalLayout_6.addWidget(self.download_progress_bar)

                self.play_tool_button = QToolButton(self.mid_frame)
                self.play_tool_button.setObjectName(u"play_tool_button")
                icon = QIcon()
                icon.addFile(u"../res/images/play.png",
                             QSize(), QIcon.Normal, QIcon.Off)
                self.play_tool_button.setIcon(icon)
                self.play_tool_button.setIconSize(QSize(24, 24))

                self.horizontalLayout_6.addWidget(self.play_tool_button)

                self.pause_tool_button = QToolButton(self.mid_frame)
                self.pause_tool_button.setObjectName(u"pause_tool_button")
                icon1 = QIcon()
                icon1.addFile(u"../res/images/pause.png",
                              QSize(), QIcon.Normal, QIcon.Off)
                self.pause_tool_button.setIcon(icon1)
                self.pause_tool_button.setIconSize(QSize(24, 24))

                self.horizontalLayout_6.addWidget(self.pause_tool_button)

                self.cancel_tool_button = QToolButton(self.mid_frame)
                self.cancel_tool_button.setObjectName(u"cancel_tool_button")
                icon2 = QIcon()
                icon2.addFile(u"../res/images/cancel.png",
                              QSize(), QIcon.Normal, QIcon.Off)
                self.cancel_tool_button.setIcon(icon2)
                self.cancel_tool_button.setIconSize(QSize(24, 24))

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

                # Total downloaded.
                self.total_downloaded_label.setText(
                    "Descargados: 72MB / 300MB")

                self.horizontalLayout_9.addWidget(self.total_downloaded_label)

                self.estimated_time_label = QLabel(self.bottom_frame)
                self.estimated_time_label.setObjectName(
                    u"estimated_time_label")
                self.estimated_time_label.setFont(font3)
                self.estimated_time_label.setAlignment(
                    Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

                # Estimated time.
                self.estimated_time_label.setText("Tiempo estimado: 10m")

                self.horizontalLayout_9.addWidget(self.estimated_time_label)

                self.verticalLayout_5.addWidget(self.bottom_frame)

                self.verticalLayout_4.addWidget(self.download_frame)

        self.accept_button.clicked.connect(self.close)
        self.resume_all_button.clicked.connect(self.resume_all)
        self.stop_all_button.clicked.connect(self.stop_all)
        self.cancel_all_button.clicked.connect(self.cancel_all)

    def search_downloads(self):
        self.downloads_count = {1}

    def resume_all(self):
        pass

    def stop_all(self):
        pass

    def cancel_all(self):
        answer = QMessageBox.question(self, "PyDownload | Cancelar descargas",
                                      "¿Está seguro de que desea cancelar todas las descargas?")
        if answer == QMessageBox.Yes:
            print("Cancelando todas las descargas...")


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


####### ABOUT #######

class About(QMainWindow, Ui_About):
    def __init__(self):
        super(About, self).__init__()

        self.setupUi(self)

        self.accept_push_button.clicked.connect(self.close)

####### ABOUT #######

####### SETTINGS #######


class Settings(QMainWindow, Ui_Settings):
    def __init__(self):
        super(Settings, self).__init__()

        self.setupUi(self)

        # Get the configuration values.
        self.get_configuration()
        # Set the configuration values.
        self.set_configuration()

        # GUI Buttons
        self.accept_push_button.clicked.connect(self.accept_and_exit)
        self.apply_push_button.clicked.connect(self.apply)
        self.cancel_push_button.clicked.connect(self.close)
        self.file_input.clicked.connect(self.browse_files)

    def get_configuration(self):
        # Get registry values.
        self.theme = QSettings("PyDownload", "Theme")
        self.downloads = QSettings("PyDownload", "Downloads")
        self.preferences = QSettings("PyDownload", "Preferences")
        self.languages = QSettings("PyDownload", "Languages")

    def set_configuration(self):
        # Themes
        if self.theme.value("light-theme") == "true":
            self.light_theme_radio.setChecked(True)
        else:
            self.dark_theme_radio.setChecked(True)

        # Downloads
        self.path_input.setText(self.downloads.value("downloads-path"))
        self.min_speed_input.setCurrentIndex(
            self.downloads.value("downloads-min-speed"))
        self.max_speed_input.setCurrentIndex(
            self.downloads.value("downloads-max-speed"))
        if self.downloads.value("minspeed-check-state") == "true":
            self.min_speed_input.setEnabled(True)
            self.minspeed_check.setChecked(True)
        if self.downloads.value("maxspeed-check-state") == "true":
            self.max_speed_input.setEnabled(True)
            self.max_speed_check.setChecked(True)

        # Preferences
        self.preferred_videoformat_input.setCurrentIndex(
            self.preferences.value("preferred-video-format"))
        self.preferred_audioformat_input.setCurrentIndex(
            self.preferences.value("preferred-audio-format"))
        self.preferred_videoquality_input.setCurrentIndex(
            self.preferences.value("preferred-video-quality"))
        self.preferred_audioquality_input.setCurrentIndex(
            self.preferences.value("preferred-audio-quality"))

        # Preferences checkboxes
        if self.preferences.value("videoformat-check-state") == "true":
            self.preferred_videoformat_input.setEnabled(True)
            self.videoformat_check.setChecked(True)
        if self.preferences.value("audioformat-check-state") == "true":
            self.preferred_audioformat_input.setEnabled(True)
            self.audioformat_check.setChecked(True)
        if self.preferences.value("videoquality-check-state") == "true":
            self.preferred_videoquality_input.setEnabled(True)
            self.videoquality_check.setChecked(True)
        if self.preferences.value("audioquality-check-state") == "true":
            self.preferred_audioquality_input.setEnabled(True)
            self.audioquality_check.setChecked(True)

        # Languages
        if self.languages.value("spanish-radiobtn-state") == "true":
            self.spanish_radiobtn.setChecked(True)
        if self.languages.value("catalan-radiobtn-state") == "true":
            self.catalan_radiobtn.setChecked(True)
        if self.languages.value("english-radiobtn-state") == "true":
            self.english_radiobtn.setChecked(True)
        if self.languages.value("portuguese-radiobtn-state") == "true":
            self.portuguese_radiobtn.setChecked(True)

    def save_configuration(self):
        # Themes
        self.theme.setValue("light-theme", self.light_theme_radio.isChecked())
        self.theme.setValue("dark-theme", self.dark_theme_radio.isChecked())

        # Downloads
        self.downloads.setValue("downloads-path", self.path_input.text())
        self.downloads.setValue("downloads-min-speed",
                                self.min_speed_input.currentIndex())
        self.downloads.setValue("downloads-max-speed",
                                self.max_speed_input.currentIndex())
        self.downloads.setValue("minspeed-check-state",
                                self.minspeed_check.isChecked())
        self.downloads.setValue("maxspeed-check-state",
                                self.max_speed_check.isChecked())

        # Preferences
        self.preferences.setValue(
            "preferred-video-format", self.preferred_videoformat_input.currentIndex())
        self.preferences.setValue(
            "preferred-audio-format", self.preferred_audioformat_input.currentIndex())
        self.preferences.setValue(
            "preferred-video-quality", self.preferred_videoquality_input.currentIndex())
        self.preferences.setValue(
            "preferred-audio-quality", self.preferred_audioquality_input.currentIndex())

        # Preferences checkboxes
        self.preferences.setValue(
            "videoformat-check-state", self.videoformat_check.isChecked())
        self.preferences.setValue(
            "audioformat-check-state", self.audioformat_check.isChecked())
        self.preferences.setValue(
            "videoquality-check-state", self.videoquality_check.isChecked())
        self.preferences.setValue(
            "audioquality-check-state", self.audioquality_check.isChecked())

        # Languages
        self.languages.setValue("spanish-radiobtn-state",
                                self.spanish_radiobtn.isChecked())
        self.languages.setValue("catalan-radiobtn-state",
                                self.catalan_radiobtn.isChecked())
        self.languages.setValue("english-radiobtn-state",
                                self.english_radiobtn.isChecked())
        self.languages.setValue(
            "portuguese-radiobtn-state", self.portuguese_radiobtn.isChecked())

    def check_checkboxes_state(self):
        if self.videoformat_check.isChecked() == True:
            self.preferred_videoformat_input.setEnabled(True)
        else:
            self.preferred_videoformat_input.setEnabled(False)

        if self.audioformat_check.isChecked() == True:
            self.preferred_audioformat_input.setEnabled(True)
        else:
            self.preferred_audioformat_input.setEnabled(False)

        if self.videoquality_check.isChecked() == True:
            self.preferred_videoquality_input.setEnabled(True)
        else:
            self.preferred_videoquality_input.setEnabled(False)

        if self.audioquality_check.isChecked() == True:
            self.preferred_audioquality_input.setEnabled(True)
        else:
            self.preferred_audioquality_input.setEnabled(False)

        if self.minspeed_check.isChecked() == True:
            self.min_speed_input.setEnabled(True)
        else:
            self.min_speed_input.setEnabled(False)

        if self.max_speed_check.isChecked() == True:
            self.max_speed_input.setEnabled(True)
        else:
            self.max_speed_input.setEnabled(False)

    def browse_files(self):
        user_name = getpass.getuser()
        file_name = QFileDialog.getExistingDirectory(
            self, "Abrir Carpeta", f"C:/Users/{user_name}/Downloads")
        self.path_input.setText(file_name)

    def accept_and_exit(self):
        # Apply changes and then close.
        self.apply()
        self.close()

    def apply(self):
        # Check which CheckBoxes are Checked.
        self.check_checkboxes_state()

        # Set the configuration.
        self.save_configuration()

        # Change status.
        self.change_status("Cambios realizados correctamente.", "darkgreen")

    def change_status(self, text, color):
        if color == "default" or color == "Default":
            self.status_label.setText(text)
        else:
            self.status_label.setText(text)
            self.status_label.setStyleSheet(
                "QLabel{ color: %s; }" % color)

####### SETTINGS #######


####### HISTORY #######

####### HISTORY #######


####### MANAGER #######

####### MANAGER #######


def main():
    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load("qtbase_" + QLocale.system().name(),
                    QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)

    gui = MainWindow()
    gui.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
