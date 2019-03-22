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

# Все отлично

# вариант решения

import os
import sqlite3


# обрати внимание на параметры функции
# это те файлы от которых она зависит
def create_db(db_name, schema):
    db_exists = os.path.exists(db_name)
    if db_exists:
        print('База данных существует')
        return
    print('Создаю базу данных...')
    with open(schema, encoding='utf-8') as f:
        schema_f = f.read()
        connection = sqlite3.connect(db_name)
        connection.executescript(schema_f)
        connection.close()


if __name__ == "__main__":
    db_filename = 'dhcp_snooping.db'
    schema_filename = 'dhcp_snooping_schema.sql'
    create_db(db_filename, schema_filename)
