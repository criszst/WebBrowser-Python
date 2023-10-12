from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QLineEdit
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

        self.addNewTab(QUrl('https://www.google.com'))

        self.showMaximized()
        self.show()
        self.setWindowTitle('ACS Browser')
        
        
    
    def addNewTab(self, url=None, label="Blank"):
            
        if url is None:
            url = QUrl('https://www.google.com')

        browser = QWebEngineView()
        browser.setUrl(url)
        
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
              
        browser.urlChanged.connect(lambda url, browser=browser:
                                   self.update_urlBar(url, browser))

        browser.titleChanged.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title().split(' ')[0]))
        
        browser.iconChanged.connect(lambda _, browser=browser:
                                     self.tabs.setTabIcon(self.tabs.currentIndex(), browser.page().icon()))
        
        
    def tab_open_doubleclick(self, i):
        if i == -1:
            self.addNewTab()
            
            
    def current_tab_changed(self, i):
        url = self.tabs.currentWidget().url()

        self.update_urlBar(url, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())
        

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)
        

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = browser.page().title()

        self.setWindowTitle(f'ACS - {title}')
        

    def update_urlBar(self, url, browser = None):
        if browser != self.tabs.currentWidget():
            return
 
        self.urlBar.setText(url.toString())
        self.urlBar.setCursorPosition(0)
        
        
    def goToUrl(self):
        url = QUrl(self.urlBar.text())
 
        if url.scheme() == "":

            url.setScheme("https")
 
        self.tabs.currentWidget().setUrl(url)