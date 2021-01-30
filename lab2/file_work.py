

def get_symbols_from_file(f):
    with open(f, 'rb') as file:
        return file.read()

def write_symbols_in_file(f, lst):
    with open(f, 'wb') as file:
        for symbol in lst:
            file.write(symbol.to_bytes(1, byteorder='big'))