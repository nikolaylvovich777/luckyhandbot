# -*- coding: utf-8 -*-
from db_connector import sql, c, sql_select
from lib import keyboard, lang_dicts
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply

FEEDBACK_ADMIN_CHAT = -171376739  # production


def open_feedback(bot, update):
    message_list = ''
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    lang = sql_select('lang', 'users', 'user_id = %s' % user_id)[0]
    sql.execute("UPDATE users SET state='FEEDBACK' WHERE user_id = %s;" % user_id)
    c.commit()
    sql.execute("SELECT author_name, date, text FROM feedback WHERE feedback_user_id = %s;" % user_id)
    for row in sql.fetchall():
        third = row[2]
        if not third:
            third = ' '
        message_list = message_list + '*' + row[0] + '\n' + row[1] + '*' + '\n' + third + '\n' + '\n'
    text = message_list + lang_dicts.feedback_answer[lang]
    bot.sendMessage(chat_id, text=text, reply_markup=keyboard.feedback_keyboard(lang), parse_mode='markdown')


def new_message(bot, update):
    message = update.message
    user_from = update.message.from_user
    lang = sql_select('lang', 'users', 'user_id = %s' % user_from.id)[0]
    # запись сообщения в бд
    sql.execute("INSERT INTO feedback(feedback_user_id, date, text, author, author_name, message_id, query_id) VALUES (%s, %s, %s, %s, 'You', null, null) RETURNING id;",
                (user_from.id, message.date, message.text, user_from.id))
    feedback_id = sql.fetchone()[0]
    sql.execute("UPDATE users SET state='FEEDBACK' WHERE user_id = %s;" % user_from.id)
    c.commit()
    # отправка сообщения пользователю
    bot.sendMessage(message.chat_id, text=lang_dicts.feedback_save_answer[lang], reply_markup=keyboard.feedback_keyboard(lang))
    # отправка сообщения админам
    text = u'Id обращения: ' + str(feedback_id) + '\n' + user_from.name + u' пишет: ' + message.text
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Ответить', callback_data='111')]])
    bot.sendMessage(FEEDBACK_ADMIN_CHAT, text=text, reply_markup=reply_markup)


def feedback_start_answer(bot, update):
    query = update.callback_query
    user_from = update.callback_query.from_user
    message = update.callback_query.message
    # ответить в чат
    feedback_mess_id = message.text[14:][:message.text[14:].find('\n')]
    chat_message = user_from.first_name + ' (' + user_from.name + ')' + u', что передать по обращению ' + feedback_mess_id + '?'
    bot.sendMessage(FEEDBACK_ADMIN_CHAT, text=chat_message, reply_markup=ForceReply())
    # обновление сообщения в чате feedback
    update_message = message.text + '\n* ' + user_from.first_name + u'(' + user_from.name + u') отвечает на сообщение...'
    bot.editMessageText(chat_id=FEEDBACK_ADMIN_CHAT, message_id=message.message_id, text=update_message)
    # запись в бд
    sql.execute("UPDATE feedback SET message_id=%s, query_id=%s WHERE id = %s;", (message.message_id, query.id, feedback_mess_id))
    c.commit()


def feedback_answer(bot, update):
    user_from = update.message.from_user
    message = update.message
    bot_message = update.message.reply_to_message
    feedback_mess_id = bot_message.text[bot_message.text.find(u'ю ') + 2:-1]
    feedback_user_id = sql_select('feedback_user_id', 'feedback', 'id = %s' % feedback_mess_id)[0]
    lang, feedback_username = sql_select('lang, name', 'users', 'user_id = %s' % feedback_user_id)
    message_id, query_id, message_text = sql_select('message_id, query_id, text', 'feedback', 'feedback_user_id = %s ORDER BY 1 DESC' % feedback_user_id)
    # запись сообщения в бд
    sql.execute("INSERT INTO feedback(feedback_user_id, date, text, author, author_name, message_id, query_id) VALUES (%s, %s, %s, %s, 'Support team', %s, %s);",
                (feedback_user_id, message.date, message.text, user_from.id, message_id, query_id))
    c.commit()
    # отправка сообщения пользователю
    bot.sendMessage(feedback_user_id, text=lang_dicts.new_feedback_answer[lang])
    # обновление сообщения в чате feedback
    text = u'Id обращения: ' + str(feedback_mess_id) + u'\n' + feedback_username + u' пишет: ' + message_text + u'\n* ' + user_from.first_name + u'(' + user_from.name + u') ответил на сообщение.'
    bot.editMessageText(chat_id=FEEDBACK_ADMIN_CHAT, message_id=message_id, text=text)
    bot.answerCallbackQuery(query_id, text=u"Отправлено")
