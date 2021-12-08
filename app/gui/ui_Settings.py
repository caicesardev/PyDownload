# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'SettingsuyQhEP.ui'
##
# Created by: Qt User Interface Compiler version 6.2.1
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter,
                           QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
                               QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QMainWindow, QPushButton, QRadioButton,
                               QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
                               QWidget)
import images_rc
import images_rc


class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(800, 642)
        font = QFont()
        Settings.setFont(font)
        self.centralwidget = QWidget(Settings)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.content_container_frame = QFrame(self.centralwidget)
        self.content_container_frame.setObjectName(u"content_container_frame")
        self.content_container_frame.setStyleSheet(u"QFrame#content_container_frame{\n"
                                                   "	border: 2px solid whitesmoke;\n"
                                                   "	border-radius: 30px;\n"
                                                   "	background: white;\n"
                                                   "}")
        self.content_container_frame.setFrameShape(QFrame.StyledPanel)
        self.content_container_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.content_container_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header_frame = QFrame(self.content_container_frame)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMaximumSize(QSize(16777215, 70))
        self.header_frame.setFrameShape(QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.header_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.welcome_label_frame = QFrame(self.header_frame)
        self.welcome_label_frame.setObjectName(u"welcome_label_frame")
        self.welcome_label_frame.setMaximumSize(QSize(260, 16777215))
        self.horizontalLayout_4 = QHBoxLayout(self.welcome_label_frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.image = QLabel(self.welcome_label_frame)
        self.image.setObjectName(u"image")
        self.image.setMaximumSize(QSize(24, 24))
        self.image.setPixmap(QPixmap(u":/res/images/setting.png"))
        self.image.setScaledContents(True)

        self.horizontalLayout_4.addWidget(self.image)

        self.welcome_label = QLabel(self.welcome_label_frame)
        self.welcome_label.setObjectName(u"welcome_label")
        self.welcome_label.setFont(font)

        self.horizontalLayout_4.addWidget(self.welcome_label)

        self.horizontalLayout.addWidget(self.welcome_label_frame)

        self.status_label_frame = QFrame(self.header_frame)
        self.status_label_frame.setObjectName(u"status_label_frame")
        self.status_label_frame.setStyleSheet(u"QFrame#status_label_frame{\n"
                                              "	border-radius: 8px;\n"
                                              "	background-color: #F6F8FA;\n"
                                              "}")
        self.status_label_frame.setFrameShape(QFrame.StyledPanel)
        self.status_label_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.status_label_frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.status_label = QLabel(self.status_label_frame)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setFont(font)
        self.status_label.setStyleSheet(u"QLabel#status_label{\n"
                                        "	margin-top: 2px;\n"
                                        "}")

        self.horizontalLayout_6.addWidget(self.status_label)

        self.horizontalLayout.addWidget(self.status_label_frame)

        self.verticalLayout.addWidget(self.header_frame)

        self.header_line = QFrame(self.content_container_frame)
        self.header_line.setObjectName(u"header_line")
        self.header_line.setStyleSheet(u"background-color: darkgreen;\n"
                                       "margin-left: 20px;\n"
                                       "margin-right: 10px;")
        self.header_line.setFrameShape(QFrame.HLine)
        self.header_line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.header_line)

        self.middle_frame = QFrame(self.content_container_frame)
        self.middle_frame.setObjectName(u"middle_frame")
        self.middle_frame.setMaximumSize(QSize(16777215, 82))
        self.middle_frame.setFrameShape(QFrame.StyledPanel)
        self.middle_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.middle_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.customization_buttons_group = QGroupBox(self.middle_frame)
        self.customization_buttons_group.setObjectName(
            u"customization_buttons_group")
        self.customization_buttons_group.setFont(font)
        self.customization_buttons_group.setStyleSheet(u"QGroupBox#customization_buttons_group{\n"
                                                       "	color: darkgreen;\n"
                                                       "	border: 1px solid #c7c8ca;\n"
                                                       "	border-radius: 10px;\n"
                                                       "	padding: 10px;\n"
                                                       "}")
        self.horizontalLayout_3 = QHBoxLayout(self.customization_buttons_group)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 4, -1, -1)
        self.light_theme_radio = QRadioButton(self.customization_buttons_group)
        self.light_theme_radio.setObjectName(u"light_theme_radio")
        self.light_theme_radio.setFont(font)
        self.light_theme_radio.setChecked(True)

        self.horizontalLayout_3.addWidget(self.light_theme_radio)

        self.dark_theme_radio = QRadioButton(self.customization_buttons_group)
        self.dark_theme_radio.setObjectName(u"dark_theme_radio")
        self.dark_theme_radio.setFont(font)

        self.horizontalLayout_3.addWidget(self.dark_theme_radio)

        self.horizontalLayout_2.addWidget(self.customization_buttons_group)

        self.downloads_path_group = QGroupBox(self.middle_frame)
        self.downloads_path_group.setObjectName(u"downloads_path_group")
        self.downloads_path_group.setFont(font)
        self.downloads_path_group.setStyleSheet(u"QGroupBox#downloads_path_group{\n"
                                                "	color: darkgreen;\n"
                                                "	border: 1px solid #c7c8ca;\n"
                                                "	border-radius: 10px;\n"
                                                "	padding: 10px;\n"
                                                "}")
        self.horizontalLayout_5 = QHBoxLayout(self.downloads_path_group)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.path_input = QLineEdit(self.downloads_path_group)
        self.path_input.setObjectName(u"path_input")
        self.path_input.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.path_input)

        self.file_input = QToolButton(self.downloads_path_group)
        self.file_input.setObjectName(u"file_input")

        self.horizontalLayout_5.addWidget(self.file_input)

        self.horizontalLayout_2.addWidget(self.downloads_path_group)

        self.verticalLayout.addWidget(self.middle_frame)

        self.middle_frame_2 = QFrame(self.content_container_frame)
        self.middle_frame_2.setObjectName(u"middle_frame_2")
        self.middle_frame_2.setFrameShape(QFrame.StyledPanel)
        self.middle_frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.middle_frame_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(16)
        self.download_group_box = QGroupBox(self.middle_frame_2)
        self.download_group_box.setObjectName(u"download_group_box")
        self.download_group_box.setFont(font)
        self.download_group_box.setStyleSheet(u"QGroupBox#download_group_box{\n"
                                              "	color: darkgreen;\n"
                                              "	border: 1px solid #c7c8ca;\n"
                                              "	border-radius: 10px;\n"
                                              "	padding: 10px;\n"
                                              "}")
        self.gridLayout_4 = QGridLayout(self.download_group_box)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.min_speed_label = QLabel(self.download_group_box)
        self.min_speed_label.setObjectName(u"min_speed_label")
        self.min_speed_label.setFont(font)

        self.gridLayout_4.addWidget(self.min_speed_label, 0, 0, 1, 1)

        self.min_speed_input = QComboBox(self.download_group_box)
        self.min_speed_input.addItem("")
        self.min_speed_input.addItem("")
        self.min_speed_input.addItem("")
        self.min_speed_input.addItem("")
        self.min_speed_input.addItem("")
        self.min_speed_input.setObjectName(u"min_speed_input")
        self.min_speed_input.setEnabled(False)
        self.min_speed_input.setFont(font)

        self.gridLayout_4.addWidget(self.min_speed_input, 0, 1, 1, 1)

        self.max_speed_label = QLabel(self.download_group_box)
        self.max_speed_label.setObjectName(u"max_speed_label")
        self.max_speed_label.setFont(font)

        self.gridLayout_4.addWidget(self.max_speed_label, 2, 0, 1, 1)

        self.max_speed_input = QComboBox(self.download_group_box)
        self.max_speed_input.addItem("")
        self.max_speed_input.addItem("")
        self.max_speed_input.addItem("")
        self.max_speed_input.addItem("")
        self.max_speed_input.addItem("")
        self.max_speed_input.setObjectName(u"max_speed_input")
        self.max_speed_input.setEnabled(False)
        self.max_speed_input.setFont(font)

        self.gridLayout_4.addWidget(self.max_speed_input, 2, 1, 1, 1)

        self.minspeed_check = QCheckBox(self.download_group_box)
        self.minspeed_check.setObjectName(u"minspeed_check")
        self.minspeed_check.setFont(font)

        self.gridLayout_4.addWidget(self.minspeed_check, 0, 2, 1, 1)

        self.max_speed_check = QCheckBox(self.download_group_box)
        self.max_speed_check.setObjectName(u"max_speed_check")
        self.max_speed_check.setFont(font)

        self.gridLayout_4.addWidget(self.max_speed_check, 2, 2, 1, 1)

        self.gridLayout_2.addWidget(self.download_group_box, 1, 0, 1, 1)

        self.preferences_group = QGroupBox(self.middle_frame_2)
        self.preferences_group.setObjectName(u"preferences_group")
        self.preferences_group.setFont(font)
        self.preferences_group.setStyleSheet(u"QGroupBox#preferences_group{\n"
                                             "	color: darkgreen;\n"
                                             "	border: 1px solid #c7c8ca;\n"
                                             "	border-radius: 10px;\n"
                                             "	padding: 10px;\n"
                                             "}")
        self.gridLayout_3 = QGridLayout(self.preferences_group)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.videoquality_check = QCheckBox(self.preferences_group)
        self.videoquality_check.setObjectName(u"videoquality_check")
        self.videoquality_check.setFont(font)

        self.gridLayout_3.addWidget(self.videoquality_check, 2, 2, 1, 1)

        self.preferred_audioquality_label = QLabel(self.preferences_group)
        self.preferred_audioquality_label.setObjectName(
            u"preferred_audioquality_label")

        self.gridLayout_3.addWidget(
            self.preferred_audioquality_label, 3, 0, 1, 1)

        self.audioquality_check = QCheckBox(self.preferences_group)
        self.audioquality_check.setObjectName(u"audioquality_check")
        self.audioquality_check.setFont(font)

        self.gridLayout_3.addWidget(self.audioquality_check, 3, 2, 1, 1)

        self.preferred_videoquality_input = QComboBox(self.preferences_group)
        self.preferred_videoquality_input.addItem("")
        self.preferred_videoquality_input.addItem("")
        self.preferred_videoquality_input.addItem("")
        self.preferred_videoquality_input.addItem("")
        self.preferred_videoquality_input.addItem("")
        self.preferred_videoquality_input.addItem("")
        self.preferred_videoquality_input.addItem("")
        self.preferred_videoquality_input.addItem("")
        self.preferred_videoquality_input.setObjectName(
            u"preferred_videoquality_input")
        self.preferred_videoquality_input.setEnabled(False)
        self.preferred_videoquality_input.setFont(font)

        self.gridLayout_3.addWidget(
            self.preferred_videoquality_input, 2, 1, 1, 1)

        self.audioformat_check = QCheckBox(self.preferences_group)
        self.audioformat_check.setObjectName(u"audioformat_check")
        self.audioformat_check.setFont(font)

        self.gridLayout_3.addWidget(self.audioformat_check, 1, 2, 1, 1)

        self.preferred_audioformat_label = QLabel(self.preferences_group)
        self.preferred_audioformat_label.setObjectName(
            u"preferred_audioformat_label")
        self.preferred_audioformat_label.setFont(font)

        self.gridLayout_3.addWidget(
            self.preferred_audioformat_label, 1, 0, 1, 1)

        self.preferred_videoquality_label = QLabel(self.preferences_group)
        self.preferred_videoquality_label.setObjectName(
            u"preferred_videoquality_label")
        self.preferred_videoquality_label.setFont(font)

        self.gridLayout_3.addWidget(
            self.preferred_videoquality_label, 2, 0, 1, 1)

        self.videoformat_check = QCheckBox(self.preferences_group)
        self.videoformat_check.setObjectName(u"videoformat_check")
        self.videoformat_check.setFont(font)

        self.gridLayout_3.addWidget(self.videoformat_check, 0, 2, 1, 1)

        self.preferred_videoformat_input = QComboBox(self.preferences_group)
        self.preferred_videoformat_input.addItem("")
        self.preferred_videoformat_input.addItem("")
        self.preferred_videoformat_input.addItem("")
        self.preferred_videoformat_input.addItem("")
        self.preferred_videoformat_input.setObjectName(
            u"preferred_videoformat_input")
        self.preferred_videoformat_input.setEnabled(False)
        self.preferred_videoformat_input.setFont(font)

        self.gridLayout_3.addWidget(
            self.preferred_videoformat_input, 0, 1, 1, 1)

        self.preferred_videoformat_label = QLabel(self.preferences_group)
        self.preferred_videoformat_label.setObjectName(
            u"preferred_videoformat_label")
        self.preferred_videoformat_label.setFont(font)

        self.gridLayout_3.addWidget(
            self.preferred_videoformat_label, 0, 0, 1, 1)

        self.preferred_audioformat_input = QComboBox(self.preferences_group)
        self.preferred_audioformat_input.addItem("")
        self.preferred_audioformat_input.addItem("")
        self.preferred_audioformat_input.addItem("")
        self.preferred_audioformat_input.setObjectName(
            u"preferred_audioformat_input")
        self.preferred_audioformat_input.setEnabled(False)
        self.preferred_audioformat_input.setFont(font)

        self.gridLayout_3.addWidget(
            self.preferred_audioformat_input, 1, 1, 1, 1)

        self.preferred_audioquality_input = QComboBox(self.preferences_group)
        self.preferred_audioquality_input.addItem("")
        self.preferred_audioquality_input.addItem("")
        self.preferred_audioquality_input.addItem("")
        self.preferred_audioquality_input.addItem("")
        self.preferred_audioquality_input.addItem("")
        self.preferred_audioquality_input.addItem("")
        self.preferred_audioquality_input.setObjectName(
            u"preferred_audioquality_input")
        self.preferred_audioquality_input.setEnabled(False)
        self.preferred_audioquality_input.setFont(font)

        self.gridLayout_3.addWidget(
            self.preferred_audioquality_input, 3, 1, 1, 1)

        self.gridLayout_2.addWidget(self.preferences_group, 0, 0, 1, 1)

        self.lang_group_box = QGroupBox(self.middle_frame_2)
        self.lang_group_box.setObjectName(u"lang_group_box")
        self.lang_group_box.setFont(font)
        self.lang_group_box.setStyleSheet(u"QGroupBox#lang_group_box{\n"
                                          "	color: darkgreen;\n"
                                          "	border: 1px solid #c7c8ca;\n"
                                          "	border-radius: 10px;\n"
                                          "	padding: 10px;\n"
                                          "}")
        self.gridLayout_5 = QGridLayout(self.lang_group_box)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.spanish_radiobtn = QRadioButton(self.lang_group_box)
        self.spanish_radiobtn.setObjectName(u"spanish_radiobtn")
        self.spanish_radiobtn.setFont(font)

        self.gridLayout_5.addWidget(self.spanish_radiobtn, 0, 0, 1, 1)

        self.catalan_radiobtn = QRadioButton(self.lang_group_box)
        self.catalan_radiobtn.setObjectName(u"catalan_radiobtn")
        self.catalan_radiobtn.setFont(font)

        self.gridLayout_5.addWidget(self.catalan_radiobtn, 0, 2, 1, 1)

        self.english_radiobtn = QRadioButton(self.lang_group_box)
        self.english_radiobtn.setObjectName(u"english_radiobtn")
        self.english_radiobtn.setFont(font)

        self.gridLayout_5.addWidget(self.english_radiobtn, 0, 3, 1, 1)

        self.portuguese_radiobtn = QRadioButton(self.lang_group_box)
        self.portuguese_radiobtn.setObjectName(u"portuguese_radiobtn")
        self.portuguese_radiobtn.setFont(font)

        self.gridLayout_5.addWidget(self.portuguese_radiobtn, 0, 4, 1, 1)

        self.gridLayout_2.addWidget(self.lang_group_box, 2, 0, 1, 1)

        self.verticalLayout.addWidget(self.middle_frame_2)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.footer_frame = QFrame(self.content_container_frame)
        self.footer_frame.setObjectName(u"footer_frame")
        self.footer_frame.setMinimumSize(QSize(0, 70))
        self.footer_frame.setFrameShape(QFrame.StyledPanel)
        self.footer_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.footer_frame)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer = QSpacerItem(
            473, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.accept_push_button = QPushButton(self.footer_frame)
        self.accept_push_button.setObjectName(u"accept_push_button")
        self.accept_push_button.setMinimumSize(QSize(0, 30))
        self.accept_push_button.setFont(font)

        self.horizontalLayout_7.addWidget(self.accept_push_button)

        self.apply_push_button = QPushButton(self.footer_frame)
        self.apply_push_button.setObjectName(u"apply_push_button")
        self.apply_push_button.setMinimumSize(QSize(0, 30))
        self.apply_push_button.setFont(font)
        self.apply_push_button.setStyleSheet(u"padding: 5px;")

        self.horizontalLayout_7.addWidget(self.apply_push_button)

        self.cancel_push_button = QPushButton(self.footer_frame)
        self.cancel_push_button.setObjectName(u"cancel_push_button")
        self.cancel_push_button.setMinimumSize(QSize(0, 30))
        self.cancel_push_button.setFont(font)

        self.horizontalLayout_7.addWidget(self.cancel_push_button)

        self.verticalLayout.addWidget(self.footer_frame)

        self.gridLayout.addWidget(self.content_container_frame, 0, 0, 1, 1)

        Settings.setCentralWidget(self.centralwidget)

        self.retranslateUi(Settings)

        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate(
            "Settings", u"PyDownload | Configuraci\u00f3n", None))
        self.welcome_label.setText(QCoreApplication.translate(
            "Settings", u"<html><head/><body><p><span style=\" font-size:12pt; color:#717171;\">Configuraci\u00f3n de la aplicaci\u00f3n</span></p></body></html>", None))
        self.status_label.setText(QCoreApplication.translate(
            "Settings", u"<html><head/><body><p><span style=\" color:#717171;\">No hay cambios.</span></p></body></html>", None))
