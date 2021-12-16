# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'AboutSMLzmu.ui'
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
                               QLabel, QMainWindow, QPushButton, QSizePolicy,
                               QSpacerItem, QVBoxLayout, QWidget)
import images_rc


class Ui_About(object):
    def setupUi(self, About):
        if not About.objectName():
            About.setObjectName(u"About")
        About.resize(934, 607)
        About.setMaximumSize(QSize(934, 607))
        self.centralwidget = QWidget(About)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget#centralwidget{\n"
                                         "	background:  #F6F6F6;\n"
                                         "}")
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
        self.top_frame = QFrame(self.content_container_frame)
        self.top_frame.setObjectName(u"top_frame")
        self.gridLayout_2 = QGridLayout(self.top_frame)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.content_frame = QFrame(self.top_frame)
        self.content_frame.setObjectName(u"content_frame")
        self.gridLayout_3 = QGridLayout(self.content_frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.line = QFrame(self.content_frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout_3.addWidget(self.line, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 0, 0, 1, 1)

        self.logo = QLabel(self.content_frame)
        self.logo.setObjectName(u"logo")
        self.logo.setMaximumSize(QSize(210, 210))
        self.logo.setPixmap(QPixmap(u":/res/images/download.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(Qt.AlignCenter)

        self.gridLayout_3.addWidget(self.logo, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 5, 0, 1, 1)

        self.label = QLabel(self.content_frame)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.gridLayout_3.addWidget(self.label, 3, 0, 1, 1)

        self.useful_links_frame = QFrame(self.content_frame)
        self.useful_links_frame.setObjectName(u"useful_links_frame")
        self.useful_links_frame.setFrameShape(QFrame.StyledPanel)
        self.useful_links_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.useful_links_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.useful_links_frame)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setFamilies([u"Araboto-Normal"])
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_2.setOpenExternalLinks(True)

        self.horizontalLayout.addWidget(self.label_2)

        self.label_3 = QLabel(self.useful_links_frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_3.setOpenExternalLinks(True)

        self.horizontalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(self.useful_links_frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.label_4.setOpenExternalLinks(True)

        self.horizontalLayout.addWidget(self.label_4)

        self.gridLayout_3.addWidget(self.useful_links_frame, 4, 0, 1, 1)

        self.gridLayout_2.addWidget(self.content_frame, 0, 1, 1, 1)

        self.verticalLayout.addWidget(self.top_frame)

        self.frame = QFrame(self.content_container_frame)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.accept_push_button = QPushButton(self.frame)
        self.accept_push_button.setObjectName(u"accept_push_button")
        self.accept_push_button.setMinimumSize(QSize(100, 0))
        font1 = QFont()
        self.accept_push_button.setFont(font1)
        self.accept_push_button.setStyleSheet(u"padding: 5px;")

        self.horizontalLayout_4.addWidget(self.accept_push_button)

        self.verticalLayout.addWidget(self.frame)

        self.gridLayout.addWidget(self.content_container_frame, 0, 0, 1, 1)

        About.setCentralWidget(self.centralwidget)

        self.retranslateUi(About)

        QMetaObject.connectSlotsByName(About)
    # setupUi

    def retranslateUi(self, About):
        About.setWindowTitle(
            QCoreApplication.translate("About", u"About", None))
        self.logo.setText("")
        self.label.setText(QCoreApplication.translate(
            "About", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:700; color:#550000;\">PyDownload</span></p><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Versi\u00f3n 1.0.0</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate(
            "About", u"<html><head/><body><p><a href=\"mailto:caicesardev@gmail.com\"><span style=\" text-decoration: underline; color:#0000ff;\">Contacto</span></a></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate(
            "About", u"<html><head/><body><p><a href=\"mailto:name@email.com\"><span style=\" text-decoration: underline; color:#0000ff;\">Bugs</span></a></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate(
            "About", u"<html><head/><body><p><a href=\"https://www.github.com/caicesardev/PyDownload\"><span style=\" text-decoration: underline; color:#0000ff;\">Repositorio</span></a></p></body></html>", None))
        self.accept_push_button.setText(
            QCoreApplication.translate("About", u"Aceptar", None))
    # retranslateUi
