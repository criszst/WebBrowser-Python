from http.cookies import SimpleCookie
from PyQt5.QtNetwork import QNetworkCookie

class Cookie:
    def __init__(self) -> None:
        pass
    
    def handle(self, cookie: QNetworkCookie):
        cookie['name'] = 'value'
        cookie['name']['samesite'] = 'Lax'
        cookie['name']['secure'] = True  


        contents = cookie.output().encode('ascii')


        qt_cookie = QNetworkCookie.parseCookies(contents)[0]

        
        print(qt_cookie)

        return qt_cookie
        

    
    