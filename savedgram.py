from time import sleep
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import qApp, QAction, QGridLayout, QLabel, QLayout, QLineEdit, QMainWindow, QMenu, QPushButton, QSystemTrayIcon, QWidget, QFileDialog
from qtwidgets import PasswordEdit

from start_bot import startBot
from logo import LOGO
from user_settings import get_settings, save_settings


class Savedgram(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
 
        self.setMinimumSize(QSize(440, 100))
        self.setWindowTitle("Savedgram")
        
        icon = QPixmap()
        icon.loadFromData(LOGO)
        icon = QIcon(icon)

        self.setWindowIcon(icon)

        self.centralwidget = QWidget(self)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setContextMenuPolicy(Qt.NoContextMenu)
        self.centralwidget.setObjectName("centralwidget")
        
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout.setObjectName("gridLayout")
        
        self.lbl_folder = QLabel(self.centralwidget)
        self.lbl_folder.setObjectName("lbl_folder")
        self.lbl_folder.setText("Folder:")
        self.gridLayout.addWidget(self.lbl_folder, 0, 0, 1, 1)
        
        self.folder = QLineEdit(self.centralwidget)
        self.folder.setObjectName("folder")
        self.folder.setEnabled(False)
        self.gridLayout.addWidget(self.folder, 0, 1, 1, 1)
        
        self.open = QPushButton(self.centralwidget)
        self.open.setObjectName("open")
        self.open.setText("Open")
        self.open.clicked.connect(self._open)
        self.gridLayout.addWidget(self.open, 0, 2, 1, 1)
        
        self.lbl_token = QLabel(self.centralwidget)
        self.lbl_token.setObjectName("lbl_token")
        self.lbl_token.setText("Token:")
        self.gridLayout.addWidget(self.lbl_token, 1, 0, 1, 1)
        
        self.token = PasswordEdit()
        self.token.setObjectName("token")
        self.gridLayout.addWidget(self.token, 1, 1, 1, 2)
        
        self.start = QPushButton(self.centralwidget)
        self.start.setObjectName("start")
        self.start.setText("Start")
        self.start.clicked.connect(self._start)
        self.gridLayout.addWidget(self.start, 2, 0, 1, 3)
        
        self.setCentralWidget(self.centralwidget)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(icon)
        
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)
        
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.startBot = startBot(mainwindow=self)
        self.startBot.show.connect(self.close_thread)
        
        token, folder = get_settings()
        self.token.setText(token)
        self.folder.setText(folder)
        

    def _open(self):
        folder = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folder:
            self.folder.setText(folder)

    def _start(self):
        if self.start.text() == "Start":
            self.hide()
            self.startBot.start()
            sleep(3)
            if self.start.text() == "Stop":
                save_settings(self.token.text(), self.folder.text())
        elif self.start.text() == "Stop":
            self.startBot.terminate()
            self.start.setText("Start")
            self.open.setEnabled(True)
            self.token.setEnabled(True)
            self.tray_icon.showMessage("User Info:", "Savedgram stopped by User")
    
    def close_thread(self):
        self.show()
        self.open.setEnabled(True)
        self.token.setEnabled(True)
        self.tray_icon.showMessage("User Info:", "Any error. Check Internet connection and Settings. Savedgram is stopped")
        self.startBot.terminate()
