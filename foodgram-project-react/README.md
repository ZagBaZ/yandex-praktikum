# Продуктовый помошник Foodgram 

![api+db+front](https://github.com/zagbaz/foodgram-project-react/actions/workflows/main.yml/badge.svg)

## Описание

---

Проект Foodgram позволяет постить рецепты, делиться и скачивать списки продуктов

>url:  http://84.252.129.152
>
>login: admin@admin.ru
>
>password: admin

## Использованные технологии

- Docker
- postresql
- nginx
- gunicorn
- python
- Django
- Django REST framework

### Инструкции по запуску
- клонируйте репозиторий
```
git clone https://github.com/zagbaz/foodgram-project-react.git
```

- Заполнение .env:
```
Чтобы добавить переменную в .env необходимо открыть файл .env в директории 
infra/ 
директории проекта и поместить туда переменную в формате имя_переменной=значение. 
Пример в файле .env.example
```

- откройте терминал и перейдите в директорию проекта в папку infra/
```
docke-compouse up -d
```
- создание супрепользователя
```
docker-compose exec backend python manage.py createsuperuser
```
- сбор статики и миграци
```
docker-compose exec backend python manage.py collectstatic
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

### Автор:

Автор ZagBaz
