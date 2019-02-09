# -*- coding: utf-8 -*-
'''
Задание 9.4a

Задача такая же, как и задании 9.4, но функция convert_config_to_dict должна поддерживать еще один уровень вложенности.
При этом, не привязываясь к конкретным разделам в тестовом файле.
Функция должна быть универсальной, и сработать, если это будут другие разделы.

Если уровня вложенности два:
* то команды верхнего уровня будут ключами словаря,
* а команды подуровней - списками

Если уровня вложенности три:
* самый вложенный уровень должен быть списком,
* а остальные - словарями.

При записи команд в словарь, пробелы в начале строки надо удалить.

Проверить работу функции надо на примере файла config_r1.txt

Обратите внимание на конфигурационный файл.
В нем есть разделы с большей вложенностью, например, разделы:
* interface Ethernet0/3.100
* router bgp 100

Секция итогового словаря на примере interface Ethernet0/3.100:

'interface Ethernet0/3.100':{
               'encapsulation dot1Q 100':[],
               'xconnect 10.2.2.2 12100 encapsulation mpls':
                   ['backup peer 10.4.4.4 14100',
                    'backup delay 1 1']}

Примеры других секций словаря можно посмотреть в тесте к этому заданию.
Тест проверяет не весь словарь, а несколько разнотипных секций.

Ограничение: Все задания надо выполнять используя только пройденные темы.

'''

ignore = ['duplex', 'alias', 'Current configuration']


def ignore_command(command, ignore):
    '''
    Функция проверяет содержится ли в команде слово из списка ignore.

    command - строка. Команда, которую надо проверить
    ignore - список. Список слов

    Возвращает
    * True, если в команде содержится слово из списка ignore
    * False - если нет
    '''
    return any(word in command for word in ignore)


def convert_config_to_dict(config_filename):
  result = {}
  with open(config_filename, 'r') as f:
    command = subcommand = ''
    for line in f:
      if ignore_command(line, ignore) or line.strip() == '' : continue
      if not line.startswith('!'):
        if not line.startswith(' '):
          command = line.strip()
          result.setdefault(command, [])
        elif line.startswith(' ') and not line.startswith('  '):
          subcommand = line.strip()
          result[command].append(subcommand)
        elif line.startswith('  '):
          if type(result[command]) == list:
            temp_dict = {key: [] for key in result[command]}
            del(result[command])
            result[command] = temp_dict
          result.setdefault(command, {})
          result[command].setdefault(subcommand, [])
          result[command][subcommand].append(line.strip())
      else:
        command = subcommand = ''
  return result

