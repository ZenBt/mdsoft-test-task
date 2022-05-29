# mdsoft-test-task
## Тестовое задание для MediaSoft.team
[**Ссылка на исходное ТЗ**](https://drive.google.com/file/d/1DU2-MSCNN-FzCa8ksB3rx2GQy23LSt5T/view?usp=sharing)
## Выполнил
Игорь ZenBt Ткаченко
## Описание проекта
REST-api сервис по трекингу Магазинов.
### Добавление магазина 
`POST /shop/`, content_type='application/json' \
Формат запроса: 
`{  
    "name": "Shop name",  
    "city": 1,  
    "street": 3,  
    "house_number": 45,  
    "open_time": "10:00:00",  
    "close_time": "22:00:00"  
}`  
### Просмотр списка магазинов
`GET /shop/?street=&city=&open=0/1` \
Метод принимает параметры дл фильтрации. **Параметры не обзательны**. В случае отсутствия параметров выводтся все магазины, если хоть один параметр есть, то по нему выполнется фильтрация.
#### Пример запроса /shop/?city=1&street=2&open=1
`
[  
    {  
        "id": 3,  
        "name": "BK",  
        "city": "Krd",  
        "street": "Mira",  
        "house_number": 2,  
        "open_time": "09:00:00",  
        "close_time": "19:00:00"  
    }  
]  
`
### Просмотр списка городов
`GET /city/`  \
Формат ответа:  \
`
[  
    {  
        "name": "Krd"  
    },  
    { 
        "name": "Spb"  
    }  
]  
`
### Просмотр списка улиц
`GET /city/street/` — получение всех улиц города;  \
(city_id — идентификатор города)  

### Добавления города/улицы
Осуществляется администратором через `/admin/`  

## Установка
`git clone https://github.com/ZenBt/mdsoft-test-task.git` \
Создать виртуальное окружени (например через `python3 -m venv venv` \
Активировать venv `source venv/bin/activate` и установить необходимые пакеты \
`pip install -r mdsoft-test-task/requirements.txt`
Для работы необходим установленный PostgreSQL
Данные о созданном пользователе необходимо внести в переменные окружения
`export PG_NAME="название бд"` \
`export PG_USER="имя пользователя бд"` \
`export PG_PASSWORD="пароль для бд"` \
`export PG_HOST="localhost"` \
Создать секретный ключ \
`export SECRET_KEY="VerySecretKeyDjango123123"` \
Создать админа через \
`python manage.py createsuperuser` 
## Запуска на локальной машине
`python manage.py runserver`


