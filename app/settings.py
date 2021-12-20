import sys
import getpass

from gui.ui_Settings import Ui_Settings

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator, QSettings
from PySide6.QtWidgets import QMainWindow, QApplication, QFileDialog


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
        if self.downloads.value("downloads-path") != "" and self.downloads.value("downloads-min-speed") is not None and self.downloads.value("downloads-max-speed") is not None:
            self.path_input.setText(self.downloads.value("downloads-path"))
            self.min_speed_input.setCurrentIndex(
                int(self.downloads.value("downloads-min-speed")))
            self.max_speed_input.setCurrentIndex(
                int(self.downloads.value("downloads-max-speed")))
            if self.downloads.value("minspeed-check-state") == "true":
                self.min_speed_input.setEnabled(True)
                self.minspeed_check.setChecked(True)
            if self.downloads.value("maxspeed-check-state") == "true":
                self.max_speed_input.setEnabled(True)
                self.max_speed_check.setChecked(True)

        # Preferences
        if self.preferences.value("preferred-video-format") is not None and self.preferences.value("preferred-audio-format") is not None and self.preferences.value("preferred-video-quality") is not None and self.preferences.value("preferred-audio-quality") is not None:
            self.preferred_videoformat_input.setCurrentIndex(
                int(self.preferences.value("preferred-video-format")))
            self.preferred_audioformat_input.setCurrentIndex(
                int(self.preferences.value("preferred-audio-format")))
            self.preferred_videoquality_input.setCurrentIndex(
                int(self.preferences.value("preferred-video-quality")))
            self.preferred_audioquality_input.setCurrentIndex(
                int(self.preferences.value("preferred-audio-quality")))

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


def main():
    app = QApplication(sys.argv)

    translator = QTranslator()
    translator.load("qtbase_" + QLocale.system().name(),
                    QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(translator)

    gui = Settings()
    gui.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
