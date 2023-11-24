from ast import Str
import re

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QWidget, QShortcut, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

from methods.database_methods import DBMethods
from methods.tabs_methods import TabsMethods
from methods.sidebar_methods import SideBarMethods
from methods.json_methods import ConfigMethods
#from handleNetwork.setCookie import Cookie

import sys, sqlite3, datetime, json

class NavBar(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_tabs()

    def init_tabs(self):
        self.conn = sqlite3.connect("browser.db", check_same_thread=False)
        self.crsor = self.conn.cursor()
        
        self.tabs = TabsMethods().create_tabs(self) 
        self.setCentralWidget(self.tabs)
        
        self.nav_toolbar = TabsMethods().create_navigation_toolbar(self)
        self.addToolBar(self.nav_toolbar)

        
        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.goToUrl)
        self.nav_toolbar.addWidget(self.urlBar)
        
        
        self.label = QLabel()
        self.nav_toolbar.addWidget(self.label)
    

        self.addShortcut = QShortcut('Ctrl+T', self)
        self.addShortcut.activated.connect(self.addNewTab)
        
        self.closeShortcut = QShortcut('Ctrl+W', self)
        self.closeShortcut.activated.connect(self.close_current_tab)
        
        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint) -> retira os botoes de fechar, minimizar e maximizar
        
        self.addNewTab()
        
        self.showMaximized()
        self.setWindowTitle('ACS Browser')
        
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, SideBarMethods().create_sidebar(self))
        
    
    def addNewTab(self, url = None, label="Blank"):
        if url is None or url == ' ':
            url = QUrl(ConfigMethods().loadJson()['newTabURL'])

        browser = QWebEngineView()
        browser.page().WebAction()

              
        currentTabIndex = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(currentTabIndex)
        
        browser.load(url)
        
        browser.urlChanged.connect(lambda url, browser=browser:
                                     self.update_urlBar(url, browser))
        

        browser.titleChanged.connect(lambda _, i=currentTabIndex, browser=browser:
                                     self.tabs.setTabText(i, self.tabs.currentWidget().page().title()))
        
        
        browser.iconChanged.connect(lambda _, browser=browser:
                                     self.updateIcon(browser))
        
        browser.page().loadFinished.connect(self.loadDBMethods)
        
       # browser.page().profile().cookieStore().deleteAllCookies()
       
    
                
    def goToUrl(self):
        url = QUrl(self.urlBar.text())
        urlBarTxt = self.urlBar.text()
        
        self.searchEngineDefault = ''
        load = ConfigMethods().loadJson()['searchEngine']
        
        if load == 'Google':
            self.searchEngineDefault = 'https://www.google.com/search?q='
            
        elif load == 'Yahoo':
            self.searchEngineDefault = 'https://search.yahoo.com/search?q='
            
        elif load == 'Bing':
            self.searchEngineDefault = 'https://www.bing.com/search?q='
            
        elif load == 'DuckDuckGo':
            self.searchEngineDefault = 'https://duckduckgo.com/?q='
            
        
        valid_url = re.compile(
    r"^(http|https)?:?(\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
        )
        
        if valid_url.search(urlBarTxt) and not any(
            i in urlBarTxt for i in ("http://", "https://", "file:///")
        ):
            url = f'https://{urlBarTxt}'
            
            
        elif '/' not in urlBarTxt:
            url = f'{self.searchEngineDefault}{self.urlBar.text()}'
            
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
            return 0
 
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
        self.label.setText(f"Zoom atual: {self.tabs.currentWidget().zoomFactor():.1f}")