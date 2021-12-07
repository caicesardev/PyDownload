import sys
import os
import subprocess
import getpass

from pytube import YouTube

from gui.ui_Settings import Ui_Settings
from gui.ui_About import Ui_About
from gui.ui_MainWindow import Ui_MainWindow
from PySide6 import QtWebEngineWidgets
from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator, QUrl, QSettings
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QMenu, QVBoxLayout, QWidget, QFileDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)

        # Get user configuration.
        self.get_configuration()

        # App Variables
        self.valid_url = False
        self.showing_preview = False

        # Create a QVBoxLayout.
        self.vbox = QVBoxLayout()
        # Create a QWebEngineView instance.
        self.webview = QtWebEngineWidgets.QWebEngineView()
        # Add the QWebEngineView instance to layout.
        self.vbox.addWidget(self.webview)
        # Set the layout to the video_preview_widget.
        self.video_preview_widget.setLayout(self.vbox)

        # Download Button Menu
        menu = QMenu(self)
        menu.addAction('Vídeo', self.download_video)
        menu.addAction('Audio', self.download_audio)
        self.download_button.setMenu(menu)

        # GUI Buttons
        self.search_button.clicked.connect(self.search_video)

        self.exit_push_button.clicked.connect(self.on_exit)
        self.restart_push_button.clicked.connect(self.on_restart)

        self.settings_button.clicked.connect(self.on_settings_button_clicked)
        self.about_button.clicked.connect(self.on_about_button_clicked)

        self.windows = list()

        # Set browser directly to youtube.
        self.webview.setUrl(QUrl("https://www.youtube.com"))

    def get_configuration(self):
        # Get registry values.
        self.theme = QSettings("PyDownload", "Theme")
        self.downloads = QSettings("PyDownload", "Downloads")
        self.preferences = QSettings("PyDownload", "Preferences")
        self.languages = QSettings("PyDownload", "Languages")

    def on_about_button_clicked(self):
        ui = About()
        self.windows.append(ui)
        ui.show()

    def on_settings_button_clicked(self):
        ui = Settings()
        self.windows.append(ui)
        ui.show()

    def on_restart(self):
        self.close()
        subprocess.Popen([sys.executable, "./main.py"])
        os.system('cls' if os.name == 'nt' else 'clear')

    def on_exit(self):
        answer = QMessageBox.question(self, "PyDownload | Salir",
                                      "¿Está seguro de que quiere salir de la aplicación?")
        if answer == QMessageBox.Yes:
            sys.exit()

    # To search for the video.
    def search_video(self):
        self.url = self.url_input.text()

        try:
            self.yt = YouTube(self.url)

            """
            streams = self.yt.streams.all()
            for stream in streams:
                print(stream)
            """

            self.change_status("Vídeo encontrado.", "green")
            self.valid_url = True

            # Show details of the video.
            self.show_details()

        except:
            self.change_status("Vídeo no encontrado.", "red")
            self.valid_url = False
            QMessageBox.critical(
                self, "PyDownloader | Error", "Ha habido un problema al resolver el enlace, compruebe que sea válido.")

    # To show details of the searched video.
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

            # Debug if filtering is not none.
            print(self.yt.streams.filter(
                file_extension=f"{formats[str(preferred_video_format)]}",
                resolution=f"{resolutions[str(preferred_video_quality)]}",
                progressive=True).first())

            # If no stream matches filtering.
            if yv == None:
                yv = self.yt.streams.filter(
                    file_extension=f"{formats[str(preferred_video_format)]}",
                    resolution=f"{resolutions[str(preferred_video_quality)]}",
                    progressive=False).first()
                yv.download(download_path)
            else:
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
