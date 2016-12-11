# -*- coding: utf-8 -*-
import time
from datetime import datetime, timedelta
from url_shortener import url_shortener
import game.currency_lib
from admin.feedback import open_feedback
from admin.balance import BALANCE_ADMIN_CHAT
from db_connector import sql, c, sql_select
from game.handler import start_game, BOT
from lib import keyboard, lang_dicts, system_dicts
from lib.system_dicts import money_input_currency, money_input_sum, money_input_desc
import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# noinspection PyTypeChecker
def start(bot, update):
    chat_id = update.message.chat_id
    user_name = update.message.from_user.name
    user_id = update.message.from_user.id
    check_user = sql_select('id', 'users', 'user_id = %s' % user_id)[0]
    referral_user_id = update.message.text[7:]
    if not referral_user_id:
        referral_user_id = None
    if not check_user:
        sql.execute(
            "INSERT INTO users(user_id, name, state, lang, diamond, dollar, rouble, referral_user_id) VALUES (%s, %s, %s, null, 300, 0, 0, %s);",
            (user_id, user_name, 'CHOOSE_LANG', referral_user_id))
    else:
        sql.execute("UPDATE users SET name = '%s', state='CHOOSE_LANG' WHERE user_id = '%s';" % (user_name, user_id))
    bot.sendMessage(chat_id, text="Choose language", reply_markup=keyboard.lang_keyboard())
    c.commit()


