import sys
import os
import subprocess
import time
from traceback import print_exception

from pytube import YouTube

from gui.ui_MainWindow import Ui_MainWindow

from manager import Manager
from history import History
from settings import Settings
from about import About

from PySide6 import QtWebEngineWidgets
from PySide6.QtCore import QLibraryInfo, QLocale, QObject, QThread, QTranslator, QUrl, QSettings, Signal
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QMenu,
    QVBoxLayout)

__version__ = "1.0.0"


# Thread class.
class Worker(QObject):
    finished = Signal()
    update_labels = Signal()
    validate_error = Signal(str)
    valid_url = Signal(bool)

    def run(self):
        try:
            global yt
            yt = YouTube(url)
            self.update_labels.emit()
            self.valid_url.emit(True)
            self.finished.emit()
        except Exception as e:
            self.valid_url.emit(False)
            self.validate_error.emit(str(e))
            self.finished.emit()

# Worker class to update details labels.


class UpdateWorker(QObject):
    finished = Signal()
    title_label = Signal()
    lenght_label = Signal()
    publish_date_label = Signal()
    rating_label = Signal()
    views_label = Signal()

    def run(self):
        self.title_label.emit()
        time.sleep(1)
        self.lenght_label.emit()
        time.sleep(1)
        self.publish_date_label.emit()
        time.sleep(1)
        self.rating_label.emit()
        time.sleep(1)
        self.views_label.emit()
        self.finished.emit()

# MainWindow.


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        # Get user configuration.
        self.get_configuration()

        # Window Variables.
        self.showing_preview = False
        self.worker = Worker()
        self.valid_url = self.worker.valid_url

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
            self._manager_subwindow = Manager("")
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
        global url
        url = self.url_input.text()

        # Create a QThread object.
        self.thread = QThread()
        # Create a worker object.
        self.worker = Worker()
        # Move worker to the thread.
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.update_labels.connect(self.show_details)
        self.worker.validate_error.connect(self.validate_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # Start the thread.
        self.thread.start()

        self.search_button.setEnabled(False)

        # Final resets.
        self.thread.finished.connect(
            lambda: self.search_button.setEnabled(True)
        )

    # Show details of the searched video.
    def show_details(self):
        # Create a QThread object.
        self.thread2 = QThread()
        # Create a worker object.
        self.worker2 = UpdateWorker()
        # Move worker to the thread.
        self.worker2.moveToThread(self.thread2)
        # Connect signals and slots
        self.thread2.started.connect(self.worker2.run)
        self.worker2.finished.connect(self.thread2.quit)
        self.worker2.finished.connect(self.worker2.deleteLater)
        self.thread2.finished.connect(self.thread2.deleteLater)

        self.worker2.title_label.connect(
            lambda txt=yt.title: self.title_label.setText(txt))
        self.worker2.lenght_label.connect(
            lambda txt=yt.length: self.lenght_label.setText(txt))
        self.worker2.publish_date_label.connect(
            lambda txt=yt.publish_date: self.publish_date_label.setText(txt))
        self.worker2.rating_label.connect(
            lambda txt=yt.rating: self.rating_label.setText(txt))
        self.worker2.views_label.connect(
            lambda txt=yt.views: self.views_label.setText(txt))

        # Start the thread.
        self.thread2.start()

        """
        self.title_label.setText(yt.title)
        self.lenght_label.setText(str(yt.length))
        self.publish_date_label.setText(str(yt.publish_date))
        self.rating_label.setText(str(yt.rating))
        self.views_label.setText(str(yt.views))
        """

    # To download the video.
    def download_video(self):
        if self.worker.valid_url:
            self.change_status("Descargando vídeo...", "grey")

            if self._manager_subwindow is None:
                self._manager_subwindow = Manager(url)
                self._manager_subwindow.show()
                self._manager_subwindow.activateWindow()

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

    # Error when validating.
    def validate_error(self, e):
        print(e)
        msg = QMessageBox()
        msg.setWindowTitle("PyDownload | Error")
        msg.setIcon(QMessageBox.Critical)
        msg.setText(
            "La URL no se puede descargar o no está disponible.")
        msg.setDetailedText(e)
        msg.exec()

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
