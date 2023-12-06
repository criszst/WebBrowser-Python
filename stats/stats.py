from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QIcon

from icecream import ic

ic.configureOutput(prefix='DEBUG: ')

import psutil

class StatusPage(QWidget):
    def __init__(self):
        super().__init__()
        self.showStats()
        self.setGeometry(640, 170, 700, 720)
    
    def showStats(self) -> None:
       self.closeBtn = QPushButton(self)
       self.closeBtn.setIcon(QIcon('./assets/icons/sidebar/closeHistory.png'))
       self.closeBtn.clicked.connect(self.closeStatus)
       self.closeBtn.setGeometry(5, 10, 690, 30)
       
      
       with open('assets/css/config.css') as file:
            self.setStyleSheet(file.read())
           

       
       ic(psutil.Process().memory_info().rss / (1024 ** 2))
       ic(psutil.Process().cpu_percent())
       
       #self.setGeometry(70, 340, 400, 420)
       QMetaObject.connectSlotsByName(self)
       self.setWindowFlags(Qt.WindowType.Popup)
       
    def closeStatus(self):
        self.close()