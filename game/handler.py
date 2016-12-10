#  -*- coding: utf-8 -*-
from datetime import datetime

from game import currency_lib
from db_connector import sql, c, sql_select
from game.compare import compare
from game.random_choice import random_choice
from lib import keyboard, lang_dicts, system_dicts

BOT = 0


def start_game(bot, update, lang, opponent_user_id, last_game_id):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user_name = update.message.from_user.name
    now = datetime.now()
    currency = sql_select('last_game_currency', 'users', 'user_id = %s' % user_id)[0]
    lang2, opponent_name = sql_select('lang, name', 'users', 'user_id = %s' % opponent_user_id)
    if not last_game_id:
        sql.execute(
            "INSERT INTO game (opponent1_id, opponent2_id, opponent1_choose, opponent2_choose, start_time) "
            "VALUES (%s, %s, null, null, %s) RETURNING id;",
            (user_id, opponent_user_id, now.strftime("%Y-%m-%d %H:%M:%S")))
        game_id = sql.fetchone()[0]
        sql.execute(
                "UPDATE users SET last_game_id = %s WHERE user_id IN (%s, %s)" % (game_id, user_id, opponent_user_id))
    else:
        sql.execute(
            "UPDATE game SET start_time = '%s' WHERE id = %s;" % (now.strftime("%Y-%m-%d %H:%M:%S"), last_game_id))
    c.commit()
    pot = currency_lib.pot[currency]
    players_list = user_name + '\n' + opponent_name
    bot.sendMessage(chat_id, text=lang_dicts.start_play_answer[lang] % (pot, players_list), parse_mode='markdown',
                    reply_markup=keyboard.play_keyboard)
    if opponent_user_id != BOT:
        bot.sendMessage(opponent_user_id, text=lang_dicts.start_play_answer[lang2] % (pot, players_list),
                        parse_mode='markdown',
                        reply_markup=keyboard.play_keyboard)


