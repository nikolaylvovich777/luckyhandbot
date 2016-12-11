from db_connector import sql, c

# sql.execute('CREATE TABLE users '
#             '( '
#             'id serial NOT NULL, '
#             'user_id integer NOT NULL, '
#             'name text COLLATE pg_catalog.'default' NOT NULL, '
#             'state text COLLATE pg_catalog.'default', '
#             'lang text COLLATE pg_catalog.'default', '
#             'diamond integer, '
#             'dollar real, '
#             'rouble real, '
#             'last_game_time text COLLATE pg_catalog.'default', '
#             'last_game_currency text COLLATE pg_catalog.'default', '
#             'last_game_id integer, '
#             'diamond_request_time text COLLATE pg_catalog.'default', '
#             'ik_num integer NOT NULL DEFAULT 0, '
#             'referral_user_id integer,'
#             ' CONSTRAINT user_pkey PRIMARY KEY (id) '
#             ')')
# c.commit()
sql.execute(
    'INSERT"INTO users (id, user_id, name, state,lang, diamond, dollar, rouble, last_game_time, last_game_currency, last_game_id, diamond_request_time, ik_num, referral_user_id) VALUES "
    "(1, 60558942, '@risun', 'MENU', 'RUS', 300,2.94,20.2, '2016-10-15 04:08:10', 'diamond', 211, NULL, 8, NULL), "
    "(2, 0, 'BOT', 'PLAY_AGAIN', 'ENG', 997779,999999.0,999997.0, NULL, NULL, 218, NULL, 0, NULL), "
    "(5, 267178646, 'Jeremy', 'MENU', 'GER', 1007, 0.0, 0.0, '2016-10-12 12:25:20', 'diamond', 136, NULL, 0,267178646), "
    "(6, 252728429, 'Carina', 'MENU', 'GER', 130, 0.0, 0.0, '2016-10-07 22:33:40', 'diamond', 39, NULL, 0,267178646), "
    "(7, 198782816, '@Omar_alEtish', 'MENU', 'ENG', 250, 0.0, 0.0, '2016-10-07 21:23:24', 'diamond', 42, NULL, 1, NULL), "
    "(8, 12886716, '@dasein1337', 'MENU', 'RUS', 190, 0.0, 0.0, '2016-10-09 19:37:11', 'diamond', 56, NULL, 2, NULL), "
    "(9, 216718777, '@arcycanlas', 'MENU', 'ENG', 600, 0.0, 0.0, '2016-10-08 09:41:08', 'diamond', 46, NULL, 0, NULL), "
    "(10, 219053868, '@CengCrdva', 'MENU', 'ENG', 300, 0.0, 0.0, '2016-10-12 15:15:53', 'diamond', 148, NULL, 0,216718777), "
    "(11, 242321968, 'rehan', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(12, 213223845, '@nyledge', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0,216718777), "
    "(13, 154420234, 'Rochelle Salaysay', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0,216718777), "
    "(14, 246611194, '@deadevita', 'MENU', 'ENG', 460, 0.0, 0.0, '2016-10-09 06:17:57', 'diamond', 47, NULL, 0, NULL), "
    "(15, 281754345, 'Anriz Carlos', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(16, 245770190, 'Mario Rodriguez', 'MENU', 'ENG', 140, 0.0, 0.0, '2016-10-09 09:06:52', 'diamond', 48, NULL, 0, NULL), "
    "(17, 46693147, '@REBECCAKANG77', 'MENU', 'ENG', 250, 0.0, 0.0, '2016-10-12 16:31:40', 'diamond', 153, NULL, 0, NULL), "
    "(18, 137834952, '@thekidwhonevergrewup', 'PLAY_AGAIN', 'ENG', 250, 0.0, 0.0, '2016-10-09 12:28:43', 'diamond', 49, NULL, 0, NULL), "
    "(19, 268212639, '@evelina1', 'MENU', 'RUS', 480, 0.0, 0.0, '2016-10-09 12:29:43', 'diamond', 50, NULL, 0, NULL), "
    "(20, 253494834, '@Angel1229', 'MONEY_INPUT', 'RUS', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 1,268212639), "
    "(21, 231683682, '@Tabithaaa', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(22, 75392978, 'Vaceslav Kreller', 'MENU', 'GER', 300, 0.0, 0.0, '2016-10-09 13:49:20', 'diamond', 51, NULL, 0,171585224), "
    "(23, 261999345, '@AchooDa', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(24, 217072238, '@Krishna_Senpai', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(25, 190957563, '@chris_monstah', 'MENU', 'GER', 300, 0.0, 0.0, '2016-10-09 14:40:14', 'diamond', 51, NULL, 0,171585224), "
    "(26, 104690839, 'Christopher', 'MENU', 'GER', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0,190957563), "
    "(27, 294657956, '@yolandahae', 'PLAY_AGAIN', 'ENG', 250, 0.0, 0.0, '2016-10-09 17:03:23', 'diamond', 54, NULL, 3, NULL), "
    "(28, 227130289, 'Perez', 'MENU', 'ITA', 340, 0.0, 0.0, '2016-10-09 16:05:50', 'diamond', 52, NULL, 0, NULL), "
    "(29, 280423995, 'Rocky Marciano Hendico', 'WAIT_RESULT', 'ENG', 300, 0.0, 0.0, '2016-10-09 16:51:06', 'diamond', 53, NULL, 0, NULL), "
    "(30, 222954365, '@lusyanabubu', 'MENU', 'ENG', 250, 0.0, 0.0, '2016-10-12 17:11:07', 'diamond', 158, NULL, 0,171585224), "
    "(31, 11597646, '@mzzntn95', 'MENU', 'ITA', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(32, 273828550, '@mikhaelss', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(33, 110560983, '@BrhmZtkn', 'MENU', 'ENG', 300, 0.0, 0.0, '2016-10-09 23:41:50', 'diamond', NULL, NULL, 0,171585224), "
    "(34, 245600456, 'Ron', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(35, 283393175, '@marchelcello', 'MENU', 'ENG', 640, 0.0, 0.0, '2016-10-10 08:13:28', 'diamond', 63, NULL, 0, NULL), "
    "(36, 299535357, '@Indriyanahsaputri', 'PLAY_AGAIN', 'ENG', 250, 0.0, 0.0, '2016-10-10 08:13:47', 'diamond', 62, NULL, 0,283393175), "
    "(37, 296944867, '@muthiathaya', 'MONEY_INPUT', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 1, NULL), "
    "(38, 163250827, 'Jayden Tan', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(39, 281460130, '@deatyoni', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(40, 83109589, '@plohoidurdom', 'MENU', 'RUS', 1130, 0.0, 0.0, '2016-10-13 05:44:28', 'diamond', 174, NULL, 0, NULL), "
    "(41, 287623978, 'Tirtadwipa Manunggal', 'MENU', 'ENG', 140, 0.0, 0.0, '2016-10-10 16:07:56', 'diamond', 75, NULL, 1, NULL), "
    "(42, 250054848, 'Vania Sarwoko', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(43, 270347046, 'San J', 'MENU', 'ENG', 220, 0.0, 0.0, '2016-10-10 15:42:46', 'diamond', 82, NULL, 0, NULL), "
    "(44, 223352315, 'Adi San', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(45, 250609605, 'Aziz M Sulthon', 'MENU', 'ENG', 370, 0.0, 0.0, '2016-10-10 16:51:24', 'diamond', 85, NULL, 0, NULL), "
    "(46, 228061358, '@diditodidit', 'MENU', 'ENG', 240, 0.0, 0.0, '2016-10-10 16:53:08', 'diamond', 86, NULL, 0, NULL), "
    "(47, 138967689, 'Alessandro Pieroni', 'MENU', 'ITA', 290, 0.0, 0.0, '2016-10-10 17:09:10', 'diamond', 87, NULL, 0, NULL), "
    "(48, 88303804, 'Tan Wen xuan', 'IN_GAME', 'ENG', 600, 0.0, 0.0, '2016-10-10 18:12:02', 'diamond', 88, NULL, 0, NULL), "
    "(49, 153065507, '@randomfriend', 'WAIT_RESULT', 'ENG', 300, 0.0, 0.0, '2016-10-10 18:12:07', 'diamond', 88, NULL, 0,88303804), "
    "(50, 209684955, 'Angel Debon', 'MENU', 'ESP', 340, 0.0, 0.0, '2016-10-10 18:24:06', 'diamond', 89, NULL, 0, NULL), "
    "(51, 183274331, '@Magnodusk', 'MENU', 'ESP', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(52, 255632250, 'Kondrat', 'MONEY_INPUT', 'RUS', 250, 0.0, 0.0, '2016-10-10 20:54:13', 'diamond', 90, NULL, 0, NULL), "
    "(53, 143750240, '@Astraeus42', 'MENU', 'GER', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(54, 18727661, '@Fenta8', 'MENU', 'ESP', 640, 0.0, 0.0, '2016-10-10 23:24:42', 'diamond', 90, NULL, 0,18727661), "
    "(55, 232089943, '@mantanmu', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(56, 260515679, 'Yosephani Amy', 'MENU', 'ENG', 340, 0.0, 0.0, '2016-10-11 08:03:05', 'diamond', 110, NULL, 0, NULL), "
    "(57, 269794517, 'BastiГЎn Medina GГіmez', 'MENU', 'ESP', 330, 0.0, 0.0, '2016-10-11 01:15:21', 'diamond', 92, NULL, 1, NULL), "
    "(58, 169813987, 'Ben Lee', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(59, 268069118, 'Melissa Tan', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(60, 259144381, '@Denttsalman7', 'MENU', 'ENG', 290, 0.0, 0.0, '2016-10-13 11:45:45', 'diamond', 190, NULL, 0, NULL), "
    "(61, 195038057, 'Max Brain', 'MONEY_INPUT', 'RUS', 400, 0.0, 0.0, '2016-10-15 10:31:14', 'diamond', 215, NULL, 1, NULL), "
    "(62, 221500686, '@BavithiraPriya', 'MENU', 'ENG', 230, 0.0, 0.0, '2016-10-11 05:04:59', 'diamond', 96, NULL, 0, NULL), "
    "(63, 172757451, 'РРІР°РЅ РРІР°РЅРѕРІ', 'MENU', 'RUS', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0,171585224), "
    "(64, 239614128, 'Adellia Syafania', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(65, 292653795, 'Eisen Lim', 'MENU', 'ENG', 200, 0.0, 0.0, '2016-10-11 09:43:14', 'diamond', 104, NULL, 0, NULL), "
    "(66, 64633394, 'Behzad Samadi', 'MENU', 'ENG', 250, 0.0, 0.0, '2016-10-11 10:29:10', 'diamond', 106, NULL, 0, NULL), "
    "(67, 109610704, 'Munikin', 'MENU', 'RUS', 200, 0.0, 0.0, '2016-10-11 10:44:45', 'diamond', 108, NULL, 0, NULL), "
    "(68, 152273619, '@xhuishi', 'MENU', 'ENG', 380, 0.0, 0.0, '2016-10-11 09:44:52', 'diamond', 113, NULL, 0, NULL), "
    "(69, 296866581, '@devito_al', 'CHOOSE_LANG', 'ENG', 300, 0.0, 0.0, '2016-10-11 11:09:07', 'diamond', NULL, NULL, 0, NULL), "
    "(70, 197824517, 'еҐізҐће–µ', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(71, 282564933, '@Constance_19', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(72, 295097925, 'Valentino Herdian', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(73, 295856450, '@alberttony10', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(74, 249084834, 'Hartiono', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(75, 244393395, '@whdftr', 'MENU', 'ENG', 300, 0.0, 0.0, '2016-10-12 17:39:51', 'diamond', NULL, NULL, 0, NULL), "
    "(76, 261676485, 'Bertha', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(77, 121238604, 'Oscar M', 'PLAY_AGAIN', 'ESP', 250, 0.0, 0.0, '2016-10-11 16:22:20', 'diamond', 118, NULL, 0, NULL), "
    "(78, 243909316, '@Beasaw', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(79, 240154824, '@ViJe03', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(80, 273931387, 'DarГ­o Vargas', 'MENU', 'ESP', 170, 0.0, 0.0, '2016-10-11 22:16:34', 'diamond', 126, NULL, 0, NULL), "
    "(81, 227510490, '@Leviackerman104th', 'MENU', 'ENG', 634, 0.0, 0.0, '2016-10-12 01:45:32', 'diamond', 128, NULL, 0, NULL), "
    "(82, 280956165, 'eduard ubina', 'PLAY_AGAIN', 'ENG', 410, 0.0, 0.0, '2016-10-13 05:08:38', 'diamond', 173, NULL, 0,227510490), "
    "(83, 258302635, 'Amirali Khtb', 'IN_GAME', 'UAE', 300, 0.0, 0.0, '2016-10-12 12:03:09', 'diamond', 136, NULL, 0, NULL), "
    "(84, 136156024, '@Riefz', 'MENU', 'ENG', 200, 0.0, 0.0, '2016-10-13 17:56:11', 'diamond', 196, NULL, 0, NULL), "
    "(85, 230731306, '@Jeniiiiiiiii', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(86, 37279367, '@nizam23', 'MONEY_INPUT', 'ENG', 320, 0.0, 0.0, '2016-10-12 22:04:47', 'diamond', 170, NULL, 2, NULL), "
    "(87, 226357409, '@Grant999', 'IN_GAME', 'ENG', 300, 0.0, 0.0, '2016-10-12 15:00:45', 'diamond', 147, NULL, 0, NULL), "
    "(88, 279398100, '@Ja844', 'MENU', 'ENG', 550, 0.0, 0.0, '2016-10-12 17:53:18', 'diamond', 162, NULL, 1, NULL), "
    "(89, 273729735, '@Il_nova', 'MENU', 'ITA', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(90, 257594374, '@Putrimaylinda', 'MENU', 'ENG', 250, 0.0, 0.0, '2016-10-12 15:19:47', 'diamond', 164, NULL, 2,279398100), "
    "(91, 274026227, 'unggul nugratama', 'MENU', 'ENG', 340, 0.0, 0.0, '2016-10-12 18:04:06', 'diamond', 163, NULL, 0, NULL), "
    "(92, 195762888, 'Wout Van Dyck', 'IN_GAME', 'ENG', 500, 0.0, 0.0, '2016-10-12 19:34:11', 'diamond', 169, NULL, 0, NULL), "
    "(93, 144017608, 'Raghad', 'WAIT_RESULT', 'ENG', 340, 0.0, 0.0, '2016-10-12 19:43:41', 'diamond', 169, NULL, 0,195762888), "
    "(94, 261061256, '@Tesla2Trojan', 'MENU', 'ENG', 340, 0.0, 0.0, '2016-10-13 05:07:41', 'diamond', 172, NULL, 0, NULL), "
    "(95, 115206062, '@Kaa_taak', 'CHOOSE_LANG', NULL, 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(96, 231207114, 'Lerissa Aulia', 'MENU', 'ENG', 250, 0.0, 0.0, '2016-10-13 07:24:13', 'diamond', 176, NULL, 0, NULL), "
    "(97, 296985493, 'Pumpkin Ed Reloaded', 'MENU', 'GER', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(98, 96805615, '@ahmadalfian', 'MENU', 'ENG', 230, 0.0, 0.0, '2016-10-13 10:49:10', 'diamond', 187, NULL, 0, NULL), "
    "(99, 244501607, '@fany_anastasia', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(100, 277641961, 'Azmi Fauzan', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(101, 133143197, '@Vondr19', 'MENU', 'ENG', 180, 0.0, 0.0, '2016-10-13 12:29:19', 'diamond', 192, NULL, 0, NULL), "
    "(102, 149954813, '@agengpramesthi', 'PLAY_AGAIN', 'ENG', 360, 0.0, 0.0, '2016-10-14 16:21:58', 'diamond', 195, NULL, 0, NULL), "
    "(103, 26546316, 'Wai Lee', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(104, 157837869, '@miradiyas', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(105, 252997918, '@LutfiAnsyari', 'MENU', 'ENG', 490, 0.0, 0.0, '2016-10-14 06:43:09', 'diamond', 199, NULL, 1, NULL), "
    "(106, 289206814, 'Aurim', 'MENU', 'ENG', 300, 0.0, 0.0, '2016-10-14 04:22:56', 'diamond', NULL, NULL, 0, NULL), "
    "(107, 277523623, 'Ignatius Ivan Prasetyo', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0,171585224), "
    "(108, 156128288, '@JEREMXLOO', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(109, 247647587, 'Suwandi Liu', 'CHOOSE_LANG', NULL, 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(110, 278953372, '@Visroll_xx', 'MONEY_INPUT', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(111, 207449243, '@APPLEPEN69', 'MENU', 'ENG', 300, 0.0, 0.0, '2016-10-14 14:12:57', 'diamond', NULL, NULL, 0, NULL), "
    "(112, 231030977, 'Sky Chua', 'MENU', 'ENG', 300, 0.0, 0.0, NULL, NULL, NULL, NULL, 0, NULL), "
    "(113, 209263685, '@nurvan', 'MENU', 'ENG', 340, 0.0, 0.0, '2016-10-14 16:10:27', 'diamond', 206, NULL, 0, NULL), "
    "(114, 134136799, '@LeanNst', 'MONEY_INPUT', 'ENG', 500, 0.0, 0.0, '2016-10-14 19:03:59', 'diamond', 207, NULL, 0, NULL), "
    "(115, 126367249, '@Vanessasmy', 'PLAY_AGAIN', 'ENG', 917, 0.0, 0.0, '2016-10-15 11:41:12', 'diamond', 216, NULL, 0,171585224), "
    "(116, 258379489, '@Nakrishn', 'MENU', 'ENG', 200, 0.0, 0.0, '2016-10-14 19:04:21', 'diamond', 208, NULL, 0,134136799), "
    "(117, 146948146, '@amandyness', 'GIFT', 'ENG', 30, 0.0, 0.0, '2016-10-14 19:07:26', 'diamond', 209, NULL, 1,126367249), "
    "(118,  50017751, '@Snakehunter', 'PLAY_AGAIN', 'GER', 250, 0.0, 0.0, '2016-10-15 09:57:30', 'diamond', 213, NULL, 0, NULL), "
    "(119, 286458671, '@Adityayuan', 'MENU', 'ENG', 340, 0.0, 0.0, '2016-10-15 10:14:10', 'diamond', 213, NULL, 0,262154702), "
    "(120, 208628344, '@JohnnyElColombiano', 'MONEY_INPUT', 'ESP', 0, 0.0, 0.0, '2016-10-15 13:25:26', 'diamond', 218, '2016-10-15 13:25:29', 1, NULL);"
    )
