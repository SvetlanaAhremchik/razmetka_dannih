from clickhouse_driver import Client

try:

    client = Client(host='127.0.0.1', port=9000)
    print("Подключение успешно.")


    try:
        client.execute('CREATE DATABASE IF NOT EXISTS my_database')
        print("База данных создана или уже существует.")
    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")


    try:
        client.execute('''
            CREATE TABLE IF NOT EXISTS my_database.books (
                title String,
                price Float64,
                in_stock String,
                available_quantity Int32,
                description String
            ) ENGINE = MergeTree() ORDER BY title
        ''')
        print("Таблица создана или уже существует.")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")


    data = [
        ('Book Title 1', 19.99, 'Yes', 10, 'Description 1'),
        ('Book Title 2', 25.00, 'No', 0, 'Description 2')
    ]

    try:
        client.execute('INSERT INTO my_database.books (title, price, in_stock, available_quantity, description) VALUES',
                       data)
        print("Данные успешно вставлены.")
    except Exception as e:
        print(f"Ошибка при вставке данных: {e}")

except Exception as e:
    print(f"Ошибка подключения: {e}")
