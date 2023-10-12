from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QLineEdit, QWidget, QShortcut
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Tabs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self): 
        from tabsMethods import tabs_methods
        self.tabs = tabs_methods.TabsMethods.create_tabs(self)
        
        self.setCentralWidget(self.tabs)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        nav_toolbar = tabs_methods.TabsMethods.create_navigation_toolbar(self)
        self.addToolBar(nav_toolbar)
        

        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.goToUrl)
        nav_toolbar.addWidget(self.urlBar)

        self.addNewTab()
        
        self.addShortcut = QShortcut('Ctrl+T', self)
        self.addShortcut.activated.connect(self.addNewTab)
        
        self.closeShortcut = QShortcut("Ctrl+W", self)
        self.closeShortcut.activated.connect(self.close_current_tab)


        self.showMaximized()
        self.setWindowTitle('ACS Browser')
    

    def addNewTab(self, url = None, label="Blank"): 
        if url is None:
            url = QUrl('https://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(url)
        
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
              
        browser.urlChanged.connect(lambda url, browser=browser:
                                     self.update_urlBar(url, browser))

        browser.titleChanged.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, self.tabs.currentWidget().page().title()))
        
        browser.iconChanged.connect(lambda _, browser=browser:
                                     self.tabs.setTabIcon(self.tabs.currentIndex(), browser.page().icon()))
        
        
    def tab_open_doubleclick(self, i):
        if i == -1:
            self.addNewTab()
            
  
            
    def current_tab_changed(self, i):
        url = self.tabs.currentWidget().url()

        self.update_urlBar(url, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())
        

    def close_current_tab(self):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(self.tabs.currentIndex())
        

    def update_title(self, browser: QWidget):
        if browser != self.tabs.currentWidget():
            return

        title = 'ACS Browser' if browser.page().title() == '' else browser.page().title()

        self.setWindowTitle(f'{title}')
        

    def update_urlBar(self, url, browser: QWidget):
        if browser != self.tabs.currentWidget():
            return
 
        self.urlBar.setText(url.toString())
        self.urlBar.setCursorPosition(0)
        
        
    def goToUrl(self):
        url = QUrl(self.urlBar.text())
 
        if url.scheme() == '':
            url.setScheme('https')
 
        self.tabs.currentWidget().setUrl(url)