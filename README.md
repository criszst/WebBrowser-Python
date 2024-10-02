![browse-screenshot](https://github.com/Cristi4nSt/WebBrowser-Python/blob/main/assets/browser/browserImage.png?raw=true)

# Funções
It currently has basic functions of any browser (reloading the page, going back a page, viewing history, etc.)

The zoom is saved in the Database, so if you close the browser and open it later, the previously defined zoom will still be present

You can configure which search engine you want to use (google, yahoo, bing or DuckDuckGo)
<br>
You can also configure the URL of the home button and the URL that will open when you open the browser or a new tab

# Installation
Clone the repository with the Git commandt
```
git clone https://github.com/Cristi4nSt/WebBrowser-Python
```

Open the directory
```
cd WebBrowser-Python
```

Then, install the dependencies that are in the "requirements.txt" file.
```
python -m pip install -r requirements.txt
```

Finally, run the browser
```
python main.py
```

# Dependencies
- Python 3.12.0 or higher
- PyQt5 5.15.9
