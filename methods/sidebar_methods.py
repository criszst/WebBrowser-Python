from re import A
from PyQt5.QtWidgets import QMainWindow, QToolBar, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl

from methods.database_methods import DBMethods
from history import historyPopup

import sqlite3

conn = sqlite3.connect("browser.db", check_same_thread=False)
cursor = conn.cursor()

class SideBarMethods(QMainWindow):
    def __init__(self):
        super().__init__()
        self.historyRequested = None


    def create_sidebar(self, main: QMainWindow):
        sidebar = QToolBar("Barra Lateral")
        sidebar.setMovable(False)
        
        label = QLabel()
        
        current_page = main.tabs.currentWidget()
       # anotherUrl = main.tabs.currentWidget().page().url()
        
        urlTOStr = DBMethods().converUrlToStr(current_page.page().url())
        
        zoom = current_page.zoomFactor
        
        def goToHome():
            main.tabs.currentWidget().setUrl(QUrl('https://www.google.com'))
            
        def history():
            if self.historyRequested is None:
                self.historyRequested = historyPopup.WindowHistory()
                self.historyRequested.show()
            else:
                self.historyRequested.close()
                self.historyRequested = None

        def zoomIn():
            if current_page:
                current_page.setZoomFactor(zoom() + 0.1)
                #DBMethods().replaceOldData('zoom', 'url', urlTOStr, 1)
                cursor.execute(
                    "INSERT INTO zoom (url,zoomFactor) VALUES (:url,:zoomFactor)", 
                    {"url": urlTOStr, "zoomFactor": current_page.zoomFactor()}
                )
                
                conn.commit()
                formatted_zoom = f"Zoom atual: {current_page.zoomFactor():.1f}"
                
                label.setText(formatted_zoom)
                #print(anotherUrl)
                main.nav_toolbar.addWidget(label)
                label.destroy()

        def zoomOut():
            if current_page:
                current_page.setZoomFactor(zoom() - 0.1)
                #DBMethods().replaceOldData('zoom', 'url', urlTOStr, 1)
                cursor.execute(
                    "INSERT INTO zoom (url,zoomFactor) VALUES (:url,:zoomFactor)", 
                    {"url": urlTOStr, "zoomFactor": current_page.zoomFactor()}
                )
                
                conn.commit()
                formatted_zoom = f"Zoom atual: {current_page.zoomFactor():.1f}"
                
                label.setText(formatted_zoom)
                #print(anotherUrl)
                main.nav_toolbar.addWidget(label)
                label.destroy()


        home_btn = QPushButton()
        home_btn.setIcon(QIcon('./assets/icons/sidebar/casa.png'))
        home_btn.setObjectName('home_btn')
        home_btn.setToolTip('Ir para o google')
        home_btn.clicked.connect(goToHome)
        

        history_btn = QPushButton()
        history_btn.setIcon(QIcon('./assets/icons/sidebar/history.png'))
        history_btn.setObjectName('history_btn')
        history_btn.setToolTip('Ver o histórico')
        history_btn.clicked.connect(history)

        
        zoomIn_btn = QPushButton()
        zoomIn_btn.setIcon(QIcon('./assets/icons/sidebar/zoomIn.png'))
        zoomIn_btn.setObjectName('zoomIn_btn')
        zoomIn_btn.setToolTip('Aumentar o zoom')
        zoomIn_btn.clicked.connect(zoomIn)

        
        zoomOut_btn = QPushButton()
        zoomOut_btn.setIcon(QIcon('./assets/icons/sidebar/zoomOut.png'))
        zoomOut_btn.setObjectName('zoomOut_btn')
        zoomOut_btn.setToolTip('Diminuir o zoom')
        zoomOut_btn.clicked.connect(zoomOut)

        
        config_btn = QPushButton()
        config_btn.setIcon(QIcon('./assets/icons/sidebar/configIcon.png'))
        config_btn.setToolTip('Acessar as configurações')
        config_btn.setObjectName('config_btn')
        
        
    
        sidebar.addWidget(home_btn)
        sidebar.addSeparator()
        
        sidebar.addWidget(history_btn)
        sidebar.addSeparator()
        
        sidebar.addWidget(zoomIn_btn)
        sidebar.addSeparator()
        
        sidebar.addWidget(zoomOut_btn)
        sidebar.addSeparator()
        
        for i in range(0, 100):
            sidebar.addSeparator()

        sidebar.addWidget(config_btn)

        
        with open('assets/css/sidebar.css', 'r') as css_file:
            stylesheet = css_file.read()
        sidebar.setStyleSheet(stylesheet)
        
        return sidebar