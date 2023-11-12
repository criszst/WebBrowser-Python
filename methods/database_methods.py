from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget

import sqlite3, datetime

class DBMethods():
    def __init__(self):
        self.conn = sqlite3.connect('browser.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
    
    def converUrlToStr(self, url: QUrl) -> str:
        urlConverted = str(url)
        urlConverted = urlConverted[19 : len(urlConverted) - 2]
        
        return urlConverted
    
    def convertDateToBR(self, date: datetime.date) -> str:
        formattedPtBr = date.strftime('%d/%m/%Y %H:%M:%S')
        
        return formattedPtBr
    
    def replaceOldData(self, db: str, dataName: str, dataType, numberDataInTable: int) -> None:
        viewLog = self.cursor.execute(f'SELECT * FROM {db}').fetchall()
        
        for i in range(len(viewLog)):
            if dataType == viewLog[i][numberDataInTable]:
                self.cursor.execute(f'DELETE FROM {db} WHERE {dataName} = ?', [dataType])
                
        self.conn.commit()
        self.conn.close()
        
    def getCurrentZoomPage(self, currentTab: QWidget):
        urlStr = DBMethods().converUrlToStr(currentTab.page().url())
        getInfoFromUrl = self.cursor.execute('SELECT * FROM zoom WHERE url = ?', [urlStr]).fetchall()
        
        zoom = 1.0
    
        for i in range(len(getInfoFromUrl)):
            zoom = getInfoFromUrl[i][2]

        return zoom