from PyQt5.QtWidgets import QMainWindow, QTabWidget, QToolBar, QPushButton
from PyQt5.QtGui import QIcon

class TabsMethods(QTabWidget):
    def __init__(self):
        super().__init__()


    def create_tabs(self):
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabsClosable(True)
        
        with open("assets/css/tabBar.css", "r") as style:
            tabs.setStyleSheet(style.read())

        return tabs


    def create_navigation_toolbar(self, parent: QMainWindow):
        def goBack():
            parent.tabs.currentWidget().back()

        def goForward():
            parent.tabs.currentWidget().forward()
            
        def reload():
            parent.tabs.currentWidget().reload()
            
        nav_toolbar = QToolBar("Navegação")
        nav_toolbar.setMovable(False)
        
        back_btn = QPushButton()
        back_btn.setIcon(QIcon('./assets/icons/toolbar/back.png'))
        back_btn.setObjectName('back_btn')
        back_btn.setToolTip('Voltar uma página')
        back_btn.clicked.connect(goBack)
        
        forward_btn = QPushButton()
        forward_btn.setIcon(QIcon('./assets/icons/toolbar/forward.png'))
        forward_btn.setObjectName('forward_btn')
        forward_btn.setToolTip('Avançar uma página')
        forward_btn.clicked.connect(goForward)
        
        reload_btn = QPushButton()
        reload_btn.setIcon(QIcon('./assets/icons/toolbar/reload.png'))
        reload_btn.setObjectName('reload_btn')
        reload_btn.setToolTip('Recarregar a página')
        reload_btn.clicked.connect(reload)
        
        ssl_certification = QPushButton()
        ssl_certification.setIcon(QIcon('./assets/icons/toolbar/ssl_certification.png'))
        ssl_certification.setObjectName('ssl_certification')
        ssl_certification.setToolTip('A página é segura')
        #ssl_certification.clicked.connect(goBack)
        
        
        nav_toolbar.addWidget(back_btn)
        nav_toolbar.addWidget(forward_btn)
        
        nav_toolbar.addWidget(reload_btn)
        
        nav_toolbar.addSeparator()
        
        nav_toolbar.addWidget(ssl_certification)
        
        return nav_toolbar