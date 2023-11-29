from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

import navbar, sys, psutil

app = QApplication(sys.argv)
app.setApplicationName("Simple Browser")
app.setWindowIcon(QIcon('assets/logo/browser.png'))

window = navbar.NavBar()

with open("assets/css/style.css", "r") as style:
        app.setStyleSheet(style.read())

app.exec_() 