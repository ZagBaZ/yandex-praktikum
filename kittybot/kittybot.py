import requests
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import ReplyKeyboardMarkup

# Token
updater = Updater(token='<Token telegram>')

# Id
chat_id = '<Chat_ID>'

URL = 'https://api.thecatapi.com/v1/images/search'


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        print(error)
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text='Hello {}, look at this!!'.format(name),
        reply_markup=button
    )

def main():
# CommandHandler
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))

# MessageHandler;
    updater.dispatcher.add_handler(MessageHandler(Filters.text, new_cat))

# polling
    updater.start_polling(poll_interval=10.0)

# Бот будет работать до тех пор, пока не нажмете Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()