import sys

from PySide6.QtCore import QLibraryInfo, QLocale, QTranslator
from PySide6.QtWidgets import QApplication

import resources_rc  # noqa: F401
from constants import APP_NAME, VERSION
from src.browser.secure_profile import SecureProfile
from src.settings.app_paths import browser_storage_directory
from src.widgets.icons import app_icon
from src.widgets.theme import apply_theme
from src.windows.main_window import MainWindow

APP_LOCALE = QLocale(QLocale.Language.Spanish, QLocale.Country.Spain)
QT_TRANSLATION_CATALOGS = ("qtbase", "qtwebengine")


def install_qt_translations(app: QApplication) -> None:
    translations_path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    for catalog in QT_TRANSLATION_CATALOGS:
        translator = QTranslator(app)
        if translator.load(APP_LOCALE, catalog, "_", translations_path):
            app.installTranslator(translator)


def run() -> int:
    QLocale.setDefault(APP_LOCALE)
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_NAME)
    app.setApplicationVersion(VERSION)
    app.setWindowIcon(app_icon())
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
