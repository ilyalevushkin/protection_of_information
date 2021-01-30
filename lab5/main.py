from menu import *
from file_work import *
from es import ElectronicSignature

def sign_data(symbols):
    es = ElectronicSignature()
    # подписывание документа
    print('\nПодписывание документа...\n')
    private_f = bytes(str(input(f"Введите имя файла с закрытым ключом: ")), 'utf-8')
    private_key = get_symbols_from_file(private_f)
    signature = es.sign_data(symbols, private_key)
    print('Подписано!')
    print(f'Ваша электронная подпись: {signature}')
    f_sig = str(input('Введите файл, в который будет записана подпись: '))
    write_key_in_file(f_sig, signature)

def check_data(symbols):
    # проверка документа
    print('\nПроверка документа...\n')
    public_f = bytes(str(input(f"Введите имя файла с открытым ключом: : ")), 'utf-8')
    f_sig = bytes(str(input(f"Введите имя файла с подписью: : ")), 'utf-8')
    public_key = get_symbols_from_file(public_f)
    signature = get_symbols_from_file(f_sig)
    if es.check_data(symbols, public_key, signature):
        print('Проверка успешна')
    else:
        print('Ошибка!')

if __name__ == '__main__':
    es = ElectronicSignature()
    public_key, private_key = es.get_keys()
    print(f'Вам выдан открытый:{public_key}\n и закрытый:{private_key} ключи.')
    f_private = str(input('Введите файл, в который будет записан закрытый ключ: '))
    f_public = str(input('Введите файл, в который будет записан открытый ключ: '))
    write_key_in_file(f_public, public_key)
    write_key_in_file(f_private, private_key)
    while True:
        print_menu()
        choice = int(input())
        if choice == 1:
            bytes_array = bytes(str(input("Введите сообщение: ")), 'utf-8')
        elif choice == 2:
            load_file = str(input("Ввведите имя файла: "))
            bytes_array = get_symbols_from_file(load_file)
        else:
            break
        while True:
            print_work_menu()
            choice = int(input())
            if choice == 1:
                sign_data(bytes_array)
            elif choice == 2:
                check_data(bytes_array)
            else:
                break
