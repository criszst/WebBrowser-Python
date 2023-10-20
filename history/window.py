from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QDialog
from random import randint


class windowHistory(QDialog):
    def __init__(self):
        super().__init__()
        self.lay = QVBoxLayout()
        self.init_ui()

        
    def init_ui(self):
        self.label = QLabel('window')
        self.lay.addWidget(self.label)
        self.setLayout(self.lay)