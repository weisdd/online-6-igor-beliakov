# -*- coding: utf-8 -*-
import os
from datetime import timedelta, datetime
import glob
import re
import yaml
import sqlite3


def add_data_switches(conn, switches_yaml='switches.yml'):
    with open(switches_yaml, 'r', encoding='utf-8') as f:
        print('Добавляю данные в таблицу switches...')
        switches = yaml.safe_load(f)
        rows = [(key, value) for key, value in switches['switches'].items()]
        for row in rows:
            try:
                with conn:
                    query = 'INSERT INTO switches (hostname, location) values (?, ?)'
                    conn.execute(query, row)
            except sqlite3.IntegrityError as err:
                print(f'При добавлении данных: {row} возникла ошибка {err}')


def add_data_snooping(conn, dhcp_snooping_files='*_dhcp_snooping.txt'):
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    print('Удаляю старые записи...')
    with conn:
        query = 'DELETE FROM dhcp WHERE last_active <= ?'
        conn.execute(query, (week_ago,))
        # То же самое средствами SQL:
        # query = "DELETE FROM dhcp WHERE last_active <= datetime('now', '-7 days')"
        # conn.execute(query)
    files = glob.glob(dhcp_snooping_files)
    rows = []
    for file in files:
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

    print('Добавляю данные в таблицу dhcp...')
    for row in rows:
        try:
            with conn:
                query = "INSERT OR REPLACE INTO dhcp (mac, ip, vlan, interface, switch, active, last_active) VALUES (?, ?, ?, ?, ?, 1, datetime('now'))"
                conn.execute(query, row)
        except sqlite3.IntegrityError as err:
            print(f'При добавлении данных: {row} возникла ошибка {err}')


def main():
    db_name = 'dhcp_snooping.db'
    switches_yaml = 'switches.yml'
    dhcp_snooping_files = '*_dhcp_snooping.txt'
    if not os.path.exists(db_name):
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return None
    conn = sqlite3.connect(db_name)
    add_data_switches(conn, switches_yaml=switches_yaml)
    add_data_snooping(conn, dhcp_snooping_files=dhcp_snooping_files)
    dhcp_snooping_files = 'new_data/*_dhcp_snooping.txt'
    add_data_snooping(conn, dhcp_snooping_files=dhcp_snooping_files)
    conn.close()


if __name__ == '__main__':
    main()

# Все отлично

# вариант решения

import glob
import sqlite3
import re
import os
from pprint import pprint
from datetime import timedelta, datetime

import yaml


def parse_dhcp_snoop(filename):
    regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
    hostname = re.search('(\w+)_dhcp_snooping.txt', filename).group(1)
    with open(filename) as f:
        result = [match.groups()+(hostname,) for match in regex.finditer(f.read())]
    return result


def add_data(connection, query, data):
    for row in data:
        try:
            with connection:
                connection.execute(query, row)
        except sqlite3.IntegrityError as err:
            print('При добавлении данных:', row, 'Возникла ошибка:', err)


def add_sw_data(db_name, sw_data_file):
    connection = sqlite3.connect(db_name)
    query_switches = 'insert into switches values (?,?)'
    with open(sw_data_file) as f:
        switches = yaml.load(f)
        sw_data = list(switches['switches'].items())
        add_data(connection, query_switches, sw_data)
    connection.close()


def remove_old_records(conn):
    now = datetime.today().replace(microsecond=0)
    week_ago = str(now - timedelta(days = 7))
    query = "delete from dhcp where last_active < ?"
    conn.execute(query, (week_ago,))
    conn.commit()


def add_dhcp_data(db_name, data_files):
    connection = sqlite3.connect(db_name)
    remove_old_records(connection)
    connection.execute('update dhcp set active = 0')
    query = "replace into dhcp values (?, ?, ?, ?, ?, ?, datetime('now'))"
    for filename in data_files:
        result = parse_dhcp_snoop(filename)
        updated_result = [row+(1,) for row in result]
        add_data(connection, query, updated_result)
    connection.close()


if __name__ == '__main__':

    db_filename = 'dhcp_snooping.db'
    #dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')
    dhcp_snoop_files = glob.glob('new_data/sw*_dhcp_snooping.txt')
    print(dhcp_snoop_files)

    db_exists = os.path.exists(db_filename)
    if db_exists:
        #add_sw_data(db_filename, 'switches.yml')
        add_dhcp_data(db_filename, dhcp_snoop_files)
    else:
        print('База данных не существует. Для добавления данных, ее надо создать')


