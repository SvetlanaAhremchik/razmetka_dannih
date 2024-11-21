import requests
from bs4 import BeautifulSoup
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}


def get_description(book_url):
    response = requests.get(book_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    desc_div = soup.find('meta', attrs={'name': 'description'})
    if desc_div:
        return desc_div['content'].strip()
    return "Нет описания"


def get_book_info(book):
    title = book.find('h3').find('a')['title']
    price = book.find('p', class_='price_color').text[1:].replace('£', '').strip()

    in_stock_text = book.find('p', class_='instock availability').text.strip()

    if 'In stock' in in_stock_text:
        in_stock = "В наличии"
    else:
        in_stock = "Недоступно"

    relative_url = book.find('h3').find('a')['href']
    book_url = f"http://books.toscrape.com/catalogue{relative_url}"

    description = get_description(book_url)

    return {
        'title': title,
        'price': float(price),
        'in_stock': in_stock,
        'description': description,
    }


def scrape_books():
    base_url = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
    all_books = []

    while True:
        response = requests.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        books = soup.find_all('article', class_='product_pod')
        for book in books:
            book_info = get_book_info(book)
            all_books.append(book_info)

        next_button = soup.find('li', class_='next')
        if next_button is None:
            break
        next_page = next_button.find('a')['href']
        base_url = f'http://books.toscrape.com/catalogue/category/books_1/{next_page}'

    return all_books


books_data = scrape_books()

with open('books_data.json', 'w', encoding='utf-8') as f:
    json.dump(books_data, f, ensure_ascii=False, indent=4)

print("Данные о книгах успешно сохранены в books_data.json!")