# if QT_CONFIG(tooltip)
        self.customization_buttons_group.setToolTip(QCoreApplication.translate(
            "Settings", u"Personalizar la apariencia de la app", None))
#endif // QT_CONFIG(tooltip)
        self.customization_buttons_group.setTitle(
            QCoreApplication.translate("Settings", u"Personalizaci\u00f3n", None))
        self.light_theme_radio.setText(QCoreApplication.translate(
            "Settings", u"Tema predeterminado", None))
        self.dark_theme_radio.setText(
            QCoreApplication.translate("Settings", u"Tema oscuro", None))
# if QT_CONFIG(tooltip)
        self.downloads_path_group.setToolTip(QCoreApplication.translate(
            "Settings", u"La ruta de descargas de m\u00fasica y v\u00eddeos", None))
#endif // QT_CONFIG(tooltip)
        self.downloads_path_group.setTitle(
            QCoreApplication.translate("Settings", u"Ruta de descargas", None))
# if QT_CONFIG(tooltip)
        self.file_input.setToolTip(QCoreApplication.translate(
            "Settings", u"Seleccionar archivo...", None))
#endif // QT_CONFIG(tooltip)
        self.file_input.setText(
            QCoreApplication.translate("Settings", u"...", None))
# if QT_CONFIG(tooltip)
        self.download_group_box.setToolTip(QCoreApplication.translate(
            "Settings", u"Preferencias de descarga de la app", None))
