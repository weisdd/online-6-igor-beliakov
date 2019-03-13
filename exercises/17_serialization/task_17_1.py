# -*- coding: utf-8 -*-
'''
Задание 17.1

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла, в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Скрипт должен:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в файл routers_inventory.csv

В файле routers_inventory.csv должны быть такие столбцы:
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
'''

import glob
import re
import csv


def parse_sh_version(shver):
    # It'll return a tuple only if it can find
    # all elements (ios, image, uptime)
    regex = (r'Version (\S+),',
             r'image file is "(.+)"',
             r'uptime is (.+)\n',
             )
    result = []
    for pattern in regex:
        match = re.search(pattern, shver)
        if match:
            result.append(match.group(1))
        else:
            return
    return tuple(result)


def write_inventory_to_csv(data_filenames, csv_filename):
    headers = ['hostname', 'ios', 'image', 'uptime']
    with open(csv_filename, 'w', encoding='utf-8') as f_d:
        writer = csv.writer(f_d)
        writer.writerow(headers)
        for filename in data_filenames:
            with open(filename, 'r', encoding='utf-8') as f_s:
                hostname = filename.replace('sh_version_', '').replace('.txt', '')
                row = list(parse_sh_version(f_s.read()))
                row.insert(0, hostname)
                writer.writerow(row)


def main():
    sh_version_files = glob.glob('sh_vers*')
    write_inventory_to_csv(sh_version_files, 'test.csv')


if __name__ == '__main__':
    main()
