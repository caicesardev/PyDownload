from gui.ui_Manager import Ui_Manager
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QMainWindow

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

    def add_frame(self):
        from download_frame import DownloadFrame
        DownloadFrame(
            self.f_title,
            self.f_type,
            self.f_size,
            self.d_type,
            self.d_total,
            self.e_time)
        print(f"Frame added for video: {self.f_title}")
