# -*- coding: utf-8 -*-
'''
Задание 21.2

На основе конфигурации config_r1.txt, создать шаблоны:
* templates/cisco_base.txt - в нем должны быть все строки, кроме настройки alias и event manager. Имя хоста должно быть переменной hostname
* templates/alias.txt - в этот шаблон перенести все alias
* templates/eem_int_desc.txt - в этом шаблоне должен быть event manager applet

В шаблонах templates/alias.txt и templates/eem_int_desc.txt переменных нет.

Создать шаблон templates/cisco_router_base.txt. В шаблон templates/cisco_router_base.txt должно быть включено содержимое шаблонов:
* templates/cisco_base.txt
* templates/alias.txt
* templates/eem_int_desc.txt

При этом, нельзя копировать текст шаблонов.


Проверьте шаблон templates/cisco_router_base.txt, с помощью
функции generate_config из задания 21.1. Не копируйте код функции generate_config.

В качестве данных, используйте информацию из файла data_files/router_info.yml

'''

from task_21_1 import generate_config
import yaml


def main():
    with open('data_files/router_info.yml', 'r', encoding='utf-8') as f:
        data_dict = yaml.safe_load(f)
        print(generate_config('templates/cisco_router_base.txt', data_dict))


if __name__ == '__main__':
    main()
