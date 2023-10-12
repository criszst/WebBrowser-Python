from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QTabWidget, QToolBar, QAction, QTabBar

class TabsMethods:
    def __init__(self):
        super().__init__()
        
    @staticmethod
    def create_tabs(fun):
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabsClosable(True)
        tabs.tabBarDoubleClicked.connect(fun.tab_open_doubleclick)
        tabs.currentChanged.connect(fun.current_tab_changed)
        tabs.tabCloseRequested.connect(fun.close_current_tab)

        return tabs

    @staticmethod
    def create_navigation_toolbar(parent):
        def goToHome():
            parent.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))
        
        def goBack():
            parent.tabs.currentWidget().back()

    
        def reload():
            parent.tabs.currentWidget().reload()

        def stop():
            parent.tabs.currentWidget().stop()

        def goForward():
            parent.tabs.currentWidget().forward()
            
        nav_toolbar = QToolBar("Navegação")
        
        back_action = QAction('<-', parent)
        back_action.triggered.connect(goBack)
        
        front_action = QAction('->', parent)
        front_action.triggered.connect(goForward)
        
        reload_action = QAction('Recarregar', parent)
        reload_action.triggered.connect(reload)
        
        home_action = QAction('Página Inicial', parent)
        home_action.triggered.connect(goToHome)
        
        stop_action = QAction('Parar Carregamento', parent)
        stop_action.triggered.connect(stop)
        
        history_action = QAction('Historico', parent)
        
        nav_toolbar.addAction(back_action)
        nav_toolbar.addAction(front_action)
        
        nav_toolbar.addAction(reload_action)
        nav_toolbar.addAction(home_action)
        nav_toolbar.addAction(stop_action)
        
        nav_toolbar.addAction(history_action)


        return nav_toolbar

    @staticmethod
    def create_action(text, parent, slot):
        action = QAction(text, parent)
        action.triggered.connect(slot)
        return action
    
