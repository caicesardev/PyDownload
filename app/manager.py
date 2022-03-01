from gui.ui_Manager import Ui_Manager
from gui.ui_DownloadFrame import Ui_wrapper_frame
from PySide6.QtGui import QShortcut, QKeySequence, QIcon, QFont, QPixmap
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QFrame,
    QMainWindow,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QProgressBar,
    QToolButton)

########################################
########################################
# This file inits the Manager UI.
########################################
########################################


# Manager.
class Manager(QMainWindow, Ui_Manager):
    def __init__(self, f_title="", f_type="", f_size="", d_type="", d_total="", e_time=""):
        super(Manager, self).__init__()

        self.init_ui()

        self.f_title = f_title
        self.f_type = f_type
        self.f_size = f_size
        self.d_type = d_type
        self.d_total = d_total
        self.e_time = e_time

    def init_ui(self):
        self.setupUi(self)
        self.accept_button.clicked.connect(self.close)

        # Shortcuts.
        self.quit_sc = QShortcut(QKeySequence('Ctrl+W'), self)
        self.quit_sc.activated.connect(self.close)

        # VerticalSpacer
        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.add_widget()

        self.verticalLayout_4.addItem(self.verticalSpacer)

    def add_widget(self):
        d_widget = DownloadWidget(self)
        self.verticalLayout_4.addWidget(d_widget)


class DownloadWidget(QFrame, Ui_wrapper_frame):
    def __init__(self, parent):
        super(DownloadWidget, self).__init__(parent)

        self.init_ui()

    def init_ui(self):
        self.setupUi(self)

        # Manually adding some images.
        self.img_label.setPixmap(QPixmap("../res/images/youtube.png"))
        icon, icon1, icon2 = QIcon(), QIcon(), QIcon()
        icon.addFile("../res/images/play.png",
                     QSize(), QIcon.Normal, QIcon.Off)
        icon1.addFile("../res/images/pause.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        icon2.addFile("../res/images/cancel.png",
                      QSize(), QIcon.Normal, QIcon.Off)
        self.play_button.setIcon(icon)
        self.pause_button.setIcon(icon1)
        self.cancel_button.setIcon(icon2)
