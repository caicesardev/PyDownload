# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'ManagergEnled.ui'
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
                               QLabel, QMainWindow, QPushButton, QScrollArea,
                               QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)
import images_rc


class Ui_Manager(object):
    def setupUi(self, Manager):
        if not Manager.objectName():
            Manager.setObjectName(u"Manager")
        Manager.resize(1014, 726)
        font = QFont()
        Manager.setFont(font)
        self.centralwidget = QWidget(Manager)
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
        self.verticalLayout = QVBoxLayout(self.content_container_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header_frame = QFrame(self.content_container_frame)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout = QHBoxLayout(self.header_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.image = QLabel(self.header_frame)
        self.image.setObjectName(u"image")
        self.image.setMaximumSize(QSize(32, 32))
        self.image.setPixmap(QPixmap(u":/res/images/manager.png"))
        self.image.setScaledContents(True)

        self.horizontalLayout.addWidget(self.image)

        self.welcome_label_frame = QFrame(self.header_frame)
        self.welcome_label_frame.setObjectName(u"welcome_label_frame")
        self.welcome_label_frame.setMaximumSize(QSize(160, 16777215))
        self.horizontalLayout_4 = QHBoxLayout(self.welcome_label_frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.welcome_label = QLabel(self.welcome_label_frame)
        self.welcome_label.setObjectName(u"welcome_label")
        self.welcome_label.setFont(font)

        self.horizontalLayout_4.addWidget(self.welcome_label)

        self.horizontalLayout.addWidget(self.welcome_label_frame)

        self.status_label_frame = QFrame(self.header_frame)
        self.status_label_frame.setObjectName(u"status_label_frame")
        self.status_label_frame.setStyleSheet(u"QFrame#status_label_frame{\n"
                                              "	border: 1px solid white;\n"
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

        self.horizontalLayout.addWidget(self.status_label_frame)

        self.resume_all_button = QPushButton(self.header_frame)
        self.resume_all_button.setObjectName(u"resume_all_button")
        self.resume_all_button.setMinimumSize(QSize(0, 30))
        self.resume_all_button.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout.addWidget(self.resume_all_button)

        self.stop_all_button = QPushButton(self.header_frame)
        self.stop_all_button.setObjectName(u"stop_all_button")
        self.stop_all_button.setMinimumSize(QSize(0, 30))
        self.stop_all_button.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout.addWidget(self.stop_all_button)

        self.cancel_all_button = QPushButton(self.header_frame)
        self.cancel_all_button.setObjectName(u"cancel_all_button")
        self.cancel_all_button.setMinimumSize(QSize(0, 30))
        self.cancel_all_button.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout.addWidget(self.cancel_all_button)

        self.verticalLayout.addWidget(self.header_frame)

        self.header_line = QFrame(self.content_container_frame)
        self.header_line.setObjectName(u"header_line")
        self.header_line.setStyleSheet(u"background-color: darkgreen;\n"
                                       "margin-left: 15px;\n"
                                       "margin-right: 10px;")
        self.header_line.setFrameShape(QFrame.HLine)
        self.header_line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.header_line)

        self.middle_frame = QFrame(self.content_container_frame)
        self.middle_frame.setObjectName(u"middle_frame")
        self.verticalLayout_2 = QVBoxLayout(self.middle_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, -1, 0)
        self.manager_frame = QFrame(self.middle_frame)
        self.manager_frame.setObjectName(u"manager_frame")
        self.manager_frame.setFont(font)
        self.verticalLayout_3 = QVBoxLayout(self.manager_frame)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.manager_scroll_area = QScrollArea(self.manager_frame)
        self.manager_scroll_area.setObjectName(u"manager_scroll_area")
        self.manager_scroll_area.setStyleSheet(u"QScrollArea#manager_scroll_area{\n"
                                               "	background: #F0F0F0;\n"
                                               "	border-radius: 20px;\n"
                                               "	padding: 5px;\n"
                                               "}")
        self.manager_scroll_area.setFrameShape(QFrame.NoFrame)
        self.manager_scroll_area.setWidgetResizable(True)
        self.manager_content_widget = QWidget()
        self.manager_content_widget.setObjectName(u"manager_content_widget")
        self.manager_content_widget.setGeometry(QRect(0, 0, 942, 547))
        self.verticalLayout_4 = QVBoxLayout(self.manager_content_widget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer = QSpacerItem(
            20, 526, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.manager_scroll_area.setWidget(self.manager_content_widget)

        self.verticalLayout_3.addWidget(self.manager_scroll_area)

        self.verticalLayout_2.addWidget(self.manager_frame)

        self.verticalLayout.addWidget(self.middle_frame)

        self.footer_frame = QFrame(self.content_container_frame)
        self.footer_frame.setObjectName(u"footer_frame")
        self.footer_frame.setMaximumSize(QSize(16777215, 70))
        self.horizontalLayout_2 = QHBoxLayout(self.footer_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(
            870, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.accept_button = QPushButton(self.footer_frame)
        self.accept_button.setObjectName(u"accept_button")
        self.accept_button.setMinimumSize(QSize(0, 30))

        self.horizontalLayout_2.addWidget(self.accept_button)

        self.verticalLayout.addWidget(self.footer_frame)

        self.gridLayout.addWidget(self.content_container_frame, 0, 0, 1, 1)

        Manager.setCentralWidget(self.centralwidget)

        self.retranslateUi(Manager)

        QMetaObject.connectSlotsByName(Manager)
    # setupUi

    def retranslateUi(self, Manager):
        Manager.setWindowTitle(QCoreApplication.translate(
            "Manager", u"PyDownload | Gestor", None))
        self.image.setText("")
        self.welcome_label.setText(QCoreApplication.translate(
            "Manager", u"<html><head/><body><p><span style=\" font-size:11pt; color:#717171;\">Gestor de Descargas</span></p></body></html>", None))
        self.status_label.setText(QCoreApplication.translate(
            "Manager", u"<html><head/><body><p><span style=\" color:#717171;\">No hay ninguna descarga por el momento.</span></p></body></html>", None))
        self.resume_all_button.setText(
            QCoreApplication.translate("Manager", u"Reanudar todo", None))
        self.stop_all_button.setText(
            QCoreApplication.translate("Manager", u"Pausar todo", None))
        self.cancel_all_button.setText(
            QCoreApplication.translate("Manager", u"Cancelar todo", None))
        self.accept_button.setText(
            QCoreApplication.translate("Manager", u"Aceptar", None))
    # retranslateUi
