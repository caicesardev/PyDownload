import sys
import os
import subprocess
import datetime

from gui.ui_MainWindow import Ui_MainWindow

from pytube import YouTube

from manager import Manager
from history import History
from settings import Settings
from about import About

from PySide6 import QtWebEngineWidgets
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
from PySide6.QtCore import (
    QLibraryInfo,
    QLocale,
    QObject,
    QThread,
    QTranslator,
    QUrl,
    QSettings,
    Signal,
    QSettings,
    QSize,
    QPoint)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QMenu,
    QVBoxLayout)

__version__ = "1.0.0"


########################################
########################################
# This file inits the MainWindow UI and
# handles events.
########################################
########################################

# Worker class to update details labels.
class Worker(QObject):
    finished = Signal()
    title_label = Signal(str)
    lenght_label = Signal(str)
    publish_date_label = Signal(str)
    author_label = Signal(str)
    views_label = Signal(str)

    def __init__(self, url):
        super(Worker, self).__init__()
        self.url = url

    def run(self):
        self.yt = YouTube(self.url)
        self.title_label.emit(self.yt.title)
        self.lenght_label.emit(str(datetime.timedelta(seconds=self.yt.length)))
        self.publish_date_label.emit(
            str(self.yt.publish_date.strftime("%d de %b de %Y")))
        self.author_label.emit(self.yt.author)
        self.views_label.emit(str(f"{self.yt.views:,}"))
        self.finished.emit()


