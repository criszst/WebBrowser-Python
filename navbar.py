import re
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QWidget, QShortcut, QToolBar, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

from methods.database_methods import DBMethods
from methods.tabs_methods import TabsMethods
from methods.sidebar_methods import SideBarMethods
#from handleNetwork.setCookie import Cookie

import sys, sqlite3, datetime

class NavBar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_tabs()

        
    def init_tabs(self):
        self.conn = sqlite3.connect("browser.db", check_same_thread=False)
        self.crsor = self.conn.cursor()
        
        self.tabs = TabsMethods.create_tabs(self) 
        self.setCentralWidget(self.tabs)

        self.nav_toolbar = TabsMethods.create_navigation_toolbar(self)
        self.addToolBar(self.nav_toolbar)

        
        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.goToUrl)
        self.nav_toolbar.addWidget(self.urlBar)
        
        self.label = QLabel()
        self.nav_toolbar.addWidget(self.label)

        self.addNewTab()
        
        self.addShortcut = QShortcut('Ctrl+T', self)
        self.addShortcut.activated.connect(self.addNewTab)
        
        self.closeShortcut = QShortcut('Ctrl+W', self)
        self.closeShortcut.activated.connect(self.close_current_tab)
        
        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint) -> retira os botoes de fechar, minimizar e maximizar
        
        self.showMaximized()
        self.setWindowTitle('ACS Browser')
        
        
    
    def addNewTab(self, url = None, label="Blank"):
        if url is None or url == ' ':
            url = QUrl('https://www.google.com')

        browser = QWebEngineView()
        browser.load(url)

        currentTabIndex = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(currentTabIndex)
        
              
        browser.urlChanged.connect(lambda url, browser=browser:
                                     self.update_urlBar(url, browser))

        browser.titleChanged.connect(lambda _, i=currentTabIndex, browser=browser:
                                     self.tabs.setTabText(i, self.tabs.currentWidget().page().title()))
        
        browser.iconChanged.connect(lambda _, browser=browser:
                                     self.updateIcon(browser))
        
        browser.loadFinished.connect(lambda _, browser=browser:
                                     self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, SideBarMethods().create_sidebar(self)))
        
        browser.page().loadFinished.connect(self.loadDBMethods)
        
        
       # browser.page().profile().cookieStore().deleteAllCookies()
       
                
    def goToUrl(self):
        url = QUrl(self.urlBar.text())
        
        valid_url = re.compile(
        r'^(?:http|ftp)s?://'  # http:// o https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # Dominio...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...o dirección IP
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...o [dirección IPv6]
        r'(?::\d+)?'  # self.urlBar.text()Opción de puerto
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        print(re.match(valid_url, 'netflix.com'))
        
        if not re.match(valid_url, self.urlBar.text()):
            url = f'https://www.google.com/search?q={self.urlBar.text()}'
            
        elif re.match(valid_url, self.urlBar.text()) or url.scheme() == '':
            url.setScheme('https')
            
        self.tabs.currentWidget().load(QUrl.fromUserInput(url))
 
        
    
    def tab_open_doubleclick(self, currentTabIndex):
        if currentTabIndex == -1:
            self.addNewTab()
  
            
    def current_tab_changed(self):
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
            sys.exit()

        self.tabs.removeTab(self.tabs.currentIndex())
        
        
    def loadDBMethods(self):
        title = self.tabs.currentWidget().page().title()
        url = DBMethods().convertUrlToStr(self.tabs.currentWidget().page().url())
        date = DBMethods().convertDateToBR(datetime.datetime.now())
    
        DBMethods().replaceOldData('history', 'url', url, 2)


        self.crsor.execute(
            "INSERT INTO history (title,url,date) VALUES (:title,:url,:date)",
            {"title": title, "url": url, "date": date}
                      )
        
        self.conn.commit()
        
        zoomInDB = DBMethods().getCurrentZoomPage(self.tabs.currentWidget().page().url())
        self.tabs.currentWidget().setZoomFactor(float(zoomInDB))