def choose_lang(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    text = update.message.text
    if text in (u'English \U0001f1fa\U0001f1f8', u'Русский \U0001f1f7\U0001f1fa', u'Espa\xf1ol \U0001f1ea\U0001f1f8',
                u'Deutch \U0001f1e9\U0001f1ea', u'Italiano \U0001f1ee\U0001f1f9', u'Fran\xe7ais \U0001f1eb\U0001f1f7',
                u'Polski \U0001f1f5\U0001f1f1', u'\u0641\u0627\u0631\u0652\u0633\u0650\u0649\U0001f1ee\U0001f1f7',
                u'O\u02bbzbek \U0001f1fa\U0001f1ff'):
        lang = lang_dicts.lang_answer_v2[text]
        sql.execute("UPDATE users SET state='MENU', lang='%s' WHERE user_id = %s;" % (lang, user_id))
        c.commit()
        diamond, cash = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users', 'user_id = %s' % user_id)

        bot.sendMessage(chat_id, text=lang_dicts.menu_answer[lang] % (diamond, cash),
                        reply_markup=keyboard.menu_keyboard(lang))


def menu(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    pressed_button = update.message.text
    lang = sql_select('lang', 'users', 'user_id = %s' % user_id)[0]
    diamond, cash = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users', 'user_id = %s' % user_id)
    last_game_currency = sql_select('last_game_currency', 'users', 'user_id = %s' % user_id)[0]
    referral_user_id = sql_select('referral_user_id', 'users', 'user_id = %s' % user_id)[0]
    now = datetime.now()
    if pressed_button == lang_dicts.play_di_button[lang]:
        if diamond < 50:
            sql.execute("UPDATE users SET state='MONEY_INPUT' WHERE user_id = %s;" % user_id)
            c.commit()
            request_result = sql_select('diamond_request_time', 'users', 'diamond_request_time IS NOT NULL AND user_id = %s' % user_id)[0]
            if not request_result:
                sql.execute("UPDATE users SET diamond_request_time='%s'  WHERE user_id = %s;" % (now.strftime("%Y-%m-%d %H:%M:%S"), user_id))
                c.commit()
                diamond_reload_text = lang_dicts.diamond_reload_answer[lang] % '2:00:00'
            else:
                diamond_request_time = datetime.strptime(request_result, '%Y-%m-%d %H:%M:%S')
                diamond_request_timer = diamond_request_time - datetime.now() + timedelta(hours=2)
                diamond_reload_text = lang_dicts.diamond_reload_answer[lang] % str(diamond_request_timer).split('.', 2)[0]
            bot.sendMessage(chat_id, text=lang_dicts.money_input_answer[lang] % (diamond, cash, diamond_reload_text), reply_markup=keyboard.money_input_keyboard(lang))
        else:
            if not last_game_currency and referral_user_id is not None:
                referral_first_prize(referral_user_id)
            sql.execute("UPDATE users SET state='SEARCHING', last_game_currency='%s', last_game_time='%s'  WHERE user_id = %s;" % ('diamond', now.strftime("%Y-%m-%d %H:%M:%S"), user_id))
            c.commit()
            search_opponent(bot, update)
    elif pressed_button == lang_dicts.play_cash_button[lang]:
        if cash < lang_dicts.play_cash_min[lang]:
            sql.execute("UPDATE users SET state='MONEY_INPUT' WHERE user_id = %s;" % user_id)
            c.commit()
            request_result = sql_select('diamond_request_time', 'users', 'diamond_request_time IS NOT NULL AND user_id = %s' % user_id)[0]
            if not request_result:
                diamond_reload_text = ''
            else:
                diamond_request_time = datetime.strptime(request_result, '%Y-%m-%d %H:%M:%S')
                diamond_request_timer = diamond_request_time - datetime.now() + timedelta(hours=2)
                diamond_reload_text = lang_dicts.diamond_reload_answer[lang] % str(diamond_request_timer).split('.', 2)[0]
            bot.sendMessage(chat_id, text=lang_dicts.money_input_answer[lang] % (diamond, cash, diamond_reload_text), reply_markup=keyboard.money_input_keyboard(lang))
        else:
            if not last_game_currency and referral_user_id is not None:
                referral_first_prize(referral_user_id)
            sql.execute("UPDATE users SET state='SEARCHING', last_game_currency='%s', last_game_time='%s'  WHERE user_id = %s;" %
                        (lang_dicts.currency[lang], now.strftime("%Y-%m-%d %H:%M:%S"), user_id))
            c.commit()
            search_opponent(bot, update)
    elif pressed_button == lang_dicts.money_input_button[lang]:
        sql.execute("UPDATE users SET state='MONEY_INPUT' WHERE user_id = %s;" % user_id)
        c.commit()
        request_result = sql_select('diamond_request_time', 'users', 'diamond_request_time IS NOT NULL AND user_id = %s' % user_id)[0]
        if not request_result:
            diamond_reload_text = ''
        else:
            diamond_request_time = datetime.strptime(request_result, '%Y-%m-%d %H:%M:%S')
            diamond_request_timer = diamond_request_time - datetime.now() + timedelta(hours=2)
            diamond_reload_text = lang_dicts.diamond_reload_answer[lang] % str(diamond_request_timer).split('.', 2)[0]
        bot.sendMessage(chat_id, text=lang_dicts.money_input_answer[lang] % (diamond, cash, diamond_reload_text),
                        reply_markup=keyboard.money_input_keyboard(lang))
    elif pressed_button == lang_dicts.feedback_button[lang]:
        sql.execute("UPDATE users SET state='FEEDBACK' WHERE user_id = %s;" % user_id)
        c.commit()
        open_feedback(bot, update)
    elif pressed_button == lang_dicts.invite_button[lang]:
        bot.sendMessage(chat_id, text=lang_dicts.invite_answer[lang] % user_id)
    elif pressed_button == lang_dicts.help_button[lang]:
        bot.sendMessage(chat_id, text=lang_dicts.help_answer[lang] % user_id)
    elif pressed_button == lang_dicts.rate_button[lang]:
        bot.sendMessage(chat_id, text=lang_dicts.rate_answer[lang])


def feedback(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    pressed_button = update.message.text
    lang = sql_select('lang', 'users', 'user_id = %s' % user_id)[0]
    if pressed_button == lang_dicts.add_feedback_button[lang]:
        bot.sendMessage(chat_id, text=lang_dicts.add_feedback_answer[lang], reply_markup=keyboard.hide_keyboard)
        sql.execute("UPDATE users SET state='NEW_FEEDBACK' WHERE user_id = %s;" % user_id)
    elif pressed_button == lang_dicts.menu_back_button[lang]:
        bot.sendMessage(chat_id, text=lang_dicts.menu_back_answer[lang], reply_markup=keyboard.menu_keyboard(lang))
        sql.execute("UPDATE users SET state='MENU' WHERE user_id = %s;" % user_id)
    c.commit()


def search_opponent(bot, update):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    lang = sql_select('lang', 'users', 'user_id = %s' % user_id)[0]
    currency = sql_select('last_game_currency', 'users', 'user_id = %s' % user_id)[0]
    bot.sendMessage(chat_id, text=lang_dicts.searching_answer[lang], reply_markup=keyboard.hide_keyboard)
    opponent_user_id = sql_select("user_id", "users",
                                  "(state='SEARCHING' OR state='NOT_FOUND') AND user_id != %s AND last_game_currency = '%s'" % (
                                      user_id, currency))[0]
    time.sleep(1.5)
    if not opponent_user_id:
        sql.execute("UPDATE users SET state='NOT_FOUND' WHERE user_id = %s;" % user_id)
        c.commit()
        bot.sendMessage(chat_id, text=lang_dicts.not_found_answer[lang],
                        reply_markup=keyboard.pre_play_keyboard(lang))
    else:
        sql.execute("UPDATE users SET state='IN_GAME' WHERE user_id IN (%s, %s);" %
                    (user_id, opponent_user_id))
        c.commit()
        start_game(bot, update, lang, opponent_user_id, None)


def opponent_not_found(bot, update):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    pressed_button = update.message.text
    lang = sql_select('lang', 'users', 'user_id = %s' % user_id)[0]
    if pressed_button == lang_dicts.keep_wait_button[lang]:
        sql.execute("UPDATE users SET state='SEARCHING' WHERE user_id = %s;" % user_id)
        c.commit()
        search_opponent(bot, update)
    elif pressed_button == lang_dicts.play_with_bot_button[lang]:
        opponent_user_id = BOT
        sql.execute("UPDATE users SET state='IN_GAME' WHERE user_id = %s;" % user_id)
        c.commit()
        start_game(bot, update, lang, opponent_user_id, None)
    elif pressed_button == lang_dicts.discard_game_button[lang]:
        bot.sendMessage(chat_id, text=lang_dicts.menu_back_answer[lang], reply_markup=keyboard.menu_keyboard(lang))
        sql.execute("UPDATE users SET state='MENU' WHERE user_id = %s;" % user_id)
    elif pressed_button == lang_dicts.invite_button[lang]:
        bot.sendMessage(chat_id, text=lang_dicts.invite_in_play_answer_p1[lang])
        bot.sendMessage(chat_id, text=lang_dicts.invite_in_play_answer_p2[lang] % user_id)
    c.commit()


def play_again(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    pressed_button = update.message.text
    now = datetime.now()
    lang, last_game_id, currency = sql_select('lang, last_game_id, last_game_currency', 'users', 'user_id = %s' % user_id)
    opponent1_id = sql_select('opponent1_id', 'game', 'id = %s' % last_game_id)[0]
    opponent2_id = sql_select('opponent2_id', 'game', 'id = %s' % last_game_id)[0]
    if opponent1_id == user_id:
        opponent_user_id = opponent2_id
    else:
        opponent_user_id = opponent1_id
    if pressed_button == lang_dicts.play_again_button[lang]:
        diamond, cash = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users', 'user_id = %s' % user_id)
        if (currency == 'diamond' and diamond < 50) or (currency == lang_dicts.currency[lang] and cash < lang_dicts.play_cash_min[lang]):
            sql.execute("UPDATE users SET state='MONEY_INPUT' WHERE user_id = %s;" % user_id)
            c.commit()
            request_result = sql_select('diamond_request_time', 'users', 'diamond_request_time IS NOT NULL AND user_id = %s' % user_id)[0]
            if not request_result and currency == 'diamond':

                sql.execute("UPDATE users SET diamond_request_time='%s'  WHERE user_id = %s;" % (now.strftime("%Y-%m-%d %H:%M:%S"), user_id))
                c.commit()
                diamond_reload_text = lang_dicts.diamond_reload_answer[lang] % '2:00:00'
            elif not request_result and currency == lang_dicts.currency[lang]:
                diamond_reload_text = ''
            else:
                diamond_request_time = datetime.strptime(request_result, '%Y-%m-%d %H:%M:%S')
                diamond_request_timer = diamond_request_time - datetime.now() + timedelta(hours=2)
                diamond_reload_text = lang_dicts.diamond_reload_answer[lang] % str(diamond_request_timer).split('.', 2)[0]
            bot.sendMessage(chat_id, text=lang_dicts.money_input_answer[lang] % (diamond, cash, diamond_reload_text), reply_markup=keyboard.money_input_keyboard(lang))
        else:
            # если с ботом, то сразу идем играть
            if opponent_user_id == BOT:
                sql.execute("UPDATE users SET state='IN_GAME', last_game_time='%s' WHERE user_id = %s;" % (now.strftime("%Y-%m-%d %H:%M:%S"), user_id))
                c.commit()
                start_game(bot, update, lang, opponent_user_id, last_game_id)
            elif not opponent_user_id:
                bot.sendMessage(chat_id, text=lang_dicts.opponent_exit[lang], reply_markup=keyboard.menu_keyboard(lang))
                sql.execute("DELETE FROM game WHERE id=%s;" % last_game_id)
                sql.execute("UPDATE users SET state='MENU' WHERE user_id = %s;" % user_id)
                c.commit()
            else:
                opponent_state = sql_select('state', 'users', 'user_id = %s' % opponent_user_id)[0]
                if opponent_state == 'PLAY_AGAIN':
                    bot.sendMessage(chat_id, text=lang_dicts.waiting_opponent_answer[lang])
                    sql.execute("UPDATE users SET state='WAIT_OPPONENT' WHERE user_id = %s;" % user_id)
                    c.commit()
                elif opponent_state == 'WAIT_OPPONENT':
                    sql.execute("UPDATE users SET state='IN_GAME', last_game_time='%s' WHERE user_id IN (%s, %s);" % (now.strftime("%Y-%m-%d %H:%M:%S"), user_id, opponent_user_id))
                    c.commit()
                    start_game(bot, update, lang, opponent_user_id, last_game_id)
                else:
                    bot.sendMessage(chat_id, text=lang_dicts.opponent_exit[lang])
                    sql.execute("DELETE FROM game WHERE id=%s;" % last_game_id)
                    c.commit()
                    search_opponent(bot, update)
    elif pressed_button == lang_dicts.exit_game_button[lang]:
        if opponent1_id == user_id:
            sql.execute("UPDATE game SET opponent1_id=null WHERE id = %s;" % last_game_id)
        else:
            sql.execute("UPDATE game SET opponent2_id=null WHERE id = %s;" % last_game_id)
        sql.execute("UPDATE users SET state='MENU' WHERE user_id = %s;" % user_id)
        bot.sendMessage(chat_id, text=lang_dicts.menu_back_answer[lang], reply_markup=keyboard.menu_keyboard(lang))
        if not opponent_user_id:
            sql.execute("DELETE FROM game WHERE id=%s;" % last_game_id)
            c.commit()
        else:
            opponent_state, lang2 = sql_select('state, lang', 'users', 'user_id = %s' % opponent_user_id)
            if opponent_state == 'WAIT_OPPONENT' or opponent_user_id == BOT:
                sql.execute("DELETE FROM game WHERE id=%s;" % last_game_id)
                if opponent_user_id != BOT:
                    bot.sendMessage(opponent_user_id, text=lang_dicts.opponent_exit[lang2],
                                    reply_markup=keyboard.menu_keyboard(lang2))
                    sql.execute("UPDATE users SET state='MENU' WHERE user_id = %s;" % opponent_user_id)
        c.commit()


def money_input(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.name
    message = update.message.text
    lang = sql_select('lang', 'users', 'user_id = %s' % user_id)[0]
    if message == lang_dicts.menu_back_button[lang]:
        bot.sendMessage(chat_id, text=lang_dicts.menu_back_answer[lang], reply_markup=keyboard.menu_keyboard(lang))
        sql.execute("UPDATE users SET state='MENU' WHERE user_id = %s;" % user_id)
        c.commit()
    elif message == lang_dicts.withdraw_button[lang]:
        bot.sendMessage(chat_id, text=lang_dicts.withdraw_answer[lang], parse_mode='markdown')
    elif message in keyboard.MONEY_BUTTONS:
        bot.sendMessage(chat_id, text=kassa_link(update))
    elif message[:2] == '+7':
        if re.match('\+\d-\d\d\d-\d\d\d-\d\d-\d\d\s\d', message):
            out_sum = message[17:]
            balance = sql_select(lang_dicts.currency[lang], 'users', 'user_id = %s' % user_id)[0]
            if float(out_sum) > float(balance):
                bot.sendMessage(chat_id, text=lang_dicts.not_enough_funds_answer[lang])
            elif float(out_sum) < system_dicts.withdraw_min[lang]:
                bot.sendMessage(chat_id, text=lang_dicts.less_than_min_answer[lang])
            else:
                bot.sendMessage(chat_id, text=lang_dicts.request_accepted_answer[lang])
                sql.execute("UPDATE users SET %s = %s - %s WHERE user_id = %s;" % (lang_dicts.currency[lang], lang_dicts.currency[lang], out_sum, user_id))
                c.commit()
                reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Уведомить пользователя об исполнении', callback_data='1')]])
                bot.sendMessage(BALANCE_ADMIN_CHAT, text=u'Пользователь %s (%s) запросил вывод средств на сумму %s %s на номер %s' % (username, user_id, out_sum, system_dicts.currency_lib[lang_dicts.currency[lang]], message[:16]), reply_markup=reply_markup)

        else:
            bot.sendMessage(chat_id, text=lang_dicts.bad_format_answer[lang])


def old_game_cleaner(bot):
    finish_time = datetime.now() - timedelta(minutes=2)
    sql.execute("SELECT id, opponent1_id, opponent2_id, opponent1_choose, opponent2_choose FROM game WHERE start_time <= '%s'" % finish_time.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        rows = sql.fetchall()
        for row in rows:
            game_id = row[0]
            opponent1_id = row[1]
            opponent2_id = row[2]
            opponent1_choose = row[3]
            opponent2_choose = row[4]
            opponent1_name, lang, currency = sql_select('name, lang, last_game_currency', 'users', 'user_id = %s' % opponent1_id)
            if opponent2_id is None:
                opponent2_name = None
                lang2 = lang
            elif opponent2_id == BOT:
                opponent2_name = 'BOT'
                lang2 = lang
            else:
                opponent2_name, lang2 = sql_select('name, lang', 'users', 'user_id = %s' % opponent2_id)
            sql.execute("DELETE FROM game WHERE id=%s;" % game_id)
            c.commit()
            if not opponent1_choose and not opponent2_choose:
                sql.execute(
                    "UPDATE users SET state='MENU' WHERE user_id IN (%s, %s);" % (opponent1_id, opponent2_id))
                c.commit()
                diamond, cash = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users', 'user_id = %s' % opponent1_id)
                diamond2, cash2 = sql_select('diamond, %s' % lang_dicts.currency[lang2], 'users', 'user_id = %s' % opponent2_id)
                bot.sendMessage(opponent1_id, text=lang_dicts.old_game_answer[lang] % (opponent1_name, opponent2_name, diamond, cash), parse_mode='markdown', reply_markup=keyboard.menu_keyboard(lang))
                if opponent2_id != BOT:
                    bot.sendMessage(opponent2_id, text=lang_dicts.old_game_answer[lang2] % (opponent2_name, opponent1_name, diamond2, cash2), parse_mode='markdown', reply_markup=keyboard.menu_keyboard(lang2))
            elif opponent1_choose is not None and not opponent2_choose:
                sql.execute("UPDATE users SET %s = (%s + %s), state='PLAY_AGAIN' WHERE user_id=%s;" % (currency, currency, game.currency_lib.prize[currency], opponent1_id))
                sql.execute(
                    "UPDATE users SET %s = (%s - %s), state='PLAY_AGAIN' WHERE user_id=%s;" % (currency, currency, game.currency_lib.loss[currency], opponent2_id))
                c.commit()
                diamond, cash = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users', 'user_id = %s' % opponent1_id)
                diamond2, cash2 = sql_select('diamond, %s' % lang_dicts.currency[lang2], 'users', 'user_id = %s' % opponent2_id)
                bot.sendMessage(opponent1_id, text=lang_dicts.winner_answer[lang] % (opponent1_name, system_dicts.hands_revert[opponent1_choose], game.currency_lib.pot[currency], opponent2_name, u'\U0001F55A', diamond, cash), parse_mode='markdown', reply_markup=keyboard.play_again_keyboard(lang))
                bot.sendMessage(opponent2_id, text=lang_dicts.loser_answer[lang2] % (opponent2_name, u'\U0001F55A', opponent1_name, system_dicts.hands_revert[opponent1_choose], game.currency_lib.pot[currency], diamond2, cash2), parse_mode='markdown', reply_markup=keyboard.play_again_keyboard(lang2))
            elif opponent2_choose is not None and not opponent1_choose:
                sql.execute("UPDATE users SET %s = (%s + %s), state='PLAY_AGAIN' WHERE user_id=%s;" % (currency, currency, game.currency_lib.prize[currency], opponent2_id))
                sql.execute(
                    "UPDATE users SET %s = (%s - %s), state='PLAY_AGAIN' WHERE user_id=%s;" % (currency, currency, game.currency_lib.loss[currency], opponent1_id))
                c.commit()
                diamond, cash = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users', 'user_id = %s' % opponent1_id)
                diamond2, cash2 = sql_select('diamond, %s' % lang_dicts.currency[lang2], 'users', 'user_id = %s' % opponent2_id)
                bot.sendMessage(opponent1_id, text=lang_dicts.loser_answer[lang] % (opponent1_name, u'\U0001F55A', opponent2_name, system_dicts.hands_revert[opponent2_choose], game.currency_lib.pot[currency], diamond, cash), parse_mode='markdown', reply_markup=keyboard.play_again_keyboard(lang))
                bot.sendMessage(opponent2_id, text=lang_dicts.winner_answer[lang2] % (opponent2_name, system_dicts.hands_revert[opponent2_choose], game.currency_lib.pot[currency], opponent1_name, u'\U0001F55A', diamond2, cash2), parse_mode='markdown', reply_markup=keyboard.play_again_keyboard(lang2))
    except IndexError:
        return None
    return


def diamond_reload(bot):
    gift_time = datetime.now() - timedelta(hours=2)
    sql.execute("SELECT user_id, lang FROM users WHERE diamond_request_time <= '%s'" % gift_time.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        rows = sql.fetchall()
        for row in rows:
            user_id = row[0]
            lang = row[1]
            print(user_id)
            bot.sendMessage(60558942, text=lang_dicts.diamond_gift_answer[lang], reply_markup={'resize_keyboard': True, 'one_time_keyboard': False, 'keyboard': [[{'text': lang_dicts.diamond_gift_button[lang]}]]})
            sql.execute("UPDATE users SET state='GIFT', diamond_request_time = null WHERE user_id = %s;" % user_id)
            c.commit()
    except IndexError:
        return None
    return


def get_gift(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    lang = sql_select('lang', 'users', 'user_id = %s' % user_id)[0]
    sql.execute("UPDATE users SET state='MENU', diamond = (diamond + 250) WHERE user_id = %s;" % user_id)
    c.commit()
    diamond, cash = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users', 'user_id = %s' % user_id)
    bot.sendMessage(chat_id, text=lang_dicts.balance_answer[lang] % (diamond, cash))
    bot.sendMessage(chat_id, text=lang_dicts.menu_back_answer[lang], reply_markup=keyboard.menu_keyboard(lang))


def kassa_link(update):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    pressed_button = update.message.text
    ik_num = sql_select('ik_num', 'users', 'user_id = %s' % user_id)[0]
    sql.execute("UPDATE users SET ik_num = (ik_num + 1) WHERE user_id = %s;" % user_id)
    c.commit()
    ik_desc = u'Платеж от пользователя %s на сумму %s' % (user_name, money_input_desc[pressed_button])
    link = u'https://sci.interkassa.com/?ik_co_id=573221553b1eaf5e468b4569&ik_pm_no=ID_%s_NUM_%s&ik_am=%s&ik_cur=%s&ik_desc=%s&ik_pw_off=%s#/paysystemList' % (user_id, ik_num, money_input_sum[pressed_button], money_input_currency[pressed_button], ik_desc, 'okpay%3Bpayeer%3Bvisa%3Bmastercard%3Bperfectmoney%3Bpaxum%3Bbitcoin%3Bbtce')
    short_link = url_shortener(link)
    return short_link


def referral_first_prize(referral_user_id):
    sql.execute("UPDATE users SET diamond = (diamond + 300) WHERE user_id = %s;" % referral_user_id)
    c.commit()
    return
