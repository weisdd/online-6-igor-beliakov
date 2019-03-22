# -*- coding: utf-8 -*-
import os
from sys import argv
import sqlite3
from tabulate import tabulate


def get_data(conn, args):
    try:
        if len(args) == 0:
            message = 'В таблице dhcp такие записи:'
            rows = conn.execute('SELECT * FROM dhcp')
        else:
            key, value = args
            message = f'Информация об устройствах с такими параметрами: {key} {value}'
            query = 'SELECT * FROM dhcp WHERE {} = ?'.format(key)
            rows = conn.execute(query, (value,))
        print(message)
        print(tabulate([row for row in rows]))
    except sqlite3.IntegrityError as err:
        print(err)


def check_arguments(args):
    if len(args) not in [0, 2]:
        print('Скрипт поддерживает только два или ноль аргументов')
        return
    elif len(args) == 2:
        if args[0] not in ['mac', 'ip', 'vlan', 'interface', 'switch']:
            print('Данный параметр не поддерживается.\n'
                  'Допустимые значения параметров: mac, ip, vlan, interface, switch')
            return
        else:
            return True
    else:
        return True


def main():
    db_name = 'dhcp_snooping.db'
    if not check_arguments(argv[1:]):
        return
    if not os.path.exists(db_name):
        print(f'БД {db_name} не существует')
        return
    conn = sqlite3.connect(db_name)
    get_data(conn, argv[1:])


if __name__ == '__main__':
    main()

# Все отлично

# вариант решения

import sqlite3
import sys

from tabulate import tabulate


def get_data_by_key_value(db_name, key, value):
    keys = 'mac ip vlan interface switch'.split()
    if key not in keys:
        print('Данный параметр не поддерживается.')
        print('Допустимые значения параметров: {}'.format(', '.join(keys)))
        return
    connection = sqlite3.connect(db_filename)

    query = "select * from dhcp where {} = ?".format(key)
    result = connection.execute(query, (value,))

    print('\nИнформация об устройствах с такими параметрами:', key, value)
    print(tabulate(result))


def get_all_data(db_name):
    print('В таблице dhcp такие записи:')
    connection = sqlite3.connect(db_filename)
    print(tabulate(connection.execute('select * from dhcp')))


def parse_args(db_name, args):
    if len(args) == 0:
        get_all_data(db_filename)
    elif len(args) == 2:
        key, value = args
        get_data_by_key_value(db_filename, key, value)
    else:
        print('Пожалуйста, введите два или ноль аргументов')


if __name__ == '__main__':
    db_filename = 'dhcp_snooping.db'
    args = sys.argv[1:]
    parse_args(db_filename, args)
