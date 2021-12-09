import sys
import os
import subprocess
from traceback import print_exception

from pytube import YouTube

from gui.ui_MainWindow import Ui_MainWindow

from manager import Manager
from history import History
from settings import Settings
from about import About

from PySide6 import QtWebEngineWidgets
from PySide6.QtCore import QLibraryInfo, QLocale, QThread, QTranslator, QUrl, QSettings, Signal
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QMenu,
    QVBoxLayout)

__version__ = "1.0.0"


# Thread class.
class WorkerThread(QThread):
    update_labels = Signal()
    search_video = Signal()

    def __init__(self):
        super(WorkerThread, self).__init__()

    def run(self):
        pass

    def stop(self):
        pass


# MainWindow.
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
        # Set browser directly to youtube.
        self.webview.setUrl(QUrl("https://www.youtube.com"))

        # Download Button Menu.
        menu = QMenu(self)
        menu.addAction('Vídeo', self.download_video)
        menu.addAction('Audio', self.download_audio)
        self.download_button.setMenu(menu)

        # GUI Buttons.
        self.search_button.clicked.connect(self.search_video)
        self.exit_push_button.clicked.connect(self.on_exit)
        self.restart_push_button.clicked.connect(self.on_restart)

        # Sidebar buttons.
        self.download_manager_button.clicked.connect(
            self.on_download_manager_button_clicked)
        self.download_history_button.clicked.connect(
            self.on_download_history_button_clicked)
        self.settings_button.clicked.connect(self.on_settings_button_clicked)
        self.about_button.clicked.connect(self.on_about_button_clicked)

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

    # Search for the video.
    def search_video(self):
        self.url = self.url_input.text()

        try:
            self.yt = YouTube(self.url)
            self.valid_url = True
            self.show_details()
        except Exception:
            self.valid_url = False
            print_exception(*sys.exc_info())
            msg = QMessageBox()
            msg.setWindowTitle("PyDownloader | Error")
            msg.setIcon(QMessageBox.Critical)
            msg.setText(
                "Ha habido un problema al resolver el enlace, compruebe que sea válido.")
            msg.setDetailedText(str(sys.exc_info()))
            msg.exec()

    # Show details of the searched video.
    def show_details(self):
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

    # Download callback.
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
