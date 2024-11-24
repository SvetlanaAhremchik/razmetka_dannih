import requests
from lxml import html
import pandas as pd


url = 'https://www.worldometers.info/world-population/population-by-country/'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
try:
    # запрос на указанный URL
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Проверка на наличие ошибок при запросе


    tree = html.fromstring(response.text)

    # Использую XPath для извлечения данных о странах и их населении
    countries = tree.xpath("//table[@id='example2']/tbody/tr/td[2]/a/text()")  # Названия стран
    populations = tree.xpath("//table[@id='example2']/tbody/tr/td[3]/text()")  # Население стран
    land_areas = tree.xpath('//table[@id="example2"]/tbody/tr/td[7]/text()')

    # Создаю DataFrame для  сохранения в CSV
    data = pd.DataFrame({
        'Country': [country.strip() for country in countries],
        'Population': [population.strip() for population in populations],
        'Land Area': [land_area.strip() for land_area in land_areas]
    })

    data.to_csv('countries_population.csv', index=False, encoding='utf-8', sep=';')

    print("Данные успешно извлечены и сохранены в countries_population.csv.")

except requests.RequestException as e:
    # Обработка ошибок запросов HTTP
    print(f"Ошибка при выполнении запроса: {e}")

except Exception as e:
    # Общая обработка ошибок
    print(f"Произошла ошибка: {e}")
