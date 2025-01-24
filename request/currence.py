import requests
import json
from icecream import ic

class CBRF():
    def __init__(self):
        self.url = "https://www.cbr-xml-daily.ru/daily_json.js"


    async def value_yen(self,):
        responce =  requests.get(self.url)
        
        data =  json.loads(responce.text)
        ic(data)
        return data["Valute"]["JPY"]["Value"]
    async def value_von(self,):
        responce =  requests.get(self.url)
        
        data =  json.loads(responce.text)
        ic(data)
        return data["Valute"]["KRW"]["Value"]
    async def value_uan(self,):
        responce =  requests.get(self.url)
        
        data =  json.loads(responce.text)
        ic(data)
        return data["Valute"]["CNY"]["Value"]