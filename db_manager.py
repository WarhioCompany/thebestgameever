import sqlite3

path = "data/game.sqlite3"
con = sqlite3.connect(path)
cur = con.cursor()


def create_table():
    table = """ CREATE TABLE IF NOT EXISTS player_stats (
                                            score integer,
                                            money integer,
                                            night integer,
                                            speed_level integer,
                                            hp_level integer
                                        ); """

    cur.execute(table)


def reset_table():
    sql = 'DROP TABLE IF EXISTS player_stats;'
    cur.execute(sql)

    create_table()

    sql = '''INSERT INTO player_stats(score, money, night, speed_level, hp_level) VALUES(?,?,?,?,?) '''
    cur.execute(sql, (0, 0, 0, 1, 1))
    con.commit()


def get(name):
    return cur.execute(f'SELECT {name} FROM player_stats').fetchone()[0]


def get_night():
    return get('night')


def get_money():
    return get('money')


def get_score():
    return get('score')


def get_speed_level():
    return get('speed_level')


def get_hp_level():
    return get('hp_level')


def set_value(key, value):
    sql = f'''UPDATE player_stats SET {key} = ?'''
    cur.execute(sql, (value,))


def decrease_money(decrease_amount):
    money = get_money()
    set_value('money', money - decrease_amount)


def set_speed(value):
    set_value('speed_level', value)


def set_hp(value):
    set_value('hp_level', value)


def update_score_and_money(amount):
    money = get_money()
    score = get_score()
    sql = '''UPDATE player_stats SET money = ?, score = ?'''
    cur.execute(sql, (money + amount, score + amount))
