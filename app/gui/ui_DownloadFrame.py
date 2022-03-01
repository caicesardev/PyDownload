# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'DownloadFramepjAgxS.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                               QProgressBar, QSizePolicy, QSpacerItem, QToolButton,
                               QVBoxLayout, QWidget)
import images_rc


class Ui_wrapper_frame(object):
    def setupUi(self, wrapper_frame):
        if not wrapper_frame.objectName():
            wrapper_frame.setObjectName(u"wrapper_frame")
        wrapper_frame.resize(744, 134)
        wrapper_frame.setMinimumSize(QSize(383, 127))
        self.verticalLayout = QVBoxLayout(wrapper_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.header_frme = QFrame(wrapper_frame)
        self.header_frme.setObjectName(u"header_frme")
        self.header_frme.setMaximumSize(QSize(16777215, 30))
        self.header_frme.setFrameShape(QFrame.StyledPanel)
        self.header_frme.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.header_frme)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 0)
        self.left_header_horizontal_line = QSpacerItem(
            38, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.left_header_horizontal_line)

        self.title_label = QLabel(self.header_frme)
        self.title_label.setObjectName(u"title_label")
        font = QFont()
        font.setBold(True)
        self.title_label.setFont(font)

        self.horizontalLayout_6.addWidget(self.title_label)

        self.verticalLayout.addWidget(self.header_frme)

        self.middle_frme = QFrame(wrapper_frame)
        self.middle_frme.setObjectName(u"middle_frme")
        self.middle_frme.setMaximumSize(QSize(16777215, 45))
        self.middle_frme.setFrameShape(QFrame.StyledPanel)
        self.middle_frme.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.middle_frme)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.img_label = QLabel(self.middle_frme)
        self.img_label.setObjectName(u"img_label")
        self.img_label.setMaximumSize(QSize(32, 32))
        self.img_label.setPixmap(QPixmap(u":/res/images/youtube.png"))
        self.img_label.setScaledContents(True)

        self.horizontalLayout_3.addWidget(self.img_label)

        self.progress_bar = QProgressBar(self.middle_frme)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setValue(24)

        self.horizontalLayout_3.addWidget(self.progress_bar)

        self.play_button = QToolButton(self.middle_frme)
        self.play_button.setObjectName(u"play_button")
        icon = QIcon()
        icon.addFile(u":/res/images/play.png",
                     QSize(), QIcon.Normal, QIcon.Off)
        self.play_button.setIcon(icon)
        self.play_button.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.play_button)

        self.pause_button = QToolButton(self.middle_frme)
        self.pause_button.setObjectName(u"pause_button")
        icon1 = QIcon()
        icon1.addFile(u":/res/images/pause.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        self.pause_button.setIcon(icon1)
        self.pause_button.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.pause_button)

        self.cancel_button = QToolButton(self.middle_frme)
        self.cancel_button.setObjectName(u"cancel_button")
        icon2 = QIcon()
        icon2.addFile(u":/res/images/cancel.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        self.cancel_button.setIcon(icon2)
        self.cancel_button.setIconSize(QSize(24, 24))

        self.horizontalLayout_3.addWidget(self.cancel_button)

        self.verticalLayout.addWidget(self.middle_frme)

        self.footer_frme = QFrame(wrapper_frame)
        self.footer_frme.setObjectName(u"footer_frme")
        self.footer_frme.setMaximumSize(QSize(16777215, 40))
        self.footer_frme.setFrameShape(QFrame.StyledPanel)
        self.footer_frme.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.footer_frme)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, -1)
        self.left_footer_horizontal_line = QSpacerItem(
            38, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.left_footer_horizontal_line)

        self.etime_label = QLabel(self.footer_frme)
        self.etime_label.setObjectName(u"etime_label")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.etime_label.sizePolicy().hasHeightForWidth())
        self.etime_label.setSizePolicy(sizePolicy)
        self.etime_label.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_7.addWidget(self.etime_label)

        self.txt_line = QFrame(self.footer_frme)
        self.txt_line.setObjectName(u"txt_line")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.txt_line.sizePolicy().hasHeightForWidth())
        self.txt_line.setSizePolicy(sizePolicy1)
        self.txt_line.setMinimumSize(QSize(22, 24))
        self.txt_line.setStyleSheet(u"color: grey;")
        self.txt_line.setFrameShadow(QFrame.Plain)
        self.txt_line.setLineWidth(1)
        self.txt_line.setFrameShape(QFrame.HLine)

        self.horizontalLayout_7.addWidget(self.txt_line)

        self.tdownload_label = QLabel(self.footer_frme)
        self.tdownload_label.setObjectName(u"tdownload_label")
        sizePolicy.setHeightForWidth(
            self.tdownload_label.sizePolicy().hasHeightForWidth())
        self.tdownload_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_7.addWidget(self.tdownload_label)

        self.inetspeed_label = QLabel(self.footer_frme)
        self.inetspeed_label.setObjectName(u"inetspeed_label")
        sizePolicy.setHeightForWidth(
            self.inetspeed_label.sizePolicy().hasHeightForWidth())
        self.inetspeed_label.setSizePolicy(sizePolicy)

        self.horizontalLayout_7.addWidget(self.inetspeed_label)

        self.right_footer_horizontal_line = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.right_footer_horizontal_line)

        self.verticalLayout.addWidget(self.footer_frme)

        self.retranslateUi(wrapper_frame)

        QMetaObject.connectSlotsByName(wrapper_frame)
    # setupUi

    def retranslateUi(self, wrapper_frame):
        wrapper_frame.setWindowTitle(
            QCoreApplication.translate("wrapper_frame", u"Form", None))
        self.title_label.setText(QCoreApplication.translate(
            "wrapper_frame", u"KAROL G - As\u00ed Es El Amor.mp3", None))
# if QT_CONFIG(tooltip)
        self.play_button.setToolTip(QCoreApplication.translate(
            "wrapper_frame", u"Reanudar", None))
#endif // QT_CONFIG(tooltip)
        self.play_button.setText("")
# if QT_CONFIG(tooltip)
        self.pause_button.setToolTip(
            QCoreApplication.translate("wrapper_frame", u"Pausar", None))
#endif // QT_CONFIG(tooltip)
# if QT_CONFIG(tooltip)
        self.cancel_button.setToolTip(
            QCoreApplication.translate("wrapper_frame", u"Cancelar", None))
#endif // QT_CONFIG(tooltip)
        self.etime_label.setText(QCoreApplication.translate(
            "wrapper_frame", u"1m 10s restantes", None))
        self.tdownload_label.setText(QCoreApplication.translate(
            "wrapper_frame", u"44,49 de 73,7MB", None))
        self.inetspeed_label.setText(QCoreApplication.translate(
            "wrapper_frame", u"(1MB/seg)", None))
    # retranslateUi
