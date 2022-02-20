from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QProgressBar,
    QToolButton)
from manager import Manager

########################################
########################################
# This file creates dynamic frames for
# the download manager.
########################################
########################################


# Download Frame
class DownloadFrame(QFrame, Manager):
    def __init__(self, f_title, f_type, f_size, d_type, d_total, e_time):
        super(DownloadFrame, self).__init__()

        self.setup_download_frame(
            f_title,
            f_type,
            f_size,
            d_type,
            d_total,
            e_time)

    def setup_download_frame(self, f_title, f_type, f_size, d_type, d_total, e_time):
        #################### GUI DECLARATION ####################

        manager = Manager()

        print(manager.manager_content_widget)

        # Frames.
        self.download_frame = QFrame(manager.manager_content_widget)
        self.head_frame = QFrame(self.download_frame)
        self.mid_frame = QFrame(self.download_frame)
        self.bottom_frame = QFrame(self.download_frame)
        self.line = QFrame(self.download_frame)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setStyleSheet(u"background-color: darkgreen;\n"
                                "margin-left: 15px;\n"
                                "margin-right: 10px;")

        # Layouts.
        self.verticalLayout_5 = QVBoxLayout(self.download_frame)
        self.horizontalLayout_3 = QHBoxLayout(self.head_frame)
        self.horizontalLayout_6 = QHBoxLayout(self.mid_frame)
        self.horizontalLayout_9 = QHBoxLayout(self.bottom_frame)

        # Widgets.
        self.file_title_label = QLabel(self.head_frame)
        self.file_type_label = QLabel(self.head_frame)
        self.file_size_label = QLabel(self.head_frame)
        self.download_type_image = QLabel(self.mid_frame)
        self.download_progress_bar = QProgressBar(self.mid_frame)
        self.play_tool_button = QToolButton(self.mid_frame)
        self.pause_tool_button = QToolButton(self.mid_frame)
        self.cancel_tool_button = QToolButton(self.mid_frame)
        self.total_downloaded_label = QLabel(self.bottom_frame)
        self.estimated_time_label = QLabel(self.bottom_frame)

        # Widget adjustments.
        self.estimated_time_label.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.download_type_image.setMaximumSize(QSize(32, 32))
        self.download_type_image.setScaledContents(True)
        self.horizontal_spacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Fonts.
        font1 = QFont()
        font2 = QFont()
        font3 = QFont()
        font1.setBold(True)
        font2.setPointSize(10)
        font2.setBold(False)
        font3.setPointSize(10)
        self.file_title_label.setFont(font1)
        self.file_type_label.setFont(font2)
        self.file_size_label.setFont(font3)
        self.estimated_time_label.setFont(font3)
        self.total_downloaded_label.setFont(font3)

        # Icons.
        icon = QIcon()
        icon1 = QIcon()
        icon2 = QIcon()

        # Add image to icons.
        icon.addFile(u"../res/images/play.png",
                     QSize(), QIcon.Normal, QIcon.Off)
        icon1.addFile(u"../res/images/pause.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        icon2.addFile(u"../res/images/cancel.png",
                      QSize(), QIcon.Normal, QIcon.Off)

        # Set icons.
        self.play_tool_button.setIcon(icon)
        self.play_tool_button.setIconSize(QSize(24, 24))
        self.pause_tool_button.setIcon(icon1)
        self.pause_tool_button.setIconSize(QSize(24, 24))
        self.cancel_tool_button.setIcon(icon2)
        self.cancel_tool_button.setIconSize(QSize(24, 24))

        # Set tooltips.
        self.play_tool_button.setToolTip("Continuar la descarga")
        self.pause_tool_button.setToolTip("Pausar la descarga")
        self.cancel_tool_button.setToolTip("Cancelar la descarga")

        # Set text.
        self.file_title_label.setText(f_title)
        self.file_type_label.setText(f_type)
        self.file_size_label.setText(f_size)
        self.download_type_image.setPixmap(QPixmap(f"{d_type}"))
        self.total_downloaded_label.setText(d_total)
        self.estimated_time_label.setText(e_time)

        # Add widgets to layouts.
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_3.addWidget(self.file_title_label)
        self.horizontalLayout_3.addItem(self.horizontal_spacer)
        self.horizontalLayout_3.addWidget(self.file_type_label)
        self.horizontalLayout_3.addWidget(self.file_size_label)

        self.verticalLayout_5.addWidget(self.head_frame)
        self.verticalLayout_5.addWidget(self.mid_frame)
        self.verticalLayout_5.addWidget(self.bottom_frame)
        self.verticalLayout_5.addWidget(self.line)

        self.horizontalLayout_6.addWidget(self.download_type_image)
        self.horizontalLayout_6.addWidget(self.download_progress_bar)
        self.horizontalLayout_6.addWidget(self.play_tool_button)
        self.horizontalLayout_6.addWidget(self.pause_tool_button)
        self.horizontalLayout_6.addWidget(self.cancel_tool_button)
        self.horizontalLayout_6.setContentsMargins(-1, -1, -1, 0)

        self.horizontalLayout_9.addWidget(self.estimated_time_label)
        self.horizontalLayout_9.addWidget(self.total_downloaded_label)

        manager.verticalLayout_4.addWidget(self.download_frame)
        manager.horizontalLayout_4.addItem(self.verticalSpacer)

        #################### GUI DECLARATION ####################
