from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from tabs import Tabs

import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    with open("assets/css/style.css", "r") as style:
        app.setStyleSheet(style.read())
        
    app.setApplicationName('ACS Browser')
    app.setWindowIcon(QIcon('assets/logo/browserLogo.png'))
   
    window = Tabs()
    sys.exit(app.exec_())