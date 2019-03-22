# -*- coding: utf-8 -*-
import os
from sys import argv
import sqlite3
from tabulate import tabulate


def get_data(conn, args):
    try:
        if len(args) == 0:
            message = 'В таблице dhcp такие записи:'
            rows_active = conn.execute('SELECT * FROM dhcp WHERE active = 1')
            rows_inactive = conn.execute('SELECT * FROM dhcp WHERE active = 0')
        else:
            key, value = args
            message = f'Информация об устройствах с такими параметрами: {key} {value}'
            query_active = 'SELECT * FROM dhcp WHERE active = 1 AND {} = ?'.format(key)
            query_inactive = 'SELECT * FROM dhcp WHERE active = 0 AND {} = ?'.format(key)
            rows_active = conn.execute(query_active, (value,))
            rows_inactive = conn.execute(query_inactive, (value,))
        print(message)
        print('\nАктивные записи:\n')
        print(tabulate([row for row in rows_active]))
        rows_inactive_tabulate = [row for row in rows_inactive]
        if len(rows_inactive_tabulate) > 0:
            print('\nНеактивные записи:\n')
            print(tabulate(rows_inactive_tabulate))
    except sqlite3.IntegrityError as err:
        print(err)


def check_arguments(args):
    if len(args) not in [0, 2]:
        print('Скрипт поддерживает только два или ноль аргументов')
        return
    elif len(args) == 2:
        if args[0] not in ['mac', 'ip', 'vlan', 'interface', 'switch', 'active']:
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
