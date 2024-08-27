from settings import RETRY_TIME, ENDPOINT, HEADERS, HOMEWORK_STATUSES
import logging
import os
import requests
import time
from dotenv import load_dotenv
from telegram import Bot
import telegram

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        logging.info(f'Отправляем сообщение: {message}')
        bot.send_message(TELEGRAM_CHAT_ID, message)
    except telegram.error.BadRequest as error:
        logging.error(f'Сообщение не отправлено! Ошибка {error}')


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    params = {'from_date': current_timestamp}
    homework_api = requests.get(ENDPOINT, headers=HEADERS, params=params)
    homework = homework_api.json()
    try:
        logging.info('отправляем api-запрос')
        response = requests.get(
            ENDPOINT, params=params, headers=HEADERS
        )
    except ValueError as error:
        logging.error(f'{error}: не получили api-ответ')
        raise error
    error_message = (
        f'Проблемы соединения с сервером'
        f'ошибка {response.status_code}'
    )
    if response.status_code == requests.codes.ok:
        return homework
    elif response.status_code != requests.codes.ok:
        logging.error(error_message)
        raise TypeError(error_message)


def check_response(response):
    """Проверяет ответ API на корректность."""
    if type(response) is not dict:
        logging.error('API is not dict')
        raise TypeError("api answer is not dict")
    try:
        homework_list = response['homeworks']
    except KeyError:
        logging.error('dict KeyError')
        raise KeyError('dict KeyError')
    try:
        return homework_list[0]
    except TypeError:
        logging.error('Домашняя работа не найдена!')
        raise IndexError('Домашняя работа не найдена!')


def parse_status(homework):
    """Извлекает статус работы."""
    if 'homework_name' in homework:
        homework_name = homework['homework_name']
    else:
        message = 'в API отсутствует "homework_name"'
        logging.error(message)
        raise KeyError(message)
    if 'status' in homework:
        homework_status = homework['status']
    else:
        message = 'в API отсутствует "status"'
        logging.error(message)
        raise KeyError(message)

    if homework_status in HOMEWORK_STATUSES:
        verdict = HOMEWORK_STATUSES[homework_status]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    tokens_data = {
        'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID
    }
    no_value = [
        var_name for var_name, value in tokens_data.items() if not value
    ]
    if no_value:
        logging.critical(
            f'Отсутствует обязательная/ые переменная/ые окружения: {no_value}.'
            'Программа принудительно остановлена.'
        )
        return False
    logging.info('Необходимые переменные окружения доступны.')
    return True


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical('Ошибка в переменных окружения')
    bot = Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time()) - RETRY_TIME
    last_status = None
    last_error = None
    while True:
        try:
            response = get_api_answer(current_timestamp)
        except Exception as error:
            if str(error) != last_error:
                last_error = str(error)
                send_message(bot, error)
            logging.error(error)
            time.sleep(RETRY_TIME)
            continue
        try:
            homework = check_response(response)
            homework_status = homework.get('status')
            if homework_status != last_status:
                last_status = homework_status
                message = parse_status(homework)
                send_message(bot, message)
            else:
                logging.debug('Статус ДЗ не изменился')
        except Exception as error:
            error = f'Сбой в работе программы: {error}'
            if str(error) != last_error:
                last_error = str(error)
                send_message(bot, error)
            logging.error(error)
        else:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='main.log',
        filemode='a'
    )
    main()
