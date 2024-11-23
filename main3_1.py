import json
from pymongo import MongoClient
import pymongo
print(pymongo.__version__)

client = MongoClient('mongodb://localhost:27017/')

data = []
with open('./books_data.json', 'r') as f:
    data = json.load(f)

print(len(data))

db = client['books_data']
collection = db['title']

data = [
        {
            'title': 'Книга 1',
            'price': 10.99,
            'in_stock': 'В наличии',
            'available_quantity': '5',
            'description': 'Описание книги 1'
        },
        {
            'title': 'Книга 2',
            'price': 12.49,
            'in_stock': 'В наличии',
            'available_quantity': '3',
            'description': 'Описание книги 2'
        },

    ]
#collection.insert_many(data)  # Для вставки нескольких документов


all_books = collection.find()
for book in all_books:
    print(book)


new_book = {'title': 'Новая книга', 'price': 12.99}
#collection.insert_one(new_book)


collection.update_one({'title': 'Книга 1'}, {'$set': {'price': 11.99}})


collection.delete_one({'title': 'Книга 1'})