#endif // QT_CONFIG(tooltip)
        self.download_group_box.setTitle(
            QCoreApplication.translate("Settings", u"Descarga", None))
        self.min_speed_label.setText(QCoreApplication.translate(
            "Settings", u"Velocidad m\u00ednima:", None))
        self.min_speed_input.setItemText(
            0, QCoreApplication.translate("Settings", u"...", None))
        self.min_speed_input.setItemText(
            1, QCoreApplication.translate("Settings", u"1MB/s", None))
        self.min_speed_input.setItemText(
            2, QCoreApplication.translate("Settings", u"10MB/s", None))
        self.min_speed_input.setItemText(
            3, QCoreApplication.translate("Settings", u"20MB/s", None))
        self.min_speed_input.setItemText(
            4, QCoreApplication.translate("Settings", u"30/MB/s", None))

        self.max_speed_label.setText(QCoreApplication.translate(
            "Settings", u"Velocidad m\u00e1xima:", None))
        self.max_speed_input.setItemText(
            0, QCoreApplication.translate("Settings", u"...", None))
        self.max_speed_input.setItemText(
            1, QCoreApplication.translate("Settings", u"1MB/s", None))
        self.max_speed_input.setItemText(
            2, QCoreApplication.translate("Settings", u"10MB/s", None))
        self.max_speed_input.setItemText(
            3, QCoreApplication.translate("Settings", u"20MB/s", None))
        self.max_speed_input.setItemText(
            4, QCoreApplication.translate("Settings", u"30MB/s", None))

        self.minspeed_check.setText(QCoreApplication.translate(
            "Settings", u"Habilitar / Deshabilitar", None))
        self.max_speed_check.setText(QCoreApplication.translate(
            "Settings", u"Habilitar / Deshabilitar", None))
