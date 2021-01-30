from menu import *
from file_work import *
from RSA import RSA


def str_to_unicode(symbols):
    res = []
    for i in symbols:
        res.append(ord(i))
    return res

def unicode_to_str(ascii_lst):
    res = []
    for i in ascii_lst:
        res.append(chr(i))
    return res

if __name__ == '__main__':
    rsa = RSA()
    rsa.print_init()
    while True:
        print_menu()
        choice = int(input())
        if choice == 1:
            symbols_str = str(input("Введите строку: "))
            symbols = str_to_unicode(symbols_str)
            encode = rsa.encode_str(symbols)
            encode_str = unicode_to_str(encode)
            print(f"Строка \'{symbols_str}\' перекодирована в \'{encode_str}\'")

            decode = rsa.decode_str(encode)
            decode_str = unicode_to_str(decode)
            print(f"Строка \'{encode_str}\' расшифрована в \'{decode_str}\'")
        elif choice == 2:
            load_file = str(input("Ввведите имя файла: "))
            symbols = get_symbols_from_file(load_file)
            encode = rsa.encode_str(symbols)

            encode_file = str(input("Введите, куда записать зашифрованный файл: "))
            write_symbols_in_file(encode_file, encode)

            #расшифровка файла
            symbols = get_symbols_from_file(encode_file)
            decode = rsa.decode_str(symbols)
            decode_file = str(input("Введите, куда записать расшифрованный файл: "))
            write_symbols_in_file(decode_file, decode)
        else:
            break