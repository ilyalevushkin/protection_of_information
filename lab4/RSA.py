import re
import numpy as np
from random import randint

class RSA:
    def __init__(self):
        # задаем диапазон для p и q
        self.p = self.get_random_prime_number(1000, 10000)
        self.q = self.get_random_prime_number(1000, 10000)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = self.get_e(self.phi)
        self.d = self.get_d(self.e, self.phi)
        self.bytes_amount = self.get_bytes_amount(self.n)


    def is_prime(self, number):
        if number % 2 == 0:
            return False
        for i in range(3, number // 2 + 1, 2):
            if number % i == 0:
                return False
        return True

    # создает случайное простое число в заданном диапазоне
    def get_random_prime_number(self, A, B):
        number = randint(A, B)
        res = number
        while res < B + 1:
            if self.is_prime(res):
                return res
            res += 1
        res = number

        while res >= A - 1:
            if self.is_prime(res):
                return res
            res -= 1

        # возвращаем -1 если не нашли простых чисел в указанном диапазоне
        return -1

    def print_init(self):
        print('Инициализирован RSA со следующими параметрами:')
        print(f'p = {self.p}')
        print(f'q = {self.q}')
        print(f'n = {self.n}')
        print(f'phi = {self.phi}')
        print(f'e = {self.e}')
        print(f'd = {self.d}')
        print(f'Количество байт, в которое кодируется каждый символ = {self.bytes_amount}')

    def is_mutually_simple(self, num1, num2):
        while num1 != 0 and num2 != 0:
            if num1 >= num2:
                num1 %= num2
            else:
                num2 %= num1
        return (num1 + num2) == 1

    def get_e(self, phi):
        # зададим минимальное e = 17
        res = 17
        while res < phi:
            if self.is_prime(res):
                if self.is_mutually_simple(res, phi):
                    return res
            res += 1

        return -1

    def get_d(self, e, phi):
        # пусть минимальное d = sqrt4(n)
        d = int(pow(self.n, 0.25))
        while ((d * e) % phi) != 1:
            d += 1
        return d

    def get_bytes_amount(self, n):
        # вычисляем количество БИТ необходимых
        # для описания максимального числа
        k = 0
        while 2 ** k < n:
            k += 1
        # возвращаем количество байт
        return k // 8 + ((k % 8) != 0)


    def fast_exp_module(self, symbol, bit_str, res, module):
        if bit_str[0] == '1':
            res *= symbol

        if len(bit_str) == 1:
            return res % module

        return self.fast_exp_module(symbol, bit_str[1:], (res ** 2) % module, module)

    def exp_module(self, symbol, exp, module):
        #return int(pow(symbol, exp, module))

        # алгоритм быстрого возведения в степень из википедии
        bit_str = bin(exp)[2:]
        return self.fast_exp_module(symbol, bit_str, 1, module)

        # попытка ускорить возведение в степень по модулю по памяти
        '''res = 1
        i = 0
        delta = 1000
        while i < (exp - delta):
            res = (res * (symbol ** delta)) % module
            i += delta
        res = (res * (symbol ** (exp - i)) % module)
        return res'''

        # возведение в степень по модулю эффективное по памяти
        '''res = 1
        i = 0
        while i < exp:
            res = (res * symbol) % module
            i += 1
        return res'''

        # убогий вариант возведения в степень по модулю
        #return (symbol ** exp) % module

    def crypt_symb(self, symbol, exp, module):
        return self.exp_module(symbol, exp, module)

    def convert_new_symb_to_lst_bytes(self, symb):
        bytes = symb.to_bytes(self.bytes_amount, byteorder='big')
        return list(bytes)

    def encode_str(self, lst):
        res = []
        for byte in lst:
            new_symb = self.crypt_symb(byte, self.e, self.n)
            res.extend(self.convert_new_symb_to_lst_bytes(new_symb))
        return res


    def get_symb_from_lst(self, lst, pos):
        return int.from_bytes(bytes(lst[pos : pos + self.bytes_amount]), byteorder='big'), pos + self.bytes_amount

    def decode_str(self, lst):
        res = []
        i = 0
        while i < len(lst):
            symb, new_i = self.get_symb_from_lst(lst, i)
            decrypt_symb = self.crypt_symb(symb, self.d, self.n)
            res.append(decrypt_symb)
            i = new_i

        return res
