from PyQt5.QtWidgets import QGridLayout, QWidget, QPushButton, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl

class ConfigPage(QWidget):
    def __init__(self):
       super().__init__()
       layout = QGridLayout()
       
       self.closeBtn = QPushButton()
       self.closeBtn.setIcon(QIcon('./assets/icons/sidebar/closeHistory.png'))
       self.closeBtn.clicked.connect(self.closeConfig)
            
       layout.addWidget(self.closeBtn)
        
       self.setLayout(layout)    
       self.setGeometry(200, 400, 400, 420)
                         #X  #Y  #Width #Height
        
       self.setWindowFlags(Qt.WindowType.Popup)
       
    def closeConfig(self):
        self.close()