def check_choose(bot, update):
    message = update.message.text
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    opponent = sql_select('opponent1_id', 'game', 'opponent1_id = %s;' % user_id)[0]
    if not opponent:
        opponent = 'opponent2'
        opponent2 = 'opponent1'
        game_id = sql_select('id', 'game', 'opponent2_id = %s;' % user_id)[0]
    else:
        opponent = 'opponent1'
        opponent2 = 'opponent2'
        game_id = sql_select('id', 'game', 'opponent1_id = %s;' % user_id)[0]
    opponent_user_id = sql_select('%s_id' % opponent2, 'game', 'id = %s;' % game_id)[0]
    if opponent_user_id == BOT:
        other_opponent_choose = random_choice()
        sql.execute("UPDATE game SET %s_choose='%s' WHERE id=%s;" % (opponent2, other_opponent_choose, game_id))
        c.commit()
    else:
        other_opponent_choose = sql_select('%s_choose' % opponent2, 'game', 'id = %s;' % game_id)[0]
    lang = sql_select('lang', 'users', 'user_id = %s;' % user_id)[0]
    currency = sql_select('last_game_currency', 'users', 'user_id = %s;' % user_id)[0]
    referral_user_id = sql_select('referral_user_id', 'users', 'user_id = %s;' % user_id)[0]
    lang2 = sql_select('lang', 'users', 'user_id = %s;' % opponent_user_id)[0]
    opponent_user_name = sql_select('name', 'users', 'user_id = %s;' % opponent_user_id)[0]
    referral_user_id2 = sql_select('referral_user_id', 'users', 'user_id = %s;' % opponent_user_id)[0]
    if message in (u'\u270a', u'\u270b', u'\u270c'):
        sql.execute("UPDATE game SET %s_choose='%s' WHERE %s_id=%s;" % (opponent, system_dicts.hands[message], opponent, user_id))
        c.commit()

        if not other_opponent_choose:
            sql.execute("UPDATE users SET state='WAIT_RESULT' WHERE user_id = %s;" % user_id)
            c.commit()
        else:
            winner = compare(system_dicts.hands[message], other_opponent_choose)
            if winner == -1:
                bot.sendMessage(user_id, text=lang_dicts.draw_answer[lang] % (
                    user_name, message, opponent_user_name, system_dicts.hands_revert[other_opponent_choose]), parse_mode='markdown',
                                reply_markup=keyboard.play_keyboard)
                if opponent_user_id != BOT:
                    bot.sendMessage(opponent_user_id, text=lang_dicts.draw_answer[lang] % (
                        user_name, message, opponent_user_name, system_dicts.hands_revert[other_opponent_choose]), parse_mode='markdown',
                                    reply_markup=keyboard.play_keyboard)
                sql.execute("UPDATE users SET state='IN_GAME' WHERE user_id IN (%s, %s);" % (user_id, opponent_user_id))
            elif winner == 1:
                sql.execute("UPDATE users SET %s = (%s + %s), state='PLAY_AGAIN' WHERE user_id=%s;" % (
                    currency, currency, currency_lib.prize[currency], user_id))
                sql.execute("UPDATE users SET %s = (%s - %s), state='PLAY_AGAIN' WHERE user_id=%s;" % (
                    currency, currency, currency_lib.loss[currency], opponent_user_id))
                if referral_user_id is not None:
                    sql.execute("UPDATE users SET %s = (%s + %s) WHERE user_id=%s;" % (
                        currency, currency, currency_lib.referral_prize[currency], referral_user_id))
                c.commit()
                diamond, cash = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users', 'user_id = %s' % user_id)
                diamond2, cash2 = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users',
                                             'user_id = %s' % opponent_user_id)
                # отправка сообщений
                bot.sendMessage(user_id, text=lang_dicts.winner_answer[lang] % (
                    user_name, message, currency_lib.pot[currency], opponent_user_name, system_dicts.hands_revert[other_opponent_choose], diamond,
                    cash), parse_mode='markdown', reply_markup=keyboard.play_again_keyboard(lang))
                if opponent_user_id != BOT:
                    bot.sendMessage(opponent_user_id, text=lang_dicts.loser_answer[lang2] % (
                        opponent_user_name, system_dicts.hands_revert[other_opponent_choose], user_name, message, currency_lib.pot[currency],
                        diamond2,
                        cash2), parse_mode='markdown', reply_markup=keyboard.play_again_keyboard(lang2))
            else:
                sql.execute("UPDATE users SET %s = (%s - %s), state='PLAY_AGAIN' WHERE user_id=%s;" % (
                    currency, currency, currency_lib.loss[currency], user_id))
                sql.execute("UPDATE users SET %s = (%s + %s), state='PLAY_AGAIN' WHERE user_id=%s;" % (
                    currency, currency, currency_lib.prize[currency], opponent_user_id))
                c.commit()
                diamond, cash = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users', 'user_id = %s' % user_id)
                diamond2, cash2 = sql_select('diamond, %s' % lang_dicts.currency[lang], 'users',
                                             'user_id = %s' % opponent_user_id)
                bot.sendMessage(user_id, text=lang_dicts.loser_answer[lang] % (
                    user_name, message, opponent_user_name, system_dicts.hands_revert[other_opponent_choose], currency_lib.pot[currency], diamond,
                    cash), parse_mode='markdown', reply_markup=keyboard.play_again_keyboard(lang))
                if opponent_user_id != BOT:
                    if referral_user_id2 is not None:
                        sql.execute("UPDATE users SET %s = (%s + %s) WHERE user_id=%s;" % (
                            currency, currency, currency_lib.referral_prize[currency], referral_user_id2))
                    bot.sendMessage(opponent_user_id, text=lang_dicts.winner_answer[lang2] % (
                        opponent_user_name, system_dicts.hands_revert[other_opponent_choose], currency_lib.pot[currency], user_name, message,
                        diamond2,
                        cash2), parse_mode='markdown', reply_markup=keyboard.play_again_keyboard(lang2))
            sql.execute("UPDATE game SET opponent1_choose = null, opponent2_choose = null, start_time = null WHERE id = %s;" % game_id)
            c.commit()
    else:
        text = user_name + ': ' + message
        bot.sendMessage(user_id, text=text)
        if opponent_user_id != BOT:
            bot.sendMessage(opponent_user_id, text=text)


def wait_result(bot, update):
    message = update.message.text
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    game_id = sql_select('id', 'game', 'opponent1_id = %s' % user_id)[0]
    opponent = sql_select('opponent1_id', 'game', 'opponent1_id = %s' % user_id)[0]
    if not opponent:
        opponent2 = 'opponent1'
        game_id = sql_select('id', 'game', 'opponent2_id = %s' % user_id)[0]
    else:
        opponent2 = 'opponent2'
    opponent_user_id = sql_select('%s_id' % opponent2, 'game', 'id = %s' % game_id)[0]
    if message in (u'\u270a', u'\u270b', u'\u270c'):
        return 0
    else:
        text = user_name + ': ' + message
        bot.sendMessage(user_id, text=text)
        if opponent_user_id != BOT:
            bot.sendMessage(opponent_user_id, text=text)
