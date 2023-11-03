from PyQt5.QtWidgets import QGridLayout, QWidget, QPushButton, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl

import sqlite3
import navbar

conn = sqlite3.connect("browserHistory.db", check_same_thread=False)
cursor = conn.cursor()

class WindowHistory(QWidget):
    
    def __init__(self):
        super().__init__()
        layout = QGridLayout()

        self.closeBtn = QPushButton()
        self.closeBtn.setIcon(QIcon('./assets/icons/sidebar/closeHistory.png'))
        self.closeBtn.clicked.connect(self.closeHistory)
        
        layout.addWidget(self.closeBtn)
        
        self.historyList = QListWidget()
        self.historyList.itemClicked.connect(self.itemClicked)
        
        self.addItemHistory()

        layout.addWidget(self.historyList)
        
        self.setLayout(layout)    
        self.setGeometry(70, 140, 400, 420)
                                 #Width #Height
        
        self.setWindowFlags(Qt.WindowType.Popup)
        
    def addItemHistory(self):
        data = cursor.execute("SELECT * FROM history")
        siteList = data.fetchall()
        
        for items in siteList:
            siteFormatted = f'{items[1]} - {items[3]}'   
            self.historyList.addItem(siteFormatted)
            
    def itemClicked(self, item):
        siteName = item.text()
        #print(len(siteName)) #28
        date = siteName[len(siteName) - 19:]
        info = cursor.execute(
            "SELECT * FROM history WHERE date = ?", [date]
        )
        
        url = info.fetchall()[0][2]
        
        mainWindow = navbar.NavBar()
        mainWindow.tabs.currentWidget().setUrl(QUrl(url))
        
        
    def closeHistory(self):
        self.close()