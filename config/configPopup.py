from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QUrl, QRect, QMetaObject

class ConfigPage(QWidget):
    def __init__(self):
        super().__init__()
        #self.mainWidget = QWidget(self)
        self.initUIConfig()
        
    def initUIConfig(self):
       #layout = QGridLayout()

       self.closeBtn = QPushButton(self)
       self.closeBtn.setIcon(QIcon('./assets/icons/sidebar/closeHistory.png'))
       self.closeBtn.clicked.connect(self.closeConfig)
       self.closeBtn.setGeometry(5, 5, 380, 30)
        
       #layout.addWidget(self.closeBtn)
        
       self.homeBtn = QLabel(self)
       self.homeBtn.setText('URL do Botao Inicial')
       self.homeBtn.setGeometry(100, 200, 20, 10)
    

       #layout.addWidget(self.homeBtn)
       
       QMetaObject.connectSlotsByName(self)
       
       #self.setLayout(layout)
       self.setGeometry(70, 540, 400, 420)
                        #X   #Y  #Width #Height
        
       self.setWindowFlags(Qt.WindowType.Popup)
       
    def closeConfig(self):
        self.close()