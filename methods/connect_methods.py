from PyQt5.QtWidgets import QLineEdit, QWidget

class BrowserConnect:
    def __init__(self) -> None:
        pass        
        
    def update_urlBar(self, main, url: QLineEdit, browser: QWidget):
        if browser != main.tabs.currentWidget():
            return 0
 
        main.urlBar.setText(url.toString())
        main.urlBar.setCursorPosition(0)
       
        
    def updateIcon(self, main, browser: QWidget):
        if browser != main.tabs.currentWidget():
            return
        
        main.tabs.setTabIcon(main.tabs.currentIndex(), browser.page().icon())
        
        

    