print('users done!')
sql.execute('CREATE TABLE game '
            '( '
            'id serial NOT NULL, '
            'opponent1_id integer, '
            'opponent2_id integer, '
            'opponent1_choose text COLLATE pg_catalog.'default', '
            'opponent2_choose text COLLATE pg_catalog.'default', '
            'start_time text COLLATE pg_catalog.'default', '
            'CONSTRAINT game_pkey PRIMARY KEY (id) '
            ')')
c.commit()
print('game done!')
sql.execute('CREATE TABLE add_balance_requests '
            '('
            'id serial NOT NULL, '
            'admin_user_id integer NOT NULL, '
            'user_id integer NOT NULL, '
            'sum real, '
            'currency text COLLATE pg_catalog.'default', '
            'date text COLLATE pg_catalog.'default', '
            'done integer NOT NULL DEFAULT 0, '
            'CONSTRAINT add_balance_requests_pkey PRIMARY KEY (id) '
            ')')
c.commit()
print('add_balance_requests done!')
sql.execute('CREATE TABLE feedback'
            '('
            'id serial NOT NULL, '
            'feedback_user_id bigint NOT NULL, '
            'date text COLLATE pg_catalog.'default' NOT NULL, '
            'text text COLLATE pg_catalog.'default', '
            'author bigint NOT NULL, '
            'author_name text COLLATE pg_catalog.'default' NOT NULL, '
            'message_id bigint, '
            'query_id bigint, '
            'CONSTRAINT feedback_pkey PRIMARY KEY (id) '
            ')')
c.commit()
print('feedback done!')
print('db_create.py successfully executed!')
