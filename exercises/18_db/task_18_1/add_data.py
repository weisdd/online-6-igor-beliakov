# -*- coding: utf-8 -*-
import os
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
    files = glob.glob(dhcp_snooping_files)
    rows = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            switch = file.replace('_dhcp_snooping.txt', '')
            for line in f:
                # mac, ip, vlan, interface
                match = re.search(r'(\S+)\s+(\S+)\s+\d+\s+\S+\s+(\d+)\s+(\S+)', line)
                if match:
                    # -> mac, ip, vlan, interface, switch
                    rows.append(list(match.groups()) + [switch])
    print('Добавляю данные в таблицу dhcp...')
    for row in rows:
        try:
            with conn:
                query = 'INSERT INTO dhcp (mac, ip, vlan, interface, switch) VALUES (?, ?, ?, ?, ?)'
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
    conn.close()


if __name__ == '__main__':
    main()
