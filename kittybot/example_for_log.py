import logging

logging.basicConfig(level=logging.INFO,
                    filename='main.log',
                    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
                    filemode='w',
                    )

logging.debug('123')  # Когда нужна отладочная информация
logging.info('Сообщение отправлено')  # Когда нужна дополнительная информация
logging.warning('Большая нагрузка!')  # Когда что-то идёт не так, но работает
logging.error('Бот не смог отправить сообщение')  # Когда что-то сломалось
logging.critical('Всё упало! Зовите админа!1!111')  # Когда всё совсем плохо