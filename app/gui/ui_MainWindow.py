# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'MainWindowUKnJmI.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
                               QLabel, QLineEdit, QMainWindow, QPushButton,
                               QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import images_rc
import images_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1116, 778)
        font = QFont()
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget#centralwidget{\n"
                                         "	background:  #F6F6F6;\n"
                                         "}")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.sidebar_frame = QFrame(self.centralwidget)
        self.sidebar_frame.setObjectName(u"sidebar_frame")
        self.sidebar_frame.setMaximumSize(QSize(92, 16777215))
        self.verticalLayout = QVBoxLayout(self.sidebar_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.sidebar_logo_frame = QFrame(self.sidebar_frame)
        self.sidebar_logo_frame.setObjectName(u"sidebar_logo_frame")
        self.sidebar_logo_frame.setMaximumSize(QSize(16777215, 64))
        self.verticalLayout_2 = QVBoxLayout(self.sidebar_logo_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.logo = QLabel(self.sidebar_logo_frame)
        self.logo.setObjectName(u"logo")
        self.logo.setPixmap(QPixmap(u":/res/images/download.png"))
        self.logo.setScaledContents(True)

        self.verticalLayout_2.addWidget(self.logo)

        self.verticalLayout.addWidget(self.sidebar_logo_frame)

        self.sidebar_line = QFrame(self.sidebar_frame)
        self.sidebar_line.setObjectName(u"sidebar_line")
        self.sidebar_line.setStyleSheet(u"background: darkgreen;")
        self.sidebar_line.setFrameShape(QFrame.HLine)
        self.sidebar_line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.sidebar_line)

        self.sidebar_buttons_frame = QFrame(self.sidebar_frame)
        self.sidebar_buttons_frame.setObjectName(u"sidebar_buttons_frame")
        self.verticalLayout_7 = QVBoxLayout(self.sidebar_buttons_frame)
        self.verticalLayout_7.setSpacing(30)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.download_manager_button = QPushButton(self.sidebar_buttons_frame)
        self.download_manager_button.setObjectName(u"download_manager_button")
        self.download_manager_button.setStyleSheet(u"QPushButton{\n"
                                                   "	padding: 10px;\n"
                                                   "	border: 0.6px solid #CECECE;\n"
                                                   "	border-radius: 5px;\n"
                                                   "	background: white;\n"
                                                   "}\n"
                                                   "\n"
                                                   "QPushButton:hover{\n"
                                                   "	border: 0.6px solid #0078D4;\n"
                                                   "	background: #DEECF7;\n"
                                                   "}\n"
                                                   "\n"
                                                   "QPushButton:pressed{\n"
                                                   "	border: 0.6px solid #CECECE;\n"
                                                   "	background: rgba(255, 255, 255, 10);\n"
                                                   "}")
        icon = QIcon()
        icon.addFile(u":/res/images/manager.png",
                     QSize(), QIcon.Normal, QIcon.Off)
        self.download_manager_button.setIcon(icon)
        self.download_manager_button.setIconSize(QSize(32, 32))

        self.verticalLayout_7.addWidget(self.download_manager_button)

        self.download_history_button = QPushButton(self.sidebar_buttons_frame)
        self.download_history_button.setObjectName(u"download_history_button")
        self.download_history_button.setStyleSheet(u"QPushButton{\n"
                                                   "	padding: 10px;\n"
                                                   "	border: 0.6px solid #CECECE;\n"
                                                   "	border-radius: 5px;\n"
                                                   "	background: white;\n"
                                                   "}\n"
                                                   "\n"
                                                   "QPushButton:hover{\n"
                                                   "	border: 0.6px solid #0078D4;\n"
                                                   "	background: #DEECF7;\n"
                                                   "}\n"
                                                   "\n"
                                                   "QPushButton:pressed{\n"
                                                   "	border: 0.6px solid #CECECE;\n"
                                                   "	background: rgba(255, 255, 255, 10);\n"
                                                   "}")
        icon1 = QIcon()
        icon1.addFile(u":/res/images/history.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        self.download_history_button.setIcon(icon1)
        self.download_history_button.setIconSize(QSize(32, 32))

        self.verticalLayout_7.addWidget(self.download_history_button)

        self.settings_button = QPushButton(self.sidebar_buttons_frame)
        self.settings_button.setObjectName(u"settings_button")
        self.settings_button.setStyleSheet(u"QPushButton{\n"
                                           "	padding: 10px;\n"
                                           "	border: 0.6px solid #CECECE;\n"
                                           "	border-radius: 5px;\n"
                                           "	background: white;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:hover{\n"
                                           "	border: 0.6px solid #0078D4;\n"
                                           "	background: #DEECF7;\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:pressed{\n"
                                           "	border: 0.6px solid #CECECE;\n"
                                           "	background: rgba(255, 255, 255, 10);\n"
                                           "}")
        icon2 = QIcon()
        icon2.addFile(u":/res/images/setting.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        self.settings_button.setIcon(icon2)
        self.settings_button.setIconSize(QSize(32, 32))

        self.verticalLayout_7.addWidget(self.settings_button)

        self.about_button = QPushButton(self.sidebar_buttons_frame)
        self.about_button.setObjectName(u"about_button")
        self.about_button.setStyleSheet(u"QPushButton{\n"
                                        "	padding: 10px;\n"
                                        "	border: 0.6px solid #CECECE;\n"
                                        "	border-radius: 5px;\n"
                                        "	background: white;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "	border: 0.6px solid #0078D4;\n"
                                        "	background: #DEECF7;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed{\n"
                                        "	border: 0.6px solid #CECECE;\n"
                                        "	background: rgba(255, 255, 255, 10);\n"
                                        "}")
        icon3 = QIcon()
        icon3.addFile(u":/res/images/about.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        self.about_button.setIcon(icon3)
        self.about_button.setIconSize(QSize(32, 32))

        self.verticalLayout_7.addWidget(self.about_button)

        self.verticalSpacer = QSpacerItem(
            20, 320, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.verticalLayout.addWidget(self.sidebar_buttons_frame)

        self.gridLayout.addWidget(self.sidebar_frame, 0, 0, 3, 1)

        self.content_container_frame = QFrame(self.centralwidget)
        self.content_container_frame.setObjectName(u"content_container_frame")
        self.content_container_frame.setStyleSheet(u"QFrame#content_container_frame{\n"
                                                   "	border: 2px solid whitesmoke;\n"
                                                   "	border-radius: 30px;\n"
                                                   "	background: white;\n"
                                                   "}")
        self.verticalLayout_3 = QVBoxLayout(self.content_container_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.header_frame = QFrame(self.content_container_frame)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout_2 = QHBoxLayout(self.header_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.welcome_label_frame = QFrame(self.header_frame)
        self.welcome_label_frame.setObjectName(u"welcome_label_frame")
        self.welcome_label_frame.setMaximumSize(QSize(200, 16777215))
        self.horizontalLayout_4 = QHBoxLayout(self.welcome_label_frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.welcome_label = QLabel(self.welcome_label_frame)
        self.welcome_label.setObjectName(u"welcome_label")
        self.welcome_label.setFont(font)

        self.horizontalLayout_4.addWidget(self.welcome_label)

        self.horizontalLayout_2.addWidget(self.welcome_label_frame)

        self.status_label_frame = QFrame(self.header_frame)
        self.status_label_frame.setObjectName(u"status_label_frame")
        self.status_label_frame.setStyleSheet(u"QFrame#status_label_frame{\n"
                                              "	border-radius: 8px;\n"
                                              "	background-color: #F6F8FA;\n"
                                              "}")
        self.horizontalLayout_5 = QHBoxLayout(self.status_label_frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.status_label = QLabel(self.status_label_frame)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setFont(font)
        self.status_label.setStyleSheet(u"QLabel#status_label{\n"
                                        "	margin-top: 5px;\n"
                                        "}")

        self.horizontalLayout_5.addWidget(self.status_label)

        self.horizontalLayout_2.addWidget(self.status_label_frame)

        self.restart_push_button = QPushButton(self.header_frame)
        self.restart_push_button.setObjectName(u"restart_push_button")
        self.restart_push_button.setMinimumSize(QSize(0, 30))
        self.restart_push_button.setFont(font)

        self.horizontalLayout_2.addWidget(self.restart_push_button)

        self.exit_push_button = QPushButton(self.header_frame)
        self.exit_push_button.setObjectName(u"exit_push_button")
        self.exit_push_button.setMinimumSize(QSize(0, 30))
        font1 = QFont()
        font1.setBold(True)
        self.exit_push_button.setFont(font1)
        self.exit_push_button.setStyleSheet(u"color: darkred;")

        self.horizontalLayout_2.addWidget(self.exit_push_button)

        self.verticalLayout_3.addWidget(self.header_frame)

        self.header_line = QFrame(self.content_container_frame)
        self.header_line.setObjectName(u"header_line")
        self.header_line.setStyleSheet(u"background-color: darkgreen;\n"
                                       "margin-left: 20px;\n"
                                       "margin-right: 10px;")
        self.header_line.setFrameShape(QFrame.HLine)
        self.header_line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.header_line)

        self.middle_frame = QFrame(self.content_container_frame)
        self.middle_frame.setObjectName(u"middle_frame")
        self.verticalLayout_4 = QVBoxLayout(self.middle_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.url_input_frame = QFrame(self.middle_frame)
        self.url_input_frame.setObjectName(u"url_input_frame")
        self.url_input_frame.setMaximumSize(QSize(16777215, 50))
        self.url_input_frame.setFont(font)
        self.horizontalLayout_3 = QHBoxLayout(self.url_input_frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.url_label = QLabel(self.url_input_frame)
        self.url_label.setObjectName(u"url_label")
        self.url_label.setFont(font)
        self.url_label.setStyleSheet(u"margin-top: 5px;")

        self.horizontalLayout_3.addWidget(self.url_label)

        self.url_input = QLineEdit(self.url_input_frame)
        self.url_input.setObjectName(u"url_input")
        font2 = QFont()
        font2.setPointSize(10)
        self.url_input.setFont(font2)
        self.url_input.setStyleSheet(u"color: darkgreen;")

        self.horizontalLayout_3.addWidget(self.url_input)

        self.title_label = QLabel(self.url_input_frame)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setFont(font1)
        self.title_label.setStyleSheet(u"color: #717171;")

        self.horizontalLayout_3.addWidget(self.title_label)

        self.verticalLayout_4.addWidget(self.url_input_frame)

        self.video_preview_frame = QFrame(self.middle_frame)
        self.video_preview_frame.setObjectName(u"video_preview_frame")
        self.horizontalLayout_6 = QHBoxLayout(self.video_preview_frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.video_preview_widget = QWidget(self.video_preview_frame)
        self.video_preview_widget.setObjectName(u"video_preview_widget")
        self.video_preview_widget.setStyleSheet(u"QWidget#video_preview_widget{\n"
                                                "	border: 1px solid rgb(234, 236, 238);\n"
                                                "	border-radius: 10px;\n"
                                                "}")

        self.horizontalLayout_6.addWidget(self.video_preview_widget)

        self.verticalLayout_4.addWidget(self.video_preview_frame)

        self.verticalLayout_3.addWidget(self.middle_frame)

        self.footer_frame = QFrame(self.content_container_frame)
        self.footer_frame.setObjectName(u"footer_frame")
        self.footer_frame.setMaximumSize(QSize(16777215, 150))
        self.gridLayout_2 = QGridLayout(self.footer_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.details_frame = QFrame(self.footer_frame)
        self.details_frame.setObjectName(u"details_frame")
        self.verticalLayout_6 = QVBoxLayout(self.details_frame)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.lenght_label = QLabel(self.details_frame)
        self.lenght_label.setObjectName(u"lenght_label")
        self.lenght_label.setFont(font2)

        self.verticalLayout_6.addWidget(self.lenght_label)

        self.publish_date_label = QLabel(self.details_frame)
        self.publish_date_label.setObjectName(u"publish_date_label")
        self.publish_date_label.setFont(font2)

        self.verticalLayout_6.addWidget(self.publish_date_label)

        self.rating_label = QLabel(self.details_frame)
        self.rating_label.setObjectName(u"rating_label")
        self.rating_label.setFont(font2)

        self.verticalLayout_6.addWidget(self.rating_label)

        self.views_label = QLabel(self.details_frame)
        self.views_label.setObjectName(u"views_label")
        self.views_label.setFont(font2)

        self.verticalLayout_6.addWidget(self.views_label)

        self.gridLayout_2.addWidget(self.details_frame, 0, 1, 1, 1)

        self.details_labels_frame = QFrame(self.footer_frame)
        self.details_labels_frame.setObjectName(u"details_labels_frame")
        self.verticalLayout_5 = QVBoxLayout(self.details_labels_frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.llabel = QLabel(self.details_labels_frame)
        self.llabel.setObjectName(u"llabel")
        self.llabel.setFont(font)

        self.verticalLayout_5.addWidget(self.llabel)

        self.pdlabel = QLabel(self.details_labels_frame)
        self.pdlabel.setObjectName(u"pdlabel")
        self.pdlabel.setFont(font)

        self.verticalLayout_5.addWidget(self.pdlabel)

        self.rlabel = QLabel(self.details_labels_frame)
        self.rlabel.setObjectName(u"rlabel")
        self.rlabel.setFont(font)

        self.verticalLayout_5.addWidget(self.rlabel)

        self.vlabel = QLabel(self.details_labels_frame)
        self.vlabel.setObjectName(u"vlabel")
        self.vlabel.setFont(font)

        self.verticalLayout_5.addWidget(self.vlabel)

        self.gridLayout_2.addWidget(self.details_labels_frame, 0, 0, 1, 1)

        self.download_button_frame = QFrame(self.footer_frame)
        self.download_button_frame.setObjectName(u"download_button_frame")
        self.horizontalLayout = QHBoxLayout(self.download_button_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 6)
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.add_to_queue_button = QPushButton(self.download_button_frame)
        self.add_to_queue_button.setObjectName(u"add_to_queue_button")
        self.add_to_queue_button.setMinimumSize(QSize(200, 30))
        self.add_to_queue_button.setMaximumSize(QSize(16777215, 16777215))
        self.add_to_queue_button.setFont(font)

        self.horizontalLayout.addWidget(self.add_to_queue_button)

        self.gridLayout_2.addWidget(self.download_button_frame, 1, 1, 1, 1)

        self.verticalLayout_3.addWidget(self.footer_frame)

        self.gridLayout.addWidget(self.content_container_frame, 0, 1, 3, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"PyDownload", None))
        self.logo.setText("")
# if QT_CONFIG(tooltip)
        self.download_manager_button.setToolTip(
            QCoreApplication.translate("MainWindow", u"Descargas en curso", None))
#endif // QT_CONFIG(tooltip)
        self.download_manager_button.setText("")
# if QT_CONFIG(tooltip)
        self.download_history_button.setToolTip(QCoreApplication.translate(
            "MainWindow", u"Historial de descargas", None))
#endif // QT_CONFIG(tooltip)
        self.download_history_button.setText("")
# if QT_CONFIG(tooltip)
        self.settings_button.setToolTip(QCoreApplication.translate(
            "MainWindow", u"Configuraci\u00f3n", None))
#endif // QT_CONFIG(tooltip)
        self.settings_button.setText("")
# if QT_CONFIG(tooltip)
        self.about_button.setToolTip(QCoreApplication.translate(
            "MainWindow", u"Acerca de la app", None))
#endif // QT_CONFIG(tooltip)
        self.about_button.setText("")
        self.welcome_label.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; color:#717171;\">Bienvenido a PyDownload</span></p></body></html>", None))
        self.status_label.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#717171;\">Introduzca la direcci\u00f3n URL de su v\u00eddeo de YouTube para comenzar la descarga.</span></p></body></html>", None))
# if QT_CONFIG(tooltip)
        self.restart_push_button.setToolTip(QCoreApplication.translate(
            "MainWindow", u"Reiniciar la aplicaci\u00f3n", None))
#endif // QT_CONFIG(tooltip)
        self.restart_push_button.setText(
            QCoreApplication.translate("MainWindow", u"REINICIAR", None))
# if QT_CONFIG(tooltip)
        self.exit_push_button.setToolTip(QCoreApplication.translate(
            "MainWindow", u"Salir de la aplicaci\u00f3n", None))
#endif // QT_CONFIG(tooltip)
        self.exit_push_button.setText(
            QCoreApplication.translate("MainWindow", u"SALIR", None))
        self.url_label.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" color:#717171;\">URL:</span></p></body></html>", None))
        self.title_label.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.lenght_label.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.publish_date_label.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.rating_label.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.views_label.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.llabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700; color:#717171;\">Duraci\u00f3n</span></p></body></html>", None))
        self.pdlabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700; color:#717171;\">Fecha de Publicaci\u00f3n</span></p></body></html>", None))
        self.rlabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700; color:#717171;\">Valoraci\u00f3n</span></p></body></html>", None))
        self.vlabel.setText(QCoreApplication.translate(
            "MainWindow", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700; color:#717171;\">Visualizaciones</span></p></body></html>", None))
# if QT_CONFIG(tooltip)
        self.add_to_queue_button.setToolTip(QCoreApplication.translate(
            "MainWindow", u"Agregar a la cola de descargas", None))
#endif // QT_CONFIG(tooltip)
        self.add_to_queue_button.setText(QCoreApplication.translate(
            "MainWindow", u"Agregar a la cola", None))
    # retranslateUi
