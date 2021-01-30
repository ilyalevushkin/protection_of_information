from menu import *
from file_work import *
from AES import AES


def str_to_ascii(symbols):
    res = []
    for i in symbols:
        res.append(ord(i))
    return res

def ascii_to_str(ascii_lst):
    res = []
    for i in ascii_lst:
        res.append(chr(i))
    return res

if __name__ == '__main__':
    while True:
        print_aes_menu()
        choice = int(input())
        if choice == 1:
            aes = AES(128)
            print_menu()
            choice = int(input())
            if choice == 1:
                symbols_str = str(input("Введите строку: "))
                symbols = str_to_ascii(symbols_str)
                encode = aes.encrypt_str(symbols)
                encode_str = ascii_to_str(encode)
                print(f"Строка \'{symbols_str}\' перекодирована в \'{encode_str}\'")

                decode = aes.decrypt_str(encode)
                decode_str = ascii_to_str(decode)
                print(f"Строка \'{encode_str}\' расшифрована в \'{decode_str}\'")
            elif choice == 2:
                load_file = str(input("Ввведите имя файла: "))
                symbols = get_symbols_from_file(load_file)
                encode = aes.encrypt_str(symbols)

                encode_file = str(input("Введите, куда записать зашифрованный файл: "))
                write_symbols_in_file(encode_file, encode)

                decode = aes.decrypt_str(encode)
                decode_file = str(input("Введите, куда записать расшифрованный файл: "))
                write_symbols_in_file(decode_file, decode)
            else:
                break
        elif choice == 2:
            break
        elif choice == 3:
            break
        else:
            break