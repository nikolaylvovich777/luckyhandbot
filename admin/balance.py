# -*- coding: utf-8 -*-
from datetime import datetime

import xlwt

from db_connector import sql, c, sql_select
from lib import lang_dicts, system_dicts
from lib.keyboard import add_balance_keyboard, add_balance_confirm_keyboard

BALANCE_ADMIN_CHAT = -160185514  # production

DOLLAR_ADD = (lang_dicts.dollar_1_button['ENG'], lang_dicts.dollar_2_button['ENG'], lang_dicts.dollar_5_button['ENG'],
              lang_dicts.dollar_8_button['ENG'], lang_dicts.dollar_10_button['ENG'], lang_dicts.dollar_15_button['ENG'])
ROUBLE_ADD = (lang_dicts.dollar_1_button['RUS'], lang_dicts.dollar_2_button['RUS'], lang_dicts.dollar_5_button['RUS'],
              lang_dicts.dollar_8_button['RUS'], lang_dicts.dollar_10_button['RUS'], lang_dicts.dollar_15_button['RUS'])

font0 = xlwt.Font()
font0.name = 'Times New Roman'
font0.bold = True

style0 = xlwt.XFStyle()
style0.font = font0

style1 = xlwt.XFStyle()

wb = xlwt.Workbook()
ws = wb.add_sheet(u'Список', cell_overwrite_ok=True)


def add_balance(bot, update):
    message = update.message.text
    admin_user_id = update.message.from_user.id
    user_id = message[4:]
    now = datetime.now()
    check_user = sql_select('user_id', 'users', 'user_id = %s' % user_id)[0]
    if not check_user:
        bot.sendMessage(BALANCE_ADMIN_CHAT, text=u'нет такого пользователя')
    else:
        sql.execute(
            "INSERT INTO add_balance_requests (admin_user_id, user_id, date) VALUES (%s, %s, %s);",
            (admin_user_id, user_id, now.strftime("%Y-%m-%d %H:%M:%S")))
        c.commit()
        bot.sendMessage(BALANCE_ADMIN_CHAT, text=u'сколько пополнить? или нажмите отмена', reply_markup=add_balance_keyboard)


def add_balance_part2(bot, update, add_sum, currency):
    admin_user_id = update.message.from_user.id
    user_id = sql_select('user_id', 'add_balance_requests', 'admin_user_id=%s AND done = 0' % admin_user_id)[0]
    username = sql_select('name', 'users', 'user_id=%s' % user_id)[0]
    sql.execute("UPDATE add_balance_requests SET currency = '%s', sum = %s WHERE admin_user_id=%s AND done = 0;" % (currency, add_sum, admin_user_id))
    c.commit()
    bot.sendMessage(BALANCE_ADMIN_CHAT, text=u'Добавить пользователю %s (%s) на счет %s %s ?' % (username, user_id, add_sum, system_dicts.currency_lib[currency]), reply_markup=add_balance_confirm_keyboard)


def add_balance_confirm(bot, update):
    admin_user_id = update.message.from_user.id
    user_id, currency, add_sum = sql_select('user_id, currency, sum', 'add_balance_requests', 'admin_user_id=%s AND done = 0' % admin_user_id)
    lang = sql_select('lang', 'users', 'user_id=%s' % user_id)[0]
    sql.execute("UPDATE users SET %s = (%s + %s) WHERE user_id=%s;" % (currency, currency, add_sum, user_id))
    sql.execute("UPDATE add_balance_requests SET done = 1 WHERE admin_user_id=%s AND done = 0;" % admin_user_id)
    c.commit()
    bot.sendMessage(BALANCE_ADMIN_CHAT, text=u'Сделано!\nПользователю отправлено соотвествующее уведомление')
    bot.sendMessage(user_id, text=lang_dicts.add_balance_done[lang])


def stop_add(bot, update):
    admin_user_id = update.message.from_user.id
    sql.execute("DELETE FROM add_balance_requests WHERE admin_user_id=%s AND done = 0;" % admin_user_id)
    c.commit()
    bot.sendMessage(BALANCE_ADMIN_CHAT, text=u'Отменено!')


def admin_help(bot):
    bot.sendMessage(BALANCE_ADMIN_CHAT, text=u'Администраторские команды:\n'
                                             u'*list* - получение списка пользователей и информации о них\n'
                                             u'*add ?id пользователя?* - пополнение баланса пользователя после оплаты'
                                             u' (id пользователя можно узнать через команду list или квитанции интеркассы)\n'
                                             u'*help* - справка', parse_mode='markdown')


def user_list(bot):
    shapka = (u'ID пользователя', u'Имя пользователя', u'Язык пользователя', u'Брилианты', u'Доллары', u'Рубли', u'Когда играл последний раз?', u'На что играл последний раз?')
    y = 0
    for cell in shapka:
        ws.write(0, y, cell, style0)
        y += 1
    sql.execute("SELECT u.user_id, u.name, u.lang, u.diamond, u.dollar, u.rouble, u.last_game_time, u.last_game_currency "
                "FROM users u "
                "WHERE u.user_id != 0;")
    i = 1
    for row in sql.fetchall():
        y = 0
        for cell in row:
            ws.write(i, y, cell, style1)
            y += 1
        i += 1
    wb.save('user_list.xls')
    doc = open('user_list.xls', 'rb')
    bot.sendDocument(BALANCE_ADMIN_CHAT, document=doc)


def withdraw_notify(bot, update):
    message = update.callback_query.message
    user_from = update.callback_query.from_user
    query = update.callback_query
    user_id = update.callback_query.message.text[message.text.find(' (')+2:][:message.text.find(') ')-(message.text.find(' (')+2)]
    lang = sql_select('lang', 'users', 'user_id = %s' % user_id)[0]
    update_message = message.text + '\n\n*' + user_from.first_name + ' (' + user_from.name + ') ' + u'уведомил пользователя'
    bot.sendMessage(user_id, text=lang_dicts.request_executed_answer[lang])
    bot.editMessageText(chat_id=BALANCE_ADMIN_CHAT, message_id=message.message_id, text=update_message)
    bot.answerCallbackQuery(query.id, text=u"Пользователь уведомлен")
