import json

class Handle:
    def getShop():
        return json.loads(open("JSON/Shop.json", 'r').read())