# MainWindow.
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        # Get user settings.
        self.get_settings()
        # Set user settings (window size and pos)
        self.set_settings()

        # Shortcuts.
        self.quit_sc = QShortcut(QKeySequence('Ctrl+W'), self)
        self.quit_sc.activated.connect(self.on_exit)

        self.dwnld_mgr_sc = QShortcut(QKeySequence('Ctrl+D'), self)
        self.dwnld_mgr_sc.activated.connect(
            self.on_download_manager_button_clicked)

        self.dwnld_hr_sc = QShortcut(QKeySequence('Ctrl+H'), self)
        self.dwnld_hr_sc.activated.connect(
            self.on_download_history_button_clicked)

        self.settings_sc = QShortcut(QKeySequence('Ctrl+S'), self)
        self.settings_sc.activated.connect(self.on_settings_button_clicked)

        self.abt_sc = QShortcut(QKeySequence('Ctrl+A'), self)
        self.abt_sc.activated.connect(self.on_about_button_clicked)

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
        # Set current url to search input.
        self.webview.urlChanged.connect(self.set_current_url)
        self.webview.urlChanged.connect(
            self.show_details)

        # Download Button Menu.
        menu = QMenu(self)
        menu.addAction(QIcon("../res/images/reproductor-de-video.png"),
                       'Agregar vídeo a la cola', self.add_video_to_queue)
        menu.addAction(QIcon("../res/images/volumen.png"),
                       'Agregar audio a la cola', self.add_audio_to_queue)
        self.add_to_queue_button.setMenu(menu)

        # GUI Buttons.
        self.exit_push_button.clicked.connect(self.on_exit)
        self.restart_push_button.clicked.connect(self.on_restart)

        # Sidebar buttons.
        self.download_manager_button.clicked.connect(
            self.on_download_manager_button_clicked)
        self.download_history_button.clicked.connect(
            self.on_download_history_button_clicked)
        self.settings_button.clicked.connect(self.on_settings_button_clicked)
        self.about_button.clicked.connect(self.on_about_button_clicked)

        # Variables
        self.valid_url = False

        self._manager_subwindow = None
        self._history_subwindow = None
        self._settings_subwindow = None
        self._about_subwindow = None

        self.manager = Manager()

        self.list_of_video_urls = []
        self.list_of_audio_urls = []

    def set_current_url(self):
        self.current_url = self.webview.url().toString()
        self.url_input.setText(self.current_url)

    def get_settings(self):
        # Get registry values.
        self.theme = QSettings("PyDownload", "Theme")
        self.downloads = QSettings("PyDownload", "Downloads")
        self.preferences = QSettings("PyDownload", "Preferences")
        self.languages = QSettings("PyDownload", "Languages")
        self.w_attrib = QSettings("PyDownload", "WindowAttributes")

    def set_settings(self):
        # Initial window size/pos last saved. Use default values for first time.
        self.resize(self.w_attrib.value("size", QSize(270, 225)))
        self.move(self.w_attrib.value("pos", QPoint(50, 50)))

    def on_download_manager_button_clicked(self):
        if self._manager_subwindow is None:
            self._manager_subwindow = Manager()
            self.list_of_video_urls.clear()
            self.list_of_audio_urls.clear()
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

    # Show details of the searched video.
    def show_details(self):
        self.url = self.url_input.text()
        # Create a QThread object.
        self.thread = QThread()
        # Create a worker object.
        self.worker = Worker(self.url)
        # Move worker to the thread.
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        if self.url != "https://www.youtube.com/":
            try:
                if self.url.startswith("watch?v=", 24, 32):
                    self.valid_url = True

                    self.worker.title_label.connect(
                        self.update_title_label_event)
                    self.worker.lenght_label.connect(
                        self.update_lenght_label_event)
                    self.worker.publish_date_label.connect(
                        self.update_publish_date_label_event)
                    self.worker.author_label.connect(
                        self.update_author_label_event)
                    self.worker.views_label.connect(
                        self.update_views_label_event)

                    # Start the thread.
                    self.thread.start()

            except Exception as e:
                self.valid_url = False
                self.validation_error(e)

    # To add video to queue.
    def add_video_to_queue(self):
        if self.valid_url:
            self.url = self.url_input.text()
            self.yt = YouTube(self.url)

            # If it's not already in the list append it.
            if self.url not in self.list_of_video_urls:
                self.list_of_video_urls.append(self.url)
                print(f"List of videos: {self.list_of_video_urls}")

                if self._manager_subwindow is None:
                    self._manager_subwindow = Manager(
                        self.yt.title,
                        "Video",
                        "300 MB",
                        "../res/images/youtube.png",
                        "250MB",
                        "5m")
                    self._manager_subwindow = Manager()

                self._manager_subwindow.show()
                self._manager_subwindow.activateWindow()

        else:
            QMessageBox.information(self, "PyDownload | Advertencia",
                                    "No ha introucido ningún enlace válido. Inténtelo de nuevo.")

    # To add audio to queue.
    def add_audio_to_queue(self):
        if self.valid_url:
            # If it's not already in the list append it.
            if self.url not in self.list_of_audio_urls:
                self.list_of_audio_urls.append(self.url)
                print(f"List of videos: {self.list_of_audio_urls}")
        else:
            QMessageBox.information(self, "PyDownload | Advertencia",
                                    "No ha introducido ningún enlace válido. Por favor inténtelo de nuevo.")

    # Error when validating.
    @ staticmethod
    def validation_error(e):
        """[summary]

        Args:
            e ([str]): [Exception]
        """
        print(f"Error: {e}")
        msg = QMessageBox()
        msg.setWindowTitle("PyDownload | URL no válida")
        msg.setIcon(QMessageBox.Critical)
        msg.setText(
            "La URL no se puede descargar o no está disponible.")
        msg.setDetailedText(f"Error: {str(e)}")
        msg.exec()

    def update_title_label_event(self, txt):
        self.title_label.setText(txt)

    def update_lenght_label_event(self, txt):
        self.lenght_label.setText(txt)

    def update_publish_date_label_event(self, txt):
        self.publish_date_label.setText(txt)

    def update_author_label_event(self, txt):
        self.author_label.setText(txt)

    def update_views_label_event(self, txt):
        self.views_label.setText(txt)

    # To change the status bar text with dynamic information.
    def change_status(self, text, color):
        if color == "default" or color == "Default":
            self.status_label.setText(text)
        else:
            self.status_label.setText(text)
            self.status_label.setStyleSheet(
                "QLabel{ color: %s; }" % color)

    # Remember window postion and size on exit.
    def closeEvent(self, event) -> None:
        self.w_attrib.setValue("size", self.size())
        self.w_attrib.setValue("pos", self.pos())


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
