from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkCookie, QNetworkCookieJar
from PyQt5.QtWebEngineWidgets import QWebEngineProfile
from http.cookies import SimpleCookie

class Cookie:
    def __init__(self) -> None:
        pass
    
    def handle(self, browser):
        network_manager = QNetworkAccessManager()
            
        cookie = QNetworkCookie()
        cookie.setName(b'cookie_config') 
        cookie.setValue(QByteArray(b'cookie_config')) 
        cookie.setDomain(browser.page().url().host())
        cookie.setPath('/') 
        cookie.setSecure(True)


        cookie_jar = QNetworkCookieJar()
        network_manager.setCookieJar(cookie_jar)
        cookie_jar.insertCookie(cookie)

        return cookie
        

    
    