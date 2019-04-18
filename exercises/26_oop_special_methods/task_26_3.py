# -*- coding: utf-8 -*-

'''
Задание 26.3

В этом задании необходимо создать класс IPAddress.

При создании экземпляра класса, как аргумент передается IP-адрес и маска,
а также выполняется проверка корректности адреса и маски:
* Адрес считается корректно заданным, если он:
   - состоит из 4 чисел разделенных точкой
   - каждое число в диапазоне от 0 до 255
* маска считается корректной, если это число в диапазоне от 8 до 32 включительно

Если маска или адрес не прошли проверку, необходимо сгенерировать исключение ValueError с соответствующим текстом (смотри вывод ниже).

Также, при создании класса, должны быть созданы два атрибута экземпляра: ip и mask, в которых содержатся адрес и маска, соответственно.

Пример создания экземпляра класса:
In [1]: ip = IPAddress('10.1.1.1/24')

Атрибуты ip и mask
In [2]: ip1 = IPAddress('10.1.1.1/24')

In [3]: ip1.ip
Out[3]: '10.1.1.1'

In [4]: ip1.mask
Out[4]: 24

Проверка корректности адреса (traceback сокращен)
In [5]: ip1 = IPAddress('10.1.1/24')
---------------------------------------------------------------------------
...
ValueError: Incorrect IPv4 address

Проверка корректности маски (traceback сокращен)
In [6]: ip1 = IPAddress('10.1.1.1/240')
---------------------------------------------------------------------------
...
ValueError: Incorrect mask

'''

import re


class IPAddress:
    def __init__(self, address):
        self.ip, self.mask = self._get_ip_and_mask(address)

    def _get_ip_and_mask(self, address):
        '''
        Returns ip and mask if the supplied value has correct format.
        :param address: IP address in CIDR notation
        :return: ip (str), mask (int)
        '''
        if not re.search(r'^(\d{1,3}\.){3}\d{1,3}/\d{1,2}$', address):
            raise ValueError('Incorrect IPv4 address')
        ip, mask = address.split('/')
        mask = int(mask)
        for octet in map(int, ip.split('.')):
            if octet not in range(0, 256):
                raise ValueError('Incorrect IPv4 address')
        if int(mask) not in range(8, 33):
            raise ValueError('Incorrect mask')
        return ip, mask


def main():
    ip = IPAddress('192.168.1.1/24')
    print(ip.ip, ip.mask)


if __name__ == '__main__':
    main()

# Все отлично

