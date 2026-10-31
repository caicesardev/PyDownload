import sys

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

import resources_rc  # noqa: F401
from constants import APP_NAME, VERSION
from src.browser.secure_profile import SecureProfile
from src.settings.app_paths import browser_storage_directory
from src.widgets.theme import apply_theme
from src.windows.main_window import MainWindow

APP_LOCALE = QLocale(QLocale.Language.Spanish, QLocale.Country.Spain)


def install_qt_translations(app: QApplication) -> None:
    translator = QTranslator(app)
    translations_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    if translator.load(APP_LOCALE, "qtbase", "_", translations_path):
        app.installTranslator(translator)


def run() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_NAME)
    app.setApplicationVersion(VERSION)
    app.setWindowIcon(QIcon(":/icons/app.png"))
    install_qt_translations(app)
    apply_theme(app)

    profile = SecureProfile(browser_storage_directory(), app)
    window = MainWindow(profile)
    window.show()
    exit_code = app.exec()
    window.deleteLater()
    return exit_code


if __name__ == "__main__":
    sys.exit(run())
