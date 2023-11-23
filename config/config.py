import json
from typing import Any
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QUrl, QMetaObject
from PyQt5.QtGui import QIcon

import sqlite3

from matplotlib.font_manager import json_load

class ConfigPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUIConfig()
        self.conn = sqlite3.connect('browser.db')
        self.curs = self.conn.cursor()
        
        self.load = ''
        
        
    def initUIConfig(self):
       self.closeBtn = QPushButton(self)
       self.closeBtn.setIcon(QIcon('./assets/icons/sidebar/closeHistory.png'))
       self.closeBtn.clicked.connect(self.closeConfig)
       self.closeBtn.setGeometry(5, 10, 390, 30)

        
       #URL do Botao Inicial
       self.homeLabel = QLabel(self)
       self.homeLabel.setText('URL do Botao Inicial')
       self.homeLabel.setGeometry(20, 80, 130, 30)
       
       self.homeEdit = QLineEdit(self)
       self.homeEdit.setText(f'{self.loadJson()['homeURL']}')
       self.homeEdit.setGeometry(180, 80, 200, 30)
       
       
       #URL da Pagina Inicial
       self.newPageLabel = QLabel(self)
       self.newPageLabel.setText('URL da Pagina Inicial')
       self.newPageLabel.setGeometry(20, 150, 130, 30)
       
       self.newPageEdit = QLineEdit(self)
       self.newPageEdit.setText(f'{self.loadJson()['homeURL']}')
       self.newPageEdit.setGeometry(180, 150, 200, 30)
       
       
       #Engine de Busca
       self.searchEngineLabel = QLabel(self)
       self.searchEngineLabel.setText('Engine de Busca')
       self.searchEngineLabel.setGeometry(20, 220, 200, 30)
       
       self.searchEngineCombo = QComboBox(self)
       self.searchEngineCombo.addItem('Google')
       self.searchEngineCombo.addItem('Yahoo')
       self.searchEngineCombo.addItem('Bing')
       self.searchEngineCombo.setGeometry(180, 220, 200, 30)
       
       if self.loadJson()['searchEngine'] == "Google":
            self.searchEngineCombo.setCurrentIndex(0)
            
       elif self.loadJson()['searchEngine'] == "Yahoo":
            self.searchEngineCombo.setCurrentIndex(1)
            
       elif self.loadJson()['searchEngine'] == "Bing":
            self.searchEngineCombo.setCurrentIndex(2)
    
       
       
       #Salvar Dados
       self.saveBtn = QPushButton(self)
       self.saveBtn.setText('Salvar Dados')
       self.saveBtn.clicked.connect(self.saveAllData)
       self.saveBtn.setGeometry(5, 380, 390, 30)

           
       with open('assets/css/config.css') as file:
           self.setStyleSheet(file.read())
           
       QMetaObject.connectSlotsByName(self)
       
       self.setGeometry(70, 540, 400, 420)
       self.setWindowFlags(Qt.WindowType.Popup)
       
            
        
    def saveAllData(self) -> None:
        homeText = str(self.homeEdit.text())
        newPageText = str(self.newPageEdit.text())
        engineText = str(self.searchEngineCombo.currentText())
        
        self.writeJson('homeURL', homeText)
        self.writeJson('newTabURL', newPageText)
        self.writeJson('searchEngine', engineText)
        
        
    def writeJson(self, textInJSON: str, textForChange: str) -> None:
        with open('config.json', 'r') as fileJSON:
            data = json.load(fileJSON)
            
        with open('config.json', 'w', encoding='utf-8') as fileJSON:
            data[f"{textInJSON}"] = textForChange
            json.dump(data, fileJSON, indent=4)
            
    def loadJson(self):
        with open('config.json', 'r') as file:
            return json.load(file)

    def closeConfig(self):
        self.close()