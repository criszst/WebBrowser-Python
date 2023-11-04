from PyQt5.QtCore import QUrl

import sqlite3
import datetime

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
    
    def replaceOldData(self, db: str, dataName: str, dataType, numberDataInTable: int):
        viewLog = self.cursor.execute(f'SELECT * FROM {db}').fetchall()
        
        for i in range(len(viewLog)):
            if dataType == viewLog[i][numberDataInTable]:
                self.cursor.execute(f'DELETE FROM {db} WHERE {dataName} = ?', [dataType])
                
        self.conn.commit()