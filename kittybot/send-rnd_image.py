import requests
from telegram import Bot

bot = Bot(token='<Token>')
chat_id = 'Chat_ID'

URL = 'https://api.thecatapi.com/v1/images/search'
# Сделаем GET-запрос к API
# метод json() преобразует полученный ответ JSON в тип данных, понятный Python
response = requests.get(URL).json()
random_cat_url = response[0].get('url')

bot.send_photo(chat_id, random_cat_url)
