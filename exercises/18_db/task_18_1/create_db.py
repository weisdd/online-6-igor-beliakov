# -*- coding: utf-8 -*-
import os
import sqlite3


def create_db(db_name='dhcp_snooping.db'):
    if os.path.exists(db_name):
        print('База данных существует')
    else:
        print('Создаю базу данных...')
        with open('dhcp_snooping_schema.sql', 'r', encoding='utf-8') as f:
            conn = sqlite3.connect(db_name)
            conn.executescript(f.read())
            conn.close()


def main():
    create_db()


if __name__ == '__main__':
    main()
