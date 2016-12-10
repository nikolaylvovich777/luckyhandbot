#  -*- coding: utf-8 -*-
from db_connector import sql, c
from lib import lang_dicts, keyboard


def user_reload_to_menu(bot, update):
    admin_user_id = update.message.from_user.id
    if admin_user_id == 60558942:
        sql.execute("SELECT user_id, lang FROM users WHERE state IN ('IN_GAME', 'WAIT_RESULT', 'PLAY_AGAIN') "
                    "AND user_id != 0 "
                    "AND user_id != 137834952 "
                    "AND user_id != 280423995 "
                    "AND user_id != 299535357 "
                    "AND user_id != 294657956 "
                    "AND user_id != 88303804 "
                    "AND user_id != 153065507 "
                    "AND user_id != 258302635 "
                    "AND user_id != 121238604 "
                    "AND user_id != 226357409 "
                    ";"
                    )
        rows = sql.fetchall()
        for row in rows:
            user_id = row[0]
            lang = row[1]
            bot.sendMessage(user_id, text=lang_dicts.menu_back_answer[lang], reply_markup=keyboard.menu_keyboard(lang))
            sql.execute("UPDATE users SET state='MENU' WHERE user_id = %s;" % user_id)
            c.commit()
        return
    else:
        print('нельзя')