# if QT_CONFIG(tooltip)
        self.preferences_group.setToolTip(QCoreApplication.translate(
            "Settings", u"Preferencias de la app", None))
#endif // QT_CONFIG(tooltip)
        self.preferences_group.setTitle(
            QCoreApplication.translate("Settings", u"Preferencias", None))
        self.videoquality_check.setText(QCoreApplication.translate(
            "Settings", u"Habilitar / Deshabilitar", None))
        self.preferred_audioquality_label.setText(QCoreApplication.translate(
            "Settings", u"Calidad de audio preferida:", None))
        self.audioquality_check.setText(QCoreApplication.translate(
            "Settings", u"Habilitar / Deshabilitar", None))
        self.preferred_videoquality_input.setItemText(
            0, QCoreApplication.translate("Settings", u"...", None))
        self.preferred_videoquality_input.setItemText(
            1, QCoreApplication.translate("Settings", u"144p", None))
        self.preferred_videoquality_input.setItemText(
            2, QCoreApplication.translate("Settings", u"360p", None))
        self.preferred_videoquality_input.setItemText(
            3, QCoreApplication.translate("Settings", u"480p", None))
        self.preferred_videoquality_input.setItemText(
            4, QCoreApplication.translate("Settings", u"720p", None))
        self.preferred_videoquality_input.setItemText(
            5, QCoreApplication.translate("Settings", u"1080p", None))
        self.preferred_videoquality_input.setItemText(
            6, QCoreApplication.translate("Settings", u"1440p", None))
        self.preferred_videoquality_input.setItemText(
            7, QCoreApplication.translate("Settings", u"2160p", None))

        self.audioformat_check.setText(QCoreApplication.translate(
            "Settings", u"Habilitar / Deshabilitar", None))
        self.preferred_audioformat_label.setText(QCoreApplication.translate(
            "Settings", u"Formato de audio preferido:", None))
        self.preferred_videoquality_label.setText(QCoreApplication.translate(
            "Settings", u"Calidad de v\u00eddeo preferida:", None))
        self.videoformat_check.setText(QCoreApplication.translate(
            "Settings", u"Habilitar / Deshabilitar", None))
        self.preferred_videoformat_input.setItemText(
            0, QCoreApplication.translate("Settings", u"...", None))
        self.preferred_videoformat_input.setItemText(
            1, QCoreApplication.translate("Settings", u"mp4", None))
        self.preferred_videoformat_input.setItemText(
            2, QCoreApplication.translate("Settings", u"3gpp", None))
        self.preferred_videoformat_input.setItemText(
            3, QCoreApplication.translate("Settings", u"webm", None))

        self.preferred_videoformat_label.setText(QCoreApplication.translate(
            "Settings", u"Formato de v\u00eddeo preferido:", None))
        self.preferred_audioformat_input.setItemText(
            0, QCoreApplication.translate("Settings", u"...", None))
        self.preferred_audioformat_input.setItemText(
            1, QCoreApplication.translate("Settings", u"mp3", None))
        self.preferred_audioformat_input.setItemText(
            2, QCoreApplication.translate("Settings", u"webm", None))

        self.preferred_audioquality_input.setItemText(
            0, QCoreApplication.translate("Settings", u"...", None))
        self.preferred_audioquality_input.setItemText(
            1, QCoreApplication.translate("Settings", u"48kbps", None))
        self.preferred_audioquality_input.setItemText(
            2, QCoreApplication.translate("Settings", u"50kbps", None))
        self.preferred_audioquality_input.setItemText(
            3, QCoreApplication.translate("Settings", u"70kbps", None))
        self.preferred_audioquality_input.setItemText(
            4, QCoreApplication.translate("Settings", u"128kbps", None))
        self.preferred_audioquality_input.setItemText(
            5, QCoreApplication.translate("Settings", u"160kbps", None))

