from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtGui import QIcon

class SideBarMethods(QMainWindow):
    def __init__(self):
        super().__init__()

    @staticmethod
    def create_sidebar(main: QMainWindow):
        sidebar = QToolBar("SideBar")
        sidebar.setMovable(False)
        
        def zoomIn():
            main.zoomIn()

        def zoomOut():
            main.zoomOut()
        
        home_action = QAction(QIcon('./assets/icons/sidebar/casa.png'), 'Voltar ao Google', main)
        #home_action.triggered.connect(goBack)
        
        history_action = QAction(QIcon('./assets/icons/sidebar/history.png'), 'Ver o histórico', main)
        #history_action.triggered.connect(goBack)
        
        zoomIn_action = QAction(QIcon('./assets/icons/sidebar/zoomIn.png'), 'Ver o histórico', main)
        zoomIn_action.triggered.connect(zoomIn)
        
        zoomOut_action = QAction(QIcon('./assets/icons/sidebar/zoomOut.png'), 'Ver o histórico', main)
        zoomOut_action.triggered.connect(zoomOut)
        
        config_action = QAction(QIcon('./assets/icons/sidebar/configIcon.png'), 'Ver o histórico', main)
        #config_action.triggered.connect(goBack)
        
        

        home_btn = QPushButton()
        home_btn.setIcon(home_action.icon())
        home_btn.setObjectName('home_btn')


        history_btn = QPushButton()
        history_btn.setIcon(history_action.icon())
        history_btn.setObjectName('history_btn')

        
        zoomIn_btn = QPushButton()
        zoomIn_btn.setIcon(zoomIn_action.icon())
        zoomIn_btn.setObjectName('zoomIn_btn')

        
        zoomOut_btn = QPushButton()
        zoomOut_btn.setIcon(zoomOut_action.icon())
        zoomOut_btn.setObjectName('zoomOut_btn')

        
        config_btn = QPushButton()
        config_btn.setIcon(config_action.icon())
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
