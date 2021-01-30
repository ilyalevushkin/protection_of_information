from random import sample
from menu import print_menu
from file_work import *

class Rotor:

    def __init__(self, value, rotation, numbers_size):
        self.value = value
        self.base_value = value
        self.rotation = rotation
        self.dict_transition = self.create_dict_transition(numbers_size)


    def create_dict_transition(self, numbers_size):
        keys = sample(range(numbers_size), len(range(numbers_size)))
        values = sample(range(numbers_size), len(range(numbers_size)))
        return dict(zip(keys, values))

    def get_value(self):
        return self.value

    def get_rotation(self):
        return self.rotation

    def get_straight_transition(self, key):
        return self.dict_transition.get(key)

    def get_back_transition(self, value):
        for d_key, d_value in self.dict_transition.items():
            if d_value == value:
                return d_key

    def rotate(self):
        self.value += self.rotation

    def drop_rotor(self):
        self.value = self.base_value



class Reflector:

    def __init__(self, numbers_size):
        self.dict_transition = self.create_dict_transition(numbers_size)


    def create_dict_transition(self, numbers_size):
        keys = sample(range(numbers_size), len(range(numbers_size)))
        values = keys[::-1]
        return dict(zip(keys, values))

    def get_transition(self, key):
        return self.dict_transition.get(key)



class Transformation:

    def __init__(self, rotor1_value, rotor2_value, rotor3_value, numbers_size, way_of_transform = 0):
        self.numbers_size = numbers_size
        self.way_of_transform = way_of_transform
        self.rotor1_value = rotor1_value
        self.rotor2_value = rotor2_value
        self.rotor3_value = rotor3_value


    def get_transformation(self, symbol):
        res = 0
        if self.way_of_transform == 0:
            res = self._mod_sum(symbol, self.rotor1_value)
        elif self.way_of_transform == 1:
            res = self._abs_sum(symbol, self.rotor1_value, self.rotor2_value)
        elif self.way_of_transform == 2:
            res = self._abs_sum(symbol, self.rotor2_value, self.rotor3_value)
        elif self.way_of_transform == 3:
            res = self._mod_diff(symbol, self.rotor3_value)
        return res


    def get_reverse_transformation(self, symbol):
        res = 0
        if self.way_of_transform == 0:
            res = self._mod_diff(symbol, self.rotor1_value)
        elif self.way_of_transform == 1:
            res = self._abs_diff(symbol, self.rotor1_value, self.rotor2_value)
        elif self.way_of_transform == 2:
            res = self._abs_diff(symbol, self.rotor2_value, self.rotor3_value)
        elif self.way_of_transform == 3:
            res = self._mod_sum(symbol, self.rotor3_value)
        return res


    def _mod_sum(self, symbol, rotor_value):
        return (symbol + rotor_value) % self.numbers_size

    def _mod_diff(self, symbol, rotor_value):
        return (symbol - rotor_value) % self.numbers_size

    def _abs_sum(self, symbol, rotor1_value, rotor2_value):
        return self._mod_sum(symbol, abs(rotor1_value - rotor2_value))

    def _abs_diff(self, symbol, rotor1_value, rotor2_value):
        return self._mod_diff(symbol, abs(rotor1_value - rotor2_value))





