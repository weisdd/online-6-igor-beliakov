# -*- coding: utf-8 -*-
'''
Задание 22.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - шаблон TextFSM. Имя файла, в котором находится шаблон
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.
'''

import textfsm


def parse_output_to_dict(template, command_output):
    with open(template, 'r', encoding='utf-8') as f:
        fsm = textfsm.TextFSM(f)
        parsed_text = fsm.ParseText(command_output)
        keys = fsm.header
        result = [dict(zip(keys, value)) for value in parsed_text]
        return result


def main():
    with open('output/sh_ip_int_br.txt', 'r', encoding='utf-8') as f:
        command_output = f.read()
        print(parse_output_to_dict('templates/sh_ip_int_br.template', command_output))


if __name__ == '__main__':
    main()
