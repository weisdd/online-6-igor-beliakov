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
