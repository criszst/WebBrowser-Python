from PyQt5.QtWidgets import QMainWindow, QToolBar, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl

from methods.database_methods import DBMethods
from history.history import WindowHistory
from config.config import ConfigPage
from methods.json_methods import ConfigMethods

import sqlite3

class SideBarMethods(QMainWindow):
    def __init__(self):
        super().__init__()
        self.historyRequested = None
        self.configRequested = None


    def create_sidebar(self, main: QMainWindow):
        sidebar = QToolBar("Barra Lateral")
        sidebar.setMovable(False)
        
        main.label.setText(f"Zoom atual: {DBMethods().getCurrentZoomPage(main.tabs.currentWidget().page().url()):.1f}")
        
        def goToHome():
            main.tabs.currentWidget().setUrl(QUrl(ConfigMethods().loadJson()['homeURL']))
            
        def history():
            if self.historyRequested is None:
                self.historyRequested = WindowHistory()
                self.historyRequested.show()
            else:
                self.historyRequested.close()
                self.historyRequested = None
                

        def zoomIn():
            current_tab = main.tabs.currentWidget()
            current_tab.setZoomFactor(main.tabs.currentWidget().zoomFactor() + 0.1)
            
            urlTOStr = DBMethods().convertUrlToStr(main.tabs.currentWidget().page().url())

            DBMethods().replaceOldData('zoom', 'url', urlTOStr, 1)
                
            DBMethods().insert(
                'INSERT INTO zoom(url, zoomFactor) VALUES (:url, :zoomFactor)',
                {"url": urlTOStr, "zoomFactor": current_tab.zoomFactor()}
                              )
                
            main.label.setText(f"Zoom atual: {current_tab.zoomFactor():.1f}")
            
            
        def zoomOut():
            current_tab = main.tabs.currentWidget()
            current_tab.setZoomFactor(main.tabs.currentWidget().zoomFactor() - 0.1)
            
            urlTOStr = DBMethods().convertUrlToStr(main.tabs.currentWidget().page().url())
            
            DBMethods().replaceOldData('zoom', 'url', urlTOStr, 1)
            
            DBMethods().insert(
                'INSERT INTO zoom(url, zoomFactor) VALUES (:url, :zoomFactor)',
                {"url": urlTOStr, "zoomFactor": current_tab.zoomFactor()}
                              )
                
            main.label.setText(f"Zoom atual: {current_tab.zoomFactor():.1f}")
            print(psutil.virtual_memory().percent)
            
            
        def showConfig():
         if self.configRequested is None:
                self.configRequested = ConfigPage()
                self.configRequested.show()
         else:
                self.configRequested.close()
                self.configRequested = None


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
        config_btn.clicked.connect(showConfig)
        
        
    
        sidebar.addWidget(home_btn)
        sidebar.addSeparator()
        
        sidebar.addWidget(history_btn)
        sidebar.addSeparator()
        
        sidebar.addWidget(zoomIn_btn)
        sidebar.addSeparator()
        
        sidebar.addWidget(zoomOut_btn)
        sidebar.addSeparator()

        sidebar.addWidget(config_btn)

        
        with open('assets/css/sidebar.css', 'r') as css_file:
            stylesheet = css_file.read()
        sidebar.setStyleSheet(stylesheet)
        
        return sidebar