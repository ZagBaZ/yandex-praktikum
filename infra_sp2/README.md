### Проект:
api_yamdb - социальная сеть

# Добро пожаловать, api_yamdb!

**Yamdb** - это cоциальная сеть для поиска музыкальных произведения, книг и фильмов. Здесь Вы сможете найти понравившееся Вам произведение по названию, жанру или категории, зарегистрироваться и оценивать произведение, а так же оставлять свои отзывы для других участников. Enjoy it!

## Технологии

В проекте используются технологии:

- Python 3.7
- Джанго 2.2.19
- Docker
- nginx
- gunicorn

## Как запустить проект в dev-режиме

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/ZagBaZ/infra_sp2.git
```

```
cd infra/
```

2. Скопировать и заполнить env-файл

```
cp .env.example .env
```
```
nano .env
```

3. Запустить docker-compose:

```
docker-compose up -d
```

4. Выполнить миграции внутри контейнера web:

```
docker-compose exec web python manage.py migrate
```

```
docker-compose exec web python manage.py createsuperuser
```

```
docker-compose exec web python manage.py collectstatic --no-input
```

Запускаем по адресу: http://localhost/

## Алгоритм регистрации пользователей


1. Для того, чтобы добавить пользователя отправьте POST-запрос с параметрами Вашего email и username на эндпоинт:

```
http://127.0.0.1:8000/api/v1/auth/signup/
```

2. В ответном письме YaMDB отправит письмо с кодом подтверждения (confirmation_code) на указанный email-адрес.


3. Чтобы получить token (JWT-токен) отправьте POST-запрос с параметрами username и confirmation_code на эндпоинт:

```
http://127.0.0.1:8000/api/v1/auth/token/ 
```

4. Если хотите рассказать нам о себе и заполнить поля в своем профиле, то отправте PATCH-запрос на эндпоинт ниже:

```
http://127.0.0.1:8000/api/v1/users/me/ 
```
 
Описание полей более подробно представлены в документации
 


## В приложении можно выполнять следующие запросы к API:

```
http://127.0.0.1:8000/api/v1/
```

```
"users": http://127.0.0.1:8000/api/v1/users/
```

```
"titles": http://127.0.0.1:8000/api/v1/titles/
```

```
"categories": http://127.0.0.1:8000/api/v1/categories/
```

```
 "genres": http://127.0.0.1:8000/api/v1/genres/
```


**Полный список запросов смотрите по адресу:**

```
http://127.0.0.1:8000/redoc/
```


## Примеры запросов к API и возможности приложения:


**CATEGORIES**


***GET***

```
http://127.0.0.1:8000/api/v1/categories/?limit=1&offset=0
```

```
http://127.0.0.1:8000/api/v1/categories/book/
```


**Пример просмотра категорий с помощью search**

```
http://127.0.0.1:8000/api/v1/categories/?search=Фильм
```



**GENRES**

```
http://127.0.0.1:8000/api/v1/genres/?search=Драма
```



**TITLES**

***Пример запроса произведения по id***

```
http://127.0.0.1:8000/api/v1/titles/1/
```


***Так же есть возможность фильтрации по жанрам, категориям, названию и году***

***GET***

```
http://127.0.0.1:8000/api/v1/titles/?category=movie&genre=drama&name=&year=
```

***response***

```
{
    "count": 5,
    "next": "http://127.0.0.1:8000/api/v1/titles/?category=movie&genre=drama&name=&page=2&year=",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Побег из Шоушенка",
            "year": 1994,
            "rating": 10,
            "description": null,
            "genre": [
                {
                    "name": "Драма",
                    "slug": "drama"
                }
            ],
            "category": {
                "name": "Фильм",
                "slug": "movie"
            }
        },
        {
            "id": 2,
            "name": "Крестный отец",
            "year": 1972,
            "rating": 4,
            "description": null,
            "genre": [
                {
                    "name": "Драма",
                    "slug": "drama"
                }
            ],
            "category": {
                "name": "Фильм",
                "slug": "movie"
            }
        },
        {
            "id": 3,
            "name": "12 разгневанных мужчин",
            "year": 1957,
            "rating": 7,
            "description": null,
            "genre": [
                {
                    "name": "Драма",
                    "slug": "drama"
                }
            ],
            "category": {
                "name": "Фильм",
                "slug": "movie"
            }
        }
    ]
}
```



***POST***

```
{
"name": "string",
"year": 2000,
"description": "string",
"genre": [
          "string",
          "string"
],
"category": "book"
}
```



***PATCH***

```
http://127.0.0.1:8000/api/v1/titles/5/
{
"name": "string",
"year": 2022,
"description": "string",
"genre": [
          "skazka",
          "rock"
]
}
```


## Авторы

TeamLeader: _*[#ZagBaZ](https://github.com/ZagBaZ)*_

User program block create by _*[#eathdarc](https://github.com/eathdarc)*_

Title program block create by  _*[#MaryNix](https://github.com/MaryNix)*_

Review and Comments program block create by _*[#ZagBaZ](https://github.com/ZagBaZ)*_
