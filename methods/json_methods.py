import json

class ConfigMethods():
    def __init__(self) -> None:
        pass

    def writeJson(self, textInJSON: str, textForChange: str) -> None:
        with open('config.json', 'r') as fileJSON:
            data = json.load(fileJSON)
            
        with open('config.json', 'w', encoding='utf-8') as fileJSON:
            data[f"{textInJSON}"] = textForChange
            json.dump(data, fileJSON, indent=4)
            
    def loadJson(self):
        with open('config.json', 'r') as file:
            return json.load(file)