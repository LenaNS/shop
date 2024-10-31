# Cервис для хранения товаров. 
## Используемый стек
```
Python 3.12
Django 5.1.1
Django Rest Framework 3.15
SQLite 3
```

## Функции
```
Управление товароми:
- создание товара
- получение товара или списка товаров
- обновление товара
- удаление товара
- уменьшение количества товара

Управление ценами на товары:
- создание цены
- получение цены или списка цен
- обновление цены
- удаление цены

Управление категориями товаров:
- создание категории
- получение категории или списка категорий
- обновление категории
- удаление категории

Административная панель:
- все модели доступны в административной панели Django;
- можно осуществлять поиск продукта по его имени или категории;
- административная панель доступна по адресу /admin/.
```
## Установка
### 1. Клонирование репозитория
```
Клонируйте проект при помощи Git
```
##### Пример
```bash
git clone https://github.com/LenaNS/shop.git
```
### 2. Установка зависимостей
```
Зависимости находятся в файле requirements.txt, воспользуйтесь pip для установки (по желанию настройте виртуальное окружение)
```
##### Пример
```bash
pip install -r requirements.txt
```

### 3. Миграция БД (необязательно)
```
Приложение поставляется с тестовыми данными в файле db.sqlite3
Если Вы хотите использовать чистую БД - удалите файл db.sqlite3 и выполните миграции при помощи 'migrate'
```
##### Пример:
```bash
py manage.py migrate
```
## Запуск
```
Для запуска приложения выполните команду 'runserver', при необходимости укажите нужный порт
```
##### Пример:
```bash
py manage.py runserver localhost:8000
```
## API
#### Получить список записей о товарах
```
GET /api/products/
```
##### Пример:
```bash
curl -X GET http://127.0.0.1:8000/api/products/
```
#### Создать новую запись о товаре
```
POST /api/products/
{
    "name": str,
    "quantity": int,
    "barcode": str,
    "price": int,
    "category": int
}
```
##### Пример:
```bash
curl --json '{"name":"Приключение", "quantity":30,"barcode":2020,"price":2, "category":3}' localhost:8000/api/products/
```
#### Получить запись о товаре
```
GET /api/products/{id}/
```
##### Пример:
```bash
curl -X GET http://127.0.0.1:8000/api/products/1/
```
#### Обновить запись об автомобиле
```
PUT/PATCH /api/products/{id}/
{
    "name": str,
    "quantity": int,
    "barcode": str,
    "price": int,
    "category": int
}
```
##### Пример:
```bash
curl --json '{"id":1,"name":"Приключение", "quantity":30,"barcode":2020,"price":2, "category":3}' localhost:8000/api/products/
```
#### Удалить запись об автомобиле
```
DELETE /api/products/{id}/
```
##### Пример:
```bash
curl -X DELETE http://127.0.0.1:8000/api/products/1/
```

##### Примечание:

Все перечисленные выше методы так же доступны для цен и категорий.

#### Уменьшить количество товаров 
```
POST /api/products/{id}/reduce_quantity/
{
    "amount": int
}
```
##### Пример:
```bash
curl --json '{"amount": 4}' localhost:8000/api/products/1/reduce_quantity/
```
# Тестирование приложения

Для запуска тестов, используйте следующую команду:

```bash
python manage.py test
```