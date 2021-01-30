import re
import numpy as np
from tables import Tables

#InvSBox[SBox[i]] = i.


class AES:
    def __init__(self, version):
        if version == 128:
            self.encrypt = self._encrypt_128
            self.decrypt = self._decrypt_128
            self.encrypt_str = self._encrypt_128_str
            self.decrypt_str = self._decrypt_128_str
            self.test_key = [symbol for symbol in range(16)]
            self.N_k = 4
            self.N_b = 4
            self.N_r = 10
            self.tables = Tables()
        elif version == 192:
            pass
        elif version == 256:
            pass
        else:
            pass

    def _convert_to_4_np_matrix(self, lst, N):
        res = np.zeros((4, N), dtype=int)
        for i in range(4):
            for j in range(N):
                res[i, j] = lst[j]
            lst = lst[N:]
        return res

    def _convert_from_4_np_matrix(self, m):
        res = []
        for i in m:
            res.extend(i)
        return res


    def _sub_byte(self, byte, S_table):
        i = byte // 16
        j = byte % 16
        return S_table[i, j]

    def _sub_bytes_v(self, v, inv):
        if inv:
            S_table = self.tables.get_inverse_S_substitution()
        else:
            S_table = self.tables.get_S_substitution()
        for i in range(len(v)):
            v[i] = self._sub_byte(v[i], S_table)
        return v

    def _sub_bytes_m(self, m, inv):
        res = self._sub_bytes_v(m[0], inv=inv)
        for i in range(1, m.shape[0]):
            res = np.column_stack((res, self._sub_bytes_v(m[i], inv=inv)))
        return res


    def _xor_v(self, v1, v2):
        res = np.empty((v1.shape[0],), dtype=int)
        for i in range(len(v1)):
            res[i] = v1[i] ^ v2[i]
        return res

    def _xor_m(self, m1, m2):
        res = np.empty((m1.shape[0], m1.shape[1]), dtype=int)
        for i in range(m1.shape[0]):
            for j in range(m2.shape[1]):
                res[i, j] = m1[i, j] ^ m2[i, j]
        return res

    #циклический сдвиг на move байт влево
    def _rot_world(self, lst, move, left):
        if left:
            return np.append(lst[move:], lst[:move])
        else:
            return np.append(lst[len(lst) - move:], lst[:len(lst) - move])

    #циклический сдвиг матрицы
    def _shift_rows(self, m, inv):
        for i in range(m.shape[0]):
            if inv:
                m[i] = self._rot_world(m[i], i, left=False)
            else:
                m[i] = self._rot_world(m[i], i, left=True)
        return m


    def _GF_2_8_multiply(self, number1, number2):
        #перевод числа в двоичное представление
        number2_str = bin(number2)
        res = 0
        for i in range(len(number2_str) - 2):
            if number2_str[len(number2_str) - i - 1] == '1':
                res ^= number1 << i

        # xorим res на полином x^8 + x^4 + x^3 + x + 1 домноженный на x^(len(bin(res)) - 2 - 9)
        # до тех пор пока len(bin(res)) - 2 >= 9
        while len(bin(res)) >= 11:
            res ^= 283 << (len(bin(res)) - 11)

        return res

    def _mix_elem(self, m_str, v):
        sum = 0
        for i in range(len(m_str)):
            sum ^= self._GF_2_8_multiply(m_str[i], v[i])
        return sum

    def _mix_column(self, v, inv):
        if inv:
            C_x = self.tables.get_inverse_C_x()
        else:
            C_x = self.tables.get_C_x()
        res = []
        for i in range(C_x.shape[0]):
            res.append(self._mix_elem(C_x[i, :], v))
        return np.array(res)


    # умножение многочлена C(x) на каждый столбец матрицы
    # умножение выполняется по модулю неприводимого
    # двоичного полинома степени 8: x^8 + x^4 + x^3 + x + 1
    def _mix_columns(self, m, inv):
        res = self._mix_column(m[:, 0], inv=inv)
        for i in range(1, m.shape[1]):
            res = np.column_stack((res, self._mix_column(m[:, i], inv=inv)))
        return res

    def _key_expansion(self, bytes_matrix, N_r):
        RCon_table = self.tables.get_RCon()
        exp_key = [bytes_matrix]
        for i in range(N_r):
            i_key = self._xor_v(
                self._xor_v(
                    self._sub_bytes_v(
                        self._rot_world(exp_key[-1][:, 3], 1, left=True), inv=False),
                    RCon_table[:, i]), exp_key[-1][:, 0])

            i_key = np.column_stack((i_key, self._xor_v(i_key, exp_key[-1][:, 1])))
            i_key = np.column_stack((i_key, self._xor_v(i_key[:, 1], exp_key[-1][:, 2])))
            i_key = np.column_stack((i_key, self._xor_v(i_key[:, 2], exp_key[-1][:, 3])))
            exp_key.append(i_key)
        return exp_key


    #block - 16 bytes list
    def _encrypt_128(self, block, key):
        key = self._convert_to_4_np_matrix(key, self.N_k)
        block = self._convert_to_4_np_matrix(block, self.N_b)
        exp_key = self._key_expansion(key, self.N_r)

        block = self._xor_m(block, exp_key[0])
        
        for i in range(self.N_r):
            block = self._sub_bytes_m(block, inv=False)
            block = self._shift_rows(block, inv=False)
            if (i != self.N_r - 1):
                block = self._mix_columns(block, inv=False)
            block = self._xor_m(block, exp_key[i + 1])
        
        return self._convert_from_4_np_matrix(block)



    # block - 16 bytes list
    def _decrypt_128(self, block, key):
        key = self._convert_to_4_np_matrix(key, self.N_k)
        block = self._convert_to_4_np_matrix(block, self.N_b)
        exp_key = self._key_expansion(key, self.N_r)

        block = self._xor_m(block, exp_key[-1])

        for i in range(self.N_r):
            block = self._shift_rows(block, inv=True)

            block = self._sub_bytes_m(block, inv=True)

            block = self._xor_m(block, exp_key[len(exp_key) - i - 2])

            if (i != self.N_r - 1):
                block = self._mix_columns(block, inv=True)

        return self._convert_from_4_np_matrix(block)

    def _encrypt_128_str(self, data):
        symbols = list(data[:])
        len_symbols = len(symbols)
        if ((len(symbols) + 1) % 16) != 0:
            symbols.extend([0 for i in range(16 - (len_symbols % 16) - 1)])
        symbols.append(16 - (len_symbols % 16))

        res = []
        while len(symbols) != 0:
            buf = symbols[:16]
            buf_encrypt = self.encrypt(buf, self.test_key)
            res.extend(buf_encrypt)
            symbols = symbols[16:]
        return res

    def _decrypt_128_str(self, data):
        symbols = list(data[:])
        res = []
        while len(symbols) != 0:
            buf = symbols[:16]
            buf_decrypt = self.decrypt(buf, self.test_key)
            res.extend(buf_decrypt)
            symbols = symbols[16:]

        clear_len_res = res[-1]

        return res[:-clear_len_res]



