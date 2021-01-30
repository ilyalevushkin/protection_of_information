import re
import numpy as np
from random import randint

class HuffmanTree:

    # инициализация листа
    def leaf_init(self, weight, value):
        return {'value': value, 'left': None, 'right': None, 'weight': weight}

    def make_node(self, elem1, elem2):
        return {'value': None, 'left': elem1, 'right': elem2, 'weight': elem1['weight'] + elem2['weight']}

    def shuffle_node(self, tree_lst, node):
        i = 0
        while i < len(tree_lst) and node['weight'] > tree_lst[i]['weight']:
            i += 1

        tree_lst.insert(i, node)


    # на выходе дерево вида: {'value', 'left', 'right', 'weight'}
    def create_tree(self, freq_table):
        # инициализация списка листьев
        tree_lst = []
        for i in freq_table:
            tree_lst.append(self.leaf_init(i[0], i[1]))

        while len(tree_lst) != 1:
            node = self.make_node(tree_lst.pop(0), tree_lst.pop(0))
            self.shuffle_node(tree_lst, node)

        return tree_lst[0]


    def get_symbol_code_dict_help(self, node, code):
        if not node['left'] and not node['right']:
            return {node['value']: code}

        d = {}
        if node['left']:
            d.update(self.get_symbol_code_dict_help(node['left'], code + '1'))
        if node['right']:
            d.update(self.get_symbol_code_dict_help(node['right'], code + '0'))
        return d

    # получаем словарь с парами: {symbol : code} (ex.: {'D':'101'})
    def get_symbol_code_dict_from_tree(self, tree):
        return self.get_symbol_code_dict_help(tree, '')

    # получаем словарь с парами: {code : symbol} (ex.: {'101':'D'})
    def get_code_symbol_dict_from_data(self, data):
        d = {}
        pos = 0
        while True:
            symbol = chr(data[pos])
            pos += 1

            code = ''
            while data[pos] != 44 and data[pos] != 46:
                code += chr(data[pos])
                pos += 1

            d.update({code: symbol})

            if data[pos] == 46:
                pos += 1
                break
            pos += 1

        return d, pos

    def update_tree(self, head, code, symbol):
        if len(code) == 0:
            head['value'] = symbol
        elif code[0] == '0':
            if not head['right']:
                head['right'] = {'value': None, 'left': None, 'right': None}
            self.update_tree(head['right'], code[1:], symbol)
        elif code[0] == '1':
            if not head['left']:
                head['left'] = {'value': None, 'left': None, 'right': None}
            self.update_tree(head['left'], code[1:], symbol)

    def create_tree_from_code_symbol_dict(self, code_symbol_dict):
        tree = {'value': None, 'left': None, 'right': None}
        for code, symbol in code_symbol_dict.items():
            self.update_tree(tree, code, symbol)
        return tree

    def get_value_by_bits(self, bits, node, way_len):
        if not node['left'] and not node['right']:
            return node['value'], way_len


        if bits[0] == '0':
            return self.get_value_by_bits(bits[1:], node['right'], way_len + 1)
        elif bits[0] == '1':
            return self.get_value_by_bits(bits[1:], node['left'], way_len + 1)



class Huffman:
    def __init__(self):
        # задаем диапазон для p и q
        self.huffman_tree = HuffmanTree()

    # возвращает список вида: [(частота, буква),...]
    def get_freq_table(self, lst):
        d = {}
        for i in lst:
            if i not in d:
                d.update({i: 1})
            else:
                d[i] += 1
        return list(zip(d.values(), d.keys()))

    # на выходе: ['010010101001010']
    def encode_data_to_bits(self, symbol_code_dict, data):
        bits_lst = [symbol_code_dict[symbol] for symbol in data]
        bits = ''
        for i in bits_lst:
            bits += i
        return bits

    def str_to_int(self, code):
        return [ord(symbol) for symbol in code]

    # [{symbol:code}, {symbol:code},...] -> [
    # ord(symbol), ord('0'), ord('1'), ..., ord(','),
    # ord(symbol), ord('0'), ord('1'), ..., ord(','),
    # ...,
    # ord(symbol), ord('0'), ord('1'), ..., ord('.')
    # ]
    def tree_to_bytes_lst(self, symbol_code_dict):
        lst = []
        for symbol, code in symbol_code_dict.items():
            lst.append(symbol)
            lst.extend(self.str_to_int(code))
            lst.append(ord(','))
        lst.pop()
        lst.append(ord('.'))
        return lst

    # на входе: '010101010101011101000...'
    # на выходе: [21, 42, ...]
    def bits_lst_to_bytes_lst(self, bits):
        # берем по 8 бит
        bytes_lst = []
        i = 0

        # считаем количество нуликов в начале файла и добавляем его в конец
        while bits[i] == '0':
            i += 1
        zero_start_amount = i

        while i < len(bits) - 8:
            bytes_lst.append(int(bits[i:i+8], 2))
            i += 8
        last_elem = bits[i:i+8]
        bytes_lst.append(int(bits[i:i + 8], 2))
        bytes_lst.append(len(last_elem))
        bytes_lst.append(zero_start_amount)
        return bytes_lst

    def bytes_lst_to_bits_lst(self, bytes):
        zero_start_amount = bytes[-1]
        bits_lst = '0' * zero_start_amount

        for i in range(len(bytes) - 3):
            number = bin(bytes[i])[2:]
            bits_lst += '0' * (8 - len(number)) + number
        len_last_elem = bytes[-2]
        last_elem = bin(bytes[-3])[2:]
        bits_lst += '0' * (len_last_elem - len(last_elem)) + last_elem
        return bits_lst

    # на входе: bits = '10101010101010101',
    # tree
    def decode_data_from_bits(self, bits, tree):
        data = []
        i = 0
        while i < len(bits):
            value, way_len = self.huffman_tree.get_value_by_bits(bits[i:], tree, 0)
            data.append(ord(value))
            i += way_len
        return data

    def encode_str(self, lst):
        freq_table = self.get_freq_table(lst)
        sorted_freq_table = sorted(freq_table)
        tree = self.huffman_tree.create_tree(sorted_freq_table)
        symbol_code_dict = self.huffman_tree.get_symbol_code_dict_from_tree(tree)

        return self.tree_to_bytes_lst(symbol_code_dict) + \
            self.bits_lst_to_bytes_lst(self.encode_data_to_bits(symbol_code_dict, lst))

    def decode_str(self, lst):
        code_symbol_dict, pos = self.huffman_tree.get_code_symbol_dict_from_data(lst)

        tree = self.huffman_tree.create_tree_from_code_symbol_dict(code_symbol_dict)

        return self.decode_data_from_bits(self.bytes_lst_to_bits_lst(lst[pos:]), tree)
