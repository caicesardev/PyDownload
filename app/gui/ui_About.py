# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'AboutoBBDuv.ui'
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
        self.content_container_frame.setFrameShape(QFrame.StyledPanel)
        self.content_container_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.content_container_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_frame = QFrame(self.content_container_frame)
        self.top_frame.setObjectName(u"top_frame")
        self.top_frame.setFrameShape(QFrame.StyledPanel)
        self.top_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.top_frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.logo_frame = QFrame(self.top_frame)
        self.logo_frame.setObjectName(u"logo_frame")
        self.logo_frame.setStyleSheet(u"QFrame#logo_frame{\n"
                                      "	border: 2px solid whitesmoke;\n"
                                      "	border-radius: 30px;\n"
                                      "	background: white;\n"
                                      "}")
        self.logo_frame.setFrameShape(QFrame.StyledPanel)
        self.logo_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.logo_frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.logo = QLabel(self.logo_frame)
        self.logo.setObjectName(u"logo")
        self.logo.setMaximumSize(QSize(210, 210))
        self.logo.setPixmap(QPixmap(u":/res/images/download.png"))
        self.logo.setScaledContents(True)
        self.logo.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.logo)

        self.horizontalLayout.addWidget(self.logo_frame)

        self.app_name_frame = QFrame(self.top_frame)
        self.app_name_frame.setObjectName(u"app_name_frame")
        self.app_name_frame.setStyleSheet(u"QFrame#app_name_frame{\n"
                                          "	border: 2px solid whitesmoke;\n"
                                          "	border-radius: 30px;\n"
                                          "	background: white;\n"
                                          "}")
        self.app_name_frame.setFrameShape(QFrame.StyledPanel)
        self.app_name_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.app_name_frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(15, -1, 15, -1)
        self.label_2 = QLabel(self.app_name_frame)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        self.label_2.setFont(font)

        self.verticalLayout_2.addWidget(self.label_2)

        self.description_label = QLabel(self.app_name_frame)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setFont(font)
        self.description_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.description_label)

        self.line = QFrame(self.app_name_frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.label = QLabel(self.app_name_frame)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout.addWidget(self.app_name_frame)

        self.verticalLayout.addWidget(self.top_frame)

        self.bottom_frame = QFrame(self.content_container_frame)
        self.bottom_frame.setObjectName(u"bottom_frame")
        self.bottom_frame.setStyleSheet(u"QFrame#bottom_frame{\n"
                                        "	border: 2px solid whitesmoke;\n"
                                        "	border-radius: 30px;\n"
                                        "	background: white;\n"
                                        "}")
        self.bottom_frame.setFrameShape(QFrame.StyledPanel)
        self.bottom_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.bottom_frame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.left_bottom_frame = QFrame(self.bottom_frame)
        self.left_bottom_frame.setObjectName(u"left_bottom_frame")
        self.left_bottom_frame.setFrameShape(QFrame.StyledPanel)
        self.left_bottom_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.left_bottom_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.description_label_2 = QLabel(self.left_bottom_frame)
        self.description_label_2.setObjectName(u"description_label_2")
        self.description_label_2.setFont(font)
        self.description_label_2.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.description_label_2.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.description_label_2)

        self.horizontalLayout_3.addWidget(self.left_bottom_frame)

        self.right_bottom_frame = QFrame(self.bottom_frame)
        self.right_bottom_frame.setObjectName(u"right_bottom_frame")
        self.right_bottom_frame.setFrameShape(QFrame.StyledPanel)
        self.right_bottom_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.right_bottom_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.description_label_3 = QLabel(self.right_bottom_frame)
        self.description_label_3.setObjectName(u"description_label_3")
        self.description_label_3.setFont(font)
        self.description_label_3.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.description_label_3.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.description_label_3)

        self.horizontalLayout_3.addWidget(self.right_bottom_frame)

        self.verticalLayout.addWidget(self.bottom_frame)

        self.frame = QFrame(self.content_container_frame)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 50))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.accept_push_button = QPushButton(self.frame)
        self.accept_push_button.setObjectName(u"accept_push_button")
        self.accept_push_button.setMinimumSize(QSize(100, 0))
        self.accept_push_button.setFont(font)
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
        self.label_2.setText(QCoreApplication.translate(
            "About", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700; color:#717171;\">PyDownloader</span></p></body></html>", None))
        self.description_label.setText(QCoreApplication.translate(
            "About", u"<html><head/><body><p><span style=\" color:#717171;\">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque in convallis nulla. Aenean aliquet nulla quis eros luctus feugiat. In a efficitur nisi. Praesent non enim vel diam pulvinar imperdiet. Phasellus imperdiet odio id mi sodales viverra.</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("About", u"<html><head/><body><p><span style=\" color:#717171;\">Praesent porttitor iaculis aliquet. Morbi aliquet nisl quam, quis laoreet sem facilisis ac. Vivamus tristique augue vitae diam mollis maximus. Curabitur tempor quis ipsum eget vestibulum. Quisque mollis dictum tellus eget elementum. Aenean et viverra est, condimentum blandit velit. Fusce viverra nibh turpis, venenatis luctus mauris sollicitudin a. </span></p></body></html>", None))
        self.description_label_2.setText(QCoreApplication.translate(
            "About", u"<html><head/><body><p><span style=\" color:#717171;\">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque in convallis nulla. Aenean aliquet nulla quis eros luctus feugiat. In a efficitur nisi. Praesent non enim vel diam pulvinar imperdiet. Phasellus imperdiet odio id mi sodales viverra.</span></p></body></html>", None))
        self.description_label_3.setText(QCoreApplication.translate(
            "About", u"<html><head/><body><p><span style=\" color:#717171;\">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque in convallis nulla. Aenean aliquet nulla quis eros luctus feugiat. In a efficitur nisi. Praesent non enim vel diam pulvinar imperdiet. Phasellus imperdiet odio id mi sodales viverra.</span></p></body></html>", None))
        self.accept_push_button.setText(
            QCoreApplication.translate("About", u"Aceptar", None))
    # retranslateUi
