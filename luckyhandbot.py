# -*- coding: utf-8 -*- 
import logging
from check_state import message_checker, callback_checker
from telegram.ext import (Updater, CommandHandler, MessageHandler, Dispatcher, Filters, CallbackQueryHandler, InlineQueryHandler)
from queue import Queue
from threading import Thread
from telegram import Bot


TOKEN = "214791499:AAF2UzWddc_CN-sqliyke3cMFFaBmGxf06c"  # luckyhandbot (production)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Test succeed')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def test(bot, update):
    bot.sendMessage(update.message.chat_id, text='Test succeed')


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.INFO)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", message_checker))
    dp.add_handler(CommandHandler("support", message_checker))
    dp.add_handler(MessageHandler([Filters.text], message_checker))
    dp.add_handler(CallbackQueryHandler(callback_checker))
    # dp.add_handler(RegexHandler('1111', skip_create))
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
