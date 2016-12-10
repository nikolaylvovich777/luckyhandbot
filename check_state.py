# -*- coding: utf-8 -*-
from admin.balance import BALANCE_ADMIN_CHAT, DOLLAR_ADD, ROUBLE_ADD, user_list, add_balance, admin_help, add_balance_part2, stop_add, add_balance_confirm, withdraw_notify
from admin.feedback import FEEDBACK_ADMIN_CHAT, new_message, feedback_answer, open_feedback, feedback_start_answer
from db_connector import sql_select
from game.handler import check_choose, wait_result
from handler import start, choose_lang, menu, feedback, opponent_not_found, search_opponent, play_again, money_input, old_game_cleaner, diamond_reload, get_gift


def message_checker(bot, update):
    old_game_cleaner(bot)
    diamond_reload(bot)
    chat_id = update.message.chat_id
    # reply_check = update.message.reply_to_message
    chat_state = sql_select('state', 'users', 'user_id = %s' % update.message.from_user.id)[0]
    if chat_id == FEEDBACK_ADMIN_CHAT:  # and reply_check is not None:
        feedback_answer(bot, update)
    elif chat_id == BALANCE_ADMIN_CHAT:
        if update.message.text == 'list':
            user_list(bot)
        elif update.message.text[:4] == 'add ':
            add_balance(bot, update)
        elif update.message.text == 'help':
            admin_help(bot)
        elif update.message.text == u'2500 \U0001f48e':
            add_balance_part2(bot, update, 2500, 'diamond')
        elif update.message.text in DOLLAR_ADD:
            add_balance_part2(bot, update, update.message.text[:-2], 'dollar')
        elif update.message.text in ROUBLE_ADD:
            add_balance_part2(bot, update, update.message.text[:-2], 'rouble')
        elif update.message.text in (u'\U0001F44E', u'Отмена'):
            stop_add(bot, update)
        elif update.message.text == u'\U0001F44D':
            add_balance_confirm(bot, update)
    elif (str(chat_id)[0]) != '-':
        if update.message.text[:6] == '/start':
            start(bot, update)
        elif update.message.text == '/support':
            open_feedback(bot, update)
        elif chat_state == 'CHOOSE_LANG':
            choose_lang(bot, update)
        elif chat_state == 'MENU':
            menu(bot, update)
        elif chat_state == 'FEEDBACK':
            feedback(bot, update)
        elif chat_state == 'NEW_FEEDBACK':
            new_message(bot, update)
        elif chat_state == 'SEARCHING':
            search_opponent(bot, update)
        elif chat_state == 'NOT_FOUND':
            opponent_not_found(bot, update)
        elif chat_state == 'IN_GAME':
            check_choose(bot, update)
        elif chat_state == 'WAIT_RESULT':
            wait_result(bot, update)
        elif chat_state == 'PLAY_AGAIN':
            play_again(bot, update)
        elif chat_state == 'MONEY_INPUT':
            money_input(bot, update)
        elif chat_state == 'WAIT_OPPONENT':
            play_again(bot, update)
        elif chat_state == 'GIFT':
            get_gift(bot, update)


def callback_checker(bot, update):
    chat_id = update.callback_query.message.chat_id
    if chat_id == FEEDBACK_ADMIN_CHAT:
        feedback_start_answer(bot, update)
    elif chat_id == BALANCE_ADMIN_CHAT:
        withdraw_notify(bot, update)
