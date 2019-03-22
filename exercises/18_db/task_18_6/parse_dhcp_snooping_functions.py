# -*- coding: utf-8 -*-
import os
import sqlite3
import yaml
import re
from tabulate import tabulate


def create_db(name, schema):
    if os.path.exists(name):
        print('База данных существует')
    else:
        with open(schema, 'r', encoding='utf-8') as f:
            conn = sqlite3.connect(name)
            conn.executescript(f.read())
            conn.close()


def add_data_switches(db_file, filename):
    conn = sqlite3.connect(db_file)
    for file in filename:
        with open(file, 'r', encoding='utf-8') as f:
            switches = yaml.safe_load(f)
            rows = [(key, value) for key, value in switches['switches'].items()]
            for row in rows:
                try:
                    with conn:
                        query = 'INSERT INTO switches (hostname, location) values (?, ?)'
                        conn.execute(query, row)
                except sqlite3.IntegrityError as err:
                    print(f'При добавлении данных: {row} возникла ошибка {err}')
    conn.close()


def add_data(db_file, filename):
    conn = sqlite3.connect(db_file)
    # Удаляем старые записи
    with conn:
        query = "DELETE FROM dhcp WHERE last_active <= datetime('now', '-7 days')"
        conn.execute(query)
    rows = []
    for file in filename:
        with open(file, 'r', encoding='utf-8') as f:
            switch = file.replace('_dhcp_snooping.txt', '').replace('new_data/', '')
            for line in f:
                # mac, ip, vlan, interface
                match = re.search(r'(\S+)\s+(\S+)\s+\d+\s+\S+\s+(\d+)\s+(\S+)', line)
                if match:
                    # -> mac, ip, vlan, interface, switch
                    rows.append(list(match.groups()) + [switch])
            try:
                with conn:
                    query = 'UPDATE dhcp SET active = 0 WHERE switch = ?'
                    conn.execute(query, (switch,))
            except sqlite3.IntegrityError as err:
                print(f'При добавлении данных: {row} возникла ошибка {err}')

    # Добавляем данные в таблицу dhcp...')
    for row in rows:
        try:
            with conn:
                query = "INSERT OR REPLACE INTO dhcp (mac, ip, vlan, interface, switch, active, last_active) VALUES (?, ?, ?, ?, ?, 1, datetime('now'))"
                conn.execute(query, row)
        except sqlite3.IntegrityError as err:
            print(f'При добавлении данных: {row} возникла ошибка {err}')
    conn.close()


def get_data(db_file, key, value):
    conn = sqlite3.connect(db_file)
    try:
        query_active = 'SELECT * FROM dhcp WHERE active = 1 AND {} = ?'.format(key)
        query_inactive = 'SELECT * FROM dhcp WHERE active = 0 AND {} = ?'.format(key)
        rows_active = conn.execute(query_active, (value,))
        rows_inactive = conn.execute(query_inactive, (value,))
        print('\nАктивные записи:\n')
        print(tabulate([row for row in rows_active]))
        rows_inactive_tabulate = [row for row in rows_inactive]
        if len(rows_inactive_tabulate) > 0:
            print('\nНеактивные записи:\n')
            print(tabulate(rows_inactive_tabulate))
    except sqlite3.IntegrityError as err:
        print(err)
    conn.close()


def get_all_data(db_file):
    conn = sqlite3.connect(db_file)
    try:
        rows_active = conn.execute('SELECT * FROM dhcp WHERE active = 1')
        rows_inactive = conn.execute('SELECT * FROM dhcp WHERE active = 0')
        print('\nАктивные записи:\n')
        print(tabulate([row for row in rows_active]))
        rows_inactive_tabulate = [row for row in rows_inactive]
        if len(rows_inactive_tabulate) > 0:
            print('\nНеактивные записи:\n')
            print(tabulate(rows_inactive_tabulate))
    except sqlite3.IntegrityError as err:
        print(err)
    conn.close()
