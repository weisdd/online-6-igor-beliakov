# -*- coding: utf-8 -*-

'''
Задание 26.3a

Изменить класс IPAddress из задания 26.3.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

Для этого задания нет теста!
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

    def __str__(self):
        return f'IP address {self.ip}/{self.mask}'

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.ip}/{self.mask}')"


def main():
    ip1 = IPAddress('192.168.1.1/24')
    print(ip1.__str__())
    print(ip1.__repr__())


if __name__ == '__main__':
    main()

# Все отлично
