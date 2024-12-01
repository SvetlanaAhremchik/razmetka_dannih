import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json



chromedriver_autoinstaller.install()
service = Service()
driver = webdriver.Chrome(service=service)

data = []

try:

    driver.get('https://blanki.by/catalog/zhurnaly/okhrana-truda/')


    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.thumb.shine')))


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    products = soup.select('a.thumb.shine')


    if not products:
        print("Не удалось найти товары на странице.")
    else:
        for product in products:
            title = product.find('img')['alt'] if product.find('img') and 'alt' in product.find('img').attrs else "Неизвестно"
            link = 'https://blanki.by' + product.get('href', "Неизвестно")
            img_src = product.find('img').get('src', "Нет изображения")


            data.append({
                'название': title,
                'ссылка': link,
                'изображение': img_src
            })

except Exception as e:
    print(f"Ошибка: {e}")
finally:
    driver.quit()


if data:
    with open('blanki_products.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print("Данные успешно сохранены.")
else:
    print("Нет данных для сохранения.")


#
# Сайт: https://blanki.by/catalog/zhurnaly/okhrana-truda/
# Описание
#
# Я выбрала сайт "Blanki" для извлечения информации о товарах
# из раздела "Журналы" и "Охрана труда". Целью проекта было
# получить названия товаров, ссылки на них и изображения.
# Для извлечения данных с сайта был выбран следующий подход:
# Использовались библиотеки Selenium и BeautifulSoup. Selenium
# помогает управлять браузером и автоматизировать процессы навигации,
# а BeautifulSoup позволяет удобно парсить HTML и извлекать нужные элементы.
#
# Сначала был автоматически установлен
# необходимый драйвер браузера (Chromedriver) и открыта
# веб-страница с товарами, используя Selenium.
#
# С помощью явного ожидания удостоверились,
# что все элементы, соответствующие товарам, загружены, прежде чем
# продолжить парсить содержимое страницы.
#
# Был использован CSS-селектор для нахождения всех
# элементов с классом thumb shine, содержащих информацию о товарах.
# Далее, для каждого товара извлекались название (атрибут alt изображения),
# ссылка на страницу товара и путь к изображению.
# Полученные данные сохранялись в формате JSON
# для дальнейшего использования и анализа.
#
# Трудности
# В ходе реализации проекта я столкнулась с несколькими проблемами:
# Изменение структуры сайта: После первой попытки извлечения данных
# код не работал, так как структура HTML на сайте изменилась. Я проверила
# HTML-код и обновила селекторы.
# Некоторые страницы могли загружаться медленно или заблокировать
# автоматизированные запросы. Я увеличила время ожидания загрузки
# элементов
# Копирование неправильных атрибутов: Изначально я использовала атрибут
# title для получения названия, который не всегда был доступен.
# Это было исправлено, и  использовала атрибут alt у изображений,
# что оказалась более надежным методом.
# Результаты
# В результате выполнения проекта удалось успешно извлечь следующую информацию:
# Названия товаров (в большинстве случаев извлеченные из атрибутов изображения).
# Ссылки на страницы товаров. Пути к изображениям товаров.
# Эти данные были успешно сохранены в JSON-файл, что делает
# их готовыми для использования в дальнейшем анализе или интеграции
# в другие приложения. Проект продемонстрировал эффективность использования
# Selenium и BeautifulSoup для автоматизированного извлечения данных
# из веб-страниц и показал, как можно справляться с возникающими трудностями
# в процессе парсинга.