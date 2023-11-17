from PyQt5.QtWidgets import QMainWindow, QTabWidget, QToolBar, QAction
from PyQt5.QtGui import QIcon

class TabsMethods:
    def __init__(self):
        super().__init__()

    @staticmethod
    def create_tabs(fun: QMainWindow):
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabsClosable(True)
        tabs.tabBarDoubleClicked.connect(fun.tab_open_doubleclick)
        tabs.currentChanged.connect(fun.current_tab_changed)
        tabs.tabCloseRequested.connect(fun.close_current_tab)
        
        with open("assets/css/tabBar.css", "r") as style:
            tabs.setStyleSheet(style.read())

        return tabs

    @staticmethod
    def create_navigation_toolbar(parent: QMainWindow):
        def goBack():
            parent.tabs.currentWidget().back()

        def goForward():
            parent.tabs.currentWidget().forward()
            
        def reload():
            parent.tabs.currentWidget().reload()
            
        nav_toolbar = QToolBar("Navegação")
        nav_toolbar.setMovable(False)
        
        back_action = QAction(QIcon('./assets/icons/toolbar/back.png'), 'Voltar uma página', parent)
        back_action.triggered.connect(goBack)
        
        front_action = QAction(QIcon('./assets/icons/toolbar/forward.png'), 'Avançar uma página', parent)
        front_action.triggered.connect(goForward)
        
        reload_action = QAction(QIcon('./assets/icons/toolbar/reload.png'), 'Recarregar a página', parent)
        reload_action.setShortcut('Ctrl+R')
        reload_action.triggered.connect(reload)
        
        ssl_certification = QAction(QIcon('./assets/icons/toolbar/ssl_certification'), 'A página é segura', parent)
        
        
        nav_toolbar.addAction(back_action)
        nav_toolbar.addAction(front_action)
        
        nav_toolbar.addAction(reload_action)
        
        nav_toolbar.addSeparator()
        
        nav_toolbar.addAction(ssl_certification)
        
        return nav_toolbar