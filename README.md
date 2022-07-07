# Сервер хранения параметров пользователя


### Описание
API для создания и просмотра параметров по имени юзера, имени параметра, типу

### Технологии
Python 3.7.9
Flask==2.1.2
Flask-RESTful==0.3.9
Flask-SQLAlchemy==2.5.1

### Для запуска в dev-режиме (Windows) в папке с работой:

    python -m venv venv
    source venv/Scripts/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    python app.py

API - запросы будут доступны по адресу: http://localhost:8000/

## Примеры запросов:

###Для добавления и обновления параметра необходим 

POST запрос на адрес /api/parameters/<user>/<name>/<type>/ со словарем в теле запроса:

    {
        "value": "Значение параметра"
    }

###Для получения параметра:

GET запрос на адрес /api/parameters/<user>/<name>/<type>/ со словарем в теле запроса:

Пример ответа:

    {   
        "name": "имя параметра",
        "type": "тип параметра",
        "value": "Значение параметра"
    }

###Получить все параметры юзера:

GET запрос на адрес /api/parameters/<user>/

Пример ответа:

    {   
        "name": "имя параметра",
        "type": "тип параметра",
        "value": "Значение параметра"
    }

### Добавление параметров через json-API:

POST запрос на адрес /api/<user>/ в формате:

    {
        "Query":
            [
                {
                    "Operation":"SetParam",
                    "Name": "Имя параметра",
                    "Type": "Тип параметра",
                    "Value":"Значение параметра"
                }
            ]
    }

Пример ответа:

    {
        "Result":
            [
                {
                    "Operation":"SetParam",
                    "name": "Имя параметра",
                    "type": "Тип параметра",
                    "Status":"OK|ERROR"
                }
            ]
    }


### Автор
Паша Калинин 