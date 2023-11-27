# Browser
![browse-screenshot](https://github.com/Cristi4nSt/WebBrowser-Python/blob/main/assets/browser/browserImage.png?raw=true)
Inspirado no Opera One

# Funções
Atualmente possui funções básicas de todo navegador (recarregar a página, voltar uma página, visualizar histórico, etc.)

O zoom é salvo na DataBase, então caso você feche o navegador e abra depois, o zoom anteriormente definido ainda continuará

É possivel configurar qual motor de busca deseja usar (google, yahoo, bing ou o DuckDuckGo)
<br>
Também dá pra configurar a url do botão inicial e a url que abrirá quando você abrir o browser ou uma nova aba

# Instalação
Clone o repositorio com o comando Git
```
git clone https://github.com/Cristi4nSt/WebBrowser-Python
```

Entre no diretório
```
cd WebBrowser-Python
```

Depois, instale as dependencias que estão no arquivo "requirements.txt"
```
python -m pip install -r requirements.txt
```

Por último, execute o browser
```
python main.py
```

# Dependências
- Python 3.12.0 ou superior
- PyQt5 5.15.9