class Enigma:

    def __init__(self, numbers_size = 26,
                 rotor1_value = 0,
                 rotor2_value = 1,
                 rotor3_value = 2,
                 rotor1_rotation = 1,
                 rotor2_rotation = 1,
                 rotor3_rotation = 0,
                 way1_of_transform = 0,
                 way2_of_transform = 1,
                 way3_of_transform = 2,
                 way4_of_transform = 3):
        self.numbers_size = numbers_size
        self.way1_of_transform = way1_of_transform
        self.rotor1 = Rotor(rotor1_value, rotor1_rotation, numbers_size)
        self.way2_of_transform = way2_of_transform
        self.rotor2 = Rotor(rotor2_value, rotor2_rotation, numbers_size)
        self.way3_of_transform = way3_of_transform
        self.rotor3 = Rotor(rotor3_value, rotor3_rotation, numbers_size)
        self.way4_of_transform = way4_of_transform
        self.reflector = Reflector(numbers_size)

    def drop_rotors(self):
        self.rotor1.drop_rotor()
        self.rotor2.drop_rotor()
        self.rotor3.drop_rotor()




    def encrypt_list_symbols(self, lst):
        res_lst = []
        for symbol in lst:
            res_lst.append(self.encrypt_symbol(symbol))
        return res_lst

    def decrypt_list_symbols(self, lst):
        self.drop_rotors()
        return self.encrypt_list_symbols(lst)



    def decrypt_symbol(self, symbol):
        self.drop_rotors()
        return self.encrypt_symbol(symbol)


    def encrypt_symbol(self, symbol):
        #вращаем роторы
        self.rotor1.rotate()
        self.rotor2.rotate()
        self.rotor3.rotate()
        #инициализируем трансформаторы
        self.transformation1 = Transformation(self.rotor1.value,
                                              self.rotor2.value,
                                              self.rotor3.value,
                                              self.numbers_size,
                                              self.way1_of_transform
                                              )
        self.transformation2 = Transformation(self.rotor1.value,
                                              self.rotor2.value,
                                              self.rotor3.value,
                                              self.numbers_size,
                                              self.way2_of_transform
                                              )
        self.transformation3 = Transformation(self.rotor1.value,
                                              self.rotor2.value,
                                              self.rotor3.value,
                                              self.numbers_size,
                                              self.way3_of_transform
                                              )
        self.transformation4 = Transformation(self.rotor1.value,
                                              self.rotor2.value,
                                              self.rotor3.value,
                                              self.numbers_size,
                                              self.way4_of_transform
                                              )


        #выполняем прямую трансформацию
        symbol = self.transformation1.get_transformation(symbol)
        symbol = self.rotor1.get_straight_transition(symbol)
        symbol = self.transformation2.get_transformation(symbol)
        symbol = self.rotor2.get_straight_transition(symbol)
        symbol = self.transformation3.get_transformation(symbol)
        symbol = self.rotor3.get_straight_transition(symbol)
        symbol = self.transformation4.get_transformation(symbol)

        #используем рефлектор
        symbol = self.reflector.get_transition(symbol)

        #выполняем обратную трансформацию
        symbol = self.transformation4.get_reverse_transformation(symbol)
        symbol = self.rotor3.get_back_transition(symbol)
        symbol = self.transformation3.get_reverse_transformation(symbol)
        symbol = self.rotor2.get_back_transition(symbol)
        symbol = self.transformation2.get_reverse_transformation(symbol)
        symbol = self.rotor1.get_back_transition(symbol)
        symbol = self.transformation1.get_reverse_transformation(symbol)

        return symbol



if __name__ == '__main__':
    while True:
        print_menu()
        choice = int(input())
        if choice == 1:
            enigma = Enigma(128)
            symbol = str(input("Введите символ: "))
            if len(symbol) != 1:
                print("Введен не один символ!")
                break
            encode = enigma.encrypt_symbol(symbol)
            print(f"Символ \'{symbol}\' перекодирован в \'{encode}\'")

            decode = enigma.decrypt_symbol(encode)
            print(f"Символ \'{encode}\' расшифрован в \'{decode}\'")
        elif choice == 2:
            enigma = Enigma(256)
            load_file = str(input("Ввведите имя файла: "))
            symbols = get_symbols_from_file(load_file)
            encode = enigma.encrypt_list_symbols(symbols)

            encode_file = str(input("Введите, куда записать зашифрованный файл: "))
            write_symbols_in_file(encode_file, encode)

            decode = enigma.decrypt_list_symbols(encode)
            decode_file = str(input("Введите, куда записать расшифрованный файл: "))
            write_symbols_in_file(decode_file, decode)
        else:
            break