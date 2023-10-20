from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QWidget, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView 

from tabsMethods.tabs_methods import TabsMethods
from keyboard import is_pressed

class Tabs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

        
    def init_ui(self): 
        self.tabs = TabsMethods.create_tabs(self)
        self.setCentralWidget(self.tabs)

        nav_toolbar = TabsMethods.create_navigation_toolbar(self)
        nav_toolbar.setMovable(False)

        self.addToolBar(nav_toolbar)
        
        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.goToUrl)
        nav_toolbar.addWidget(self.urlBar)

        self.addNewTab()
        
        self.addShortcut = QShortcut('Ctrl+T', self)
        self.addShortcut.activated.connect(self.addNewTab)
        
        self.closeShortcut = QShortcut('Ctrl+W', self)
        self.closeShortcut.activated.connect(self.close_current_tab)


        self.showMaximized()
        self.setWindowTitle('ACS Browser')

    
    def addNewTab(self, url = None, label="Blank"):
        from handleNetwork.setCookie import Cookie
         
        if url is None or url == ' ':
            url = QUrl('https://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(url)
    

        currentTabIndex = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(currentTabIndex)
              
        browser.urlChanged.connect(lambda url, browser=browser:
                                     self.update_urlBar(url, browser))

        browser.titleChanged.connect(lambda _, i=currentTabIndex, browser=browser:
                                     self.tabs.setTabText(i, self.tabs.currentWidget().page().title()))
        
        browser.loadFinished.connect(lambda _, browser=browser:
                                     self.update_window_title(browser))
        
        browser.iconChanged.connect(lambda _, browser=browser:
                                     self.updateIcon(browser))
        
       # browser.page().profile().cookieStore().cookieAdded.connect(lambda _, browser=browser:
       #                              Cookie().handle(browser))
            

    def goToUrl(self):
        url = QUrl(self.urlBar.text())
 
        if url.scheme() == '':
            url.setScheme('https')
 
        self.tabs.currentWidget().setUrl(url)
        
    
    def tab_open_doubleclick(self, currentTabIndex):
        if currentTabIndex == -1:
            self.addNewTab()
            
            
    def linkOpen(self, url):
        if is_pressed('ctrl+space'):
            self.addNewTab(QUrl(url))
        print(url)
  
            
    def current_tab_changed(self, currentTabIndex):
        url = self.tabs.currentWidget().url()

        self.update_urlBar(url, self.tabs.currentWidget())
        
        
    def update_window_title(self, browser: QWidget):
        if browser != self.tabs.currentWidget():
            return

        title = 'ACS Browser' if browser.page().title() == '' else browser.page().title()

        self.setWindowTitle(f'{title}')
        
    def update_urlBar(self, url: QLineEdit, browser: QWidget):
        if browser != self.tabs.currentWidget():
            return
 
        self.urlBar.setText(url.toString())
        self.urlBar.setCursorPosition(0)
        
    def updateIcon(self, browser: QWidget):
        if browser != self.tabs.currentWidget():
            return
        
        self.tabs.setTabIcon(self.tabs.currentIndex(), browser.page().icon())
        
        
    def close_current_tab(self):
        if self.tabs.count() < 2:
            self.close()

        self.tabs.removeTab(self.tabs.currentIndex())