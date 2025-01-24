import requests
from icecream import ic

class CalCulAPI():
    def __init__(self,):
        self.api_key = "r13W5ziW8N"
        self.client = "35483"
        self.headers = {
        "Content-Type": "application/json",
        "Api-Key": "r13W5ziW8N",
        "Api-Client-Id": "35483"
                        }
        
    async def search_price(self, info: dict,):
        data = {
        "owner": 1, # 1 - Физическое лицо (для личного использования), 2 - Юридическое лицо, 3 - Физическое лицо (для перепродажи)
        "age": info["age"], # "0-3", "3-5", "5-7", "7-0"
        "engine": info["engine"], # 1 - Бензиновый, 2 - Дизельный, 3 - Гибридный, 4 - Электрический
        "power": info["power"], # Мощность двигателя
        "power_unit": info["power_unit"], # 1 - ЛС, 2 - кВт (по умолчанию 1)
        "value": info["value"], # Объём двигателя в кубических сантиметрах
        "price": info["price"], # Стоимость автомобиля
        "curr": info["country"] # Валюта стоимости автомобиля (RUB, USD, EUR, CNY, JPY, KRW - по умолчанию RUB)
    }
        ic(f"{data}")
        try:
            ic("Отправка запроса к API")
            response = requests.post("https://calcus.ru/api/v1/Customs", headers=self.headers, json=data)
            ic("Расчет стоимости выполнен")
            result = response.json()
            ic(result)
            return result


        except Exception as e:
            ic(f"Ошибка {e}")