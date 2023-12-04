from PyQt5.QtWidgets import QMainWindow, QToolBar, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QCoreApplication

from icecream import ic

from methods.database_methods import DBMethods
from methods.json_methods import ConfigMethods
    
from history.history import HistoryPage
from config.config import ConfigPage
from stats.stats import StatusPage

import psutil

class SideBarMethods(QMainWindow):
    def __init__(self):
        super().__init__()
        self.historyRequested = None
        self.configRequested = None
        self.statsRequested = None


    def create_sidebar(self, main: QMainWindow):
        sidebar = QToolBar("Barra Lateral")
        sidebar.setMovable(False)
        
        main.label.setText(f"Zoom atual: {DBMethods().getCurrentZoomPage(main.tabs.currentWidget().page().url()):.1f}")
        
        def goToHome():
            main.tabs.currentWidget().setUrl(QUrl(ConfigMethods().loadJson()['homeURL']))
            
        def history():
            if self.historyRequested is None:
                self.historyRequested = HistoryPage()
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
            
        
        def stats():            
            if self.statsRequested is None:
                self.statsRequested = StatusPage()
                self.statsRequested.show()
            else:
                self.statsRequested.close()
                self.statsRequested = None

            
        def config():
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
        
        stats_btn = QPushButton()
        stats_btn.setIcon(QIcon('./assets/icons/sidebar/stats.png'))
        stats_btn.setObjectName('stats_btn')
        stats_btn.setToolTip('Mostrar Status do Browser')
        stats_btn.clicked.connect(stats)

        
        config_btn = QPushButton()
        config_btn.setIcon(QIcon('./assets/icons/sidebar/configIcon.png'))
        config_btn.setToolTip('Acessar as configurações')
        config_btn.setObjectName('config_btn')
        config_btn.clicked.connect(config)
        
        
    
        sidebar.addWidget(home_btn)
        sidebar.addSeparator()
        
        sidebar.addWidget(history_btn)
        sidebar.addSeparator()
        
        sidebar.addWidget(zoomIn_btn)
        sidebar.addSeparator()
        
        sidebar.addWidget(zoomOut_btn)
        sidebar.addSeparator()
        
        sidebar.addWidget(stats_btn)
        sidebar.addSeparator()

        sidebar.addWidget(config_btn)

        
        with open('assets/css/sidebar.css', 'r') as css_file:
            stylesheet = css_file.read()
        sidebar.setStyleSheet(stylesheet)
        
        return sidebar