# if QT_CONFIG(tooltip)
        self.lang_group_box.setToolTip(QCoreApplication.translate(
            "Settings", u"Lenguajes disponibles", None))
#endif // QT_CONFIG(tooltip)
        self.lang_group_box.setTitle(
            QCoreApplication.translate("Settings", u"Lenguaje", None))
        self.spanish_radiobtn.setText(
            QCoreApplication.translate("Settings", u"Espa\u00f1ol", None))
        self.catalan_radiobtn.setText(
            QCoreApplication.translate("Settings", u"Catal\u00e0", None))
        self.english_radiobtn.setText(
            QCoreApplication.translate("Settings", u"English", None))
        self.portuguese_radiobtn.setText(
            QCoreApplication.translate("Settings", u"Portugu\u00ebs", None))
# if QT_CONFIG(tooltip)
        self.accept_push_button.setToolTip(
            QCoreApplication.translate("Settings", u"Aceptar y salir", None))
#endif // QT_CONFIG(tooltip)
        self.accept_push_button.setText(
            QCoreApplication.translate("Settings", u"Aceptar", None))
# if QT_CONFIG(tooltip)
        self.apply_push_button.setToolTip(
            QCoreApplication.translate("Settings", u"Aplicar cambios", None))
#endif // QT_CONFIG(tooltip)
        self.apply_push_button.setText(QCoreApplication.translate(
            "Settings", u"Aplicar Cambios", None))
# if QT_CONFIG(tooltip)
        self.cancel_push_button.setToolTip(
            QCoreApplication.translate("Settings", u"Cancelar y salir", None))
#endif // QT_CONFIG(tooltip)
        self.cancel_push_button.setText(
            QCoreApplication.translate("Settings", u"Cancelar", None))
    # retranslateUi
