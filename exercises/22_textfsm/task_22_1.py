# -*- coding: utf-8 -*-
'''
Задание 22.1

Создать функцию parse_command_output. Параметры функции:
* template - шаблон TextFSM. Имя файла, в котором находится шаблон
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список:
* первый элемент - это список с названиями столбцов
* остальные элементы это списки, в котором находятся результаты обработки вывода

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.

'''

import textfsm


def parse_command_output(template, command_output):
    with open(template, 'r', encoding='utf-8') as f:
        fsm = textfsm.TextFSM(f)
        result = fsm.ParseText(command_output)
        result.insert(0, fsm.header)
        return result


def main():
    with open('output/sh_ip_int_br.txt', 'r', encoding='utf-8') as f:
        command_output = f.read()
        print(parse_command_output('templates/sh_ip_int_br.template', command_output))


if __name__ == '__main__':
    main()

# Все отлично

# вариант решения
def parse_command_output(template, command_output):
    with open(template) as tmpl:
        parser = textfsm.TextFSM(tmpl)
        header = parser.header
        result = parser.ParseText(command_output)
    return [header] + result


if __name__ == '__main__':
    with open("output/sh_ip_int_br.txt") as show:
        output = show.read()
    result = parse_command_output("templates/sh_ip_int_br.template", output)
    print(result)
