# -*- coding: utf-8 -*-
'''
Задание 21.1

Создать функцию generate_config.

Параметры функции:
* template - путь к файлу с шаблоном (например, "templates/for.txt")
* data_dict - словарь со значениями, которые надо подставить в шаблон

Функция должна возвращать строку с конфигурацией, которая была сгенерирована.

Проверить работу функции на шаблоне templates/for.txt и данных из файла data_files/for.yml.

'''

from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader


def generate_config(template, data_dict):
    # We need to cut the filepath (template) into pieces
    template_path = Path(template)
    directory = str(template_path.parent)
    file = template_path.name
    env = Environment(loader=FileSystemLoader(directory), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(file)
    return template.render(data_dict)


def main():
    print('test')
    with open('data_files/for.yml', 'r', encoding='utf-8') as f:
        data_dict = yaml.safe_load(f)
        print(generate_config('templates/for.txt', data_dict))


if __name__ == '__main__':
    main()
