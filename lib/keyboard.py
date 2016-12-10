# -*- coding: utf-8 -*-
from lib import lang_dicts
from telegram import KeyboardButton, ReplyKeyboardMarkup, Emoji


def menu_keyboard(lang):
    return {'resize_keyboard': True, 'one_time_keyboard': False, 'keyboard':
        [[{'text': lang_dicts.play_di_button[lang]}, {'text': lang_dicts.play_cash_button[lang]}],
         [{'text': lang_dicts.money_input_button[lang]}, {'text': lang_dicts.feedback_button[lang]}],
         [{'text': lang_dicts.invite_button[lang]}, {'text': lang_dicts.help_button[lang]}],
         [{'text': lang_dicts.rate_button[lang]}]]}


def lang_keyboard():
    custom_keyboard = [
        [KeyboardButton(lang_dicts.lang_answer['ENG']),
         KeyboardButton(lang_dicts.lang_answer['RUS']),
         KeyboardButton(lang_dicts.lang_answer['ESP'])],
        [KeyboardButton(lang_dicts.lang_answer['GER']),
         KeyboardButton(lang_dicts.lang_answer['ITA']),
         KeyboardButton(lang_dicts.lang_answer['FRA'])],
        [KeyboardButton(lang_dicts.lang_answer['POL']),
         KeyboardButton(lang_dicts.lang_answer['UAE']),
         KeyboardButton(lang_dicts.lang_answer['UZB'])]]
    return ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)


def feedback_keyboard(lang):
    custom_keyboard = [
        [KeyboardButton(lang_dicts.add_feedback_button[lang])],
        [KeyboardButton(lang_dicts.menu_back_button[lang])]]
    return ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)

hide_keyboard = {'hide_keyboard': True}


def pre_play_keyboard(lang):
    custom_keyboard = [
        [KeyboardButton(lang_dicts.keep_wait_button[lang]),
         KeyboardButton(lang_dicts.play_with_bot_button[lang])],
        [KeyboardButton(lang_dicts.discard_game_button[lang]),
         KeyboardButton(lang_dicts.invite_button[lang])]]
    return ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)


play_keyboard = {'resize_keyboard': True, 'one_time_keyboard': False, 'keyboard':
        [[{'text': Emoji.RAISED_FIST}, {'text': Emoji.RAISED_HAND},
         {'text': Emoji.VICTORY_HAND}]]}


def play_again_keyboard(lang):
    custom_keyboard = [[KeyboardButton(lang_dicts.play_again_button[lang])],
                       [KeyboardButton(lang_dicts.exit_game_button[lang])]]
    return ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)


def money_input_keyboard(lang):
    # noinspection PyTypeChecker
    custom_keyboard = [
        [KeyboardButton(lang_dicts.dollar_1_button[lang]),
         KeyboardButton(lang_dicts.dollar_2_button[lang]),
         KeyboardButton(lang_dicts.dollar_5_button[lang])],
        [KeyboardButton(lang_dicts.dollar_8_button[lang]),
         KeyboardButton(lang_dicts.dollar_10_button[lang]),
         KeyboardButton(lang_dicts.dollar_15_button[lang])],
        [KeyboardButton(u'2500 \U0001f48e')],
        [KeyboardButton(lang_dicts.withdraw_button[lang]),
         KeyboardButton(lang_dicts.menu_back_button[lang])]]
    return ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=False)

add_balance_keyboard = {'resize_keyboard': True, 'one_time_keyboard': True, 'keyboard':
        [[{'text': lang_dicts.dollar_1_button['ENG']}, {'text': lang_dicts.dollar_2_button['ENG']}, {'text': lang_dicts.dollar_5_button['ENG']}],
         [{'text': lang_dicts.dollar_8_button['ENG']}, {'text': lang_dicts.dollar_10_button['ENG']}, {'text': lang_dicts.dollar_15_button['ENG']}],
         [{'text': lang_dicts.dollar_1_button['RUS']}, {'text': lang_dicts.dollar_2_button['RUS']}, {'text': lang_dicts.dollar_5_button['RUS']}],
         [{'text': lang_dicts.dollar_8_button['RUS']}, {'text': lang_dicts.dollar_10_button['RUS']}, {'text': lang_dicts.dollar_15_button['RUS']}],
         [{'text': u'2500 \U0001f48e'}], [{'text': u'Отмена'}]]}

add_balance_confirm_keyboard = {'resize_keyboard': True, 'one_time_keyboard': True, 'keyboard':
        [[{'text': u'\U0001F44D'}, {'text': u'\U0001F44E'}]]}

MONEY_BUTTONS = (u'2500 \U0001f48e',
                 u'1 \U0001f4b2', u'2 \U0001f4b2', u'5 \U0001f4b2', u'8 \U0001f4b2', u'10 \U0001f4b2', u'15 \U0001f4b2',
                 u'30 ₽', u'50 ₽', u'100 ₽', u'200 ₽', u'500 ₽', u'1000 ₽')
