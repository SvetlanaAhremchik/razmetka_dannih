import requests
import json
from secret import api_token

final_point = "https://api.foursquare.com/v3/places/search"

city = input("Введите название города: ")
lookfor = input("Введите категорию объекта (cafe, fitness, museum): ")
fields = "categories,name,rating,location"

params = {
    "near": city,
    "query": lookfor,
    "limit": 10,
}

headers = {
    "Accept": "application/json",
    "Authorization": api_token
}

response = requests.get(final_point, params=params, headers=headers)

if response.status_code == 200:
    print("Успешный запрос API!")
    data = json.loads(response.text)
    venues = data.get("results", [])

    if not venues:
        print("Заведения не найдены.")
    else:
        for venue in venues:
            print("Название:", venue["name"])
            address = venue["location"].get("address", "Нет адреса")
            print("Адрес:", address)
            rating = venue.get("rating", "Нет рейтинга")
            print("Рейтинг:", rating)
            print("\n")
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)