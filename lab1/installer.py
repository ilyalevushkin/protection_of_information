from sys import platform
from subprocess import check_output
import re

def create_unic_key(command):
    res = re.findall(r': (\d+)\n', command)
    return ''.join(res)


def print_access_key(key):
    with open('license.key', 'w') as f:
        f.write(key)

if __name__ == '__main__':
    if platform.startswith('win32'):
        print('win32')
    elif platform.startswith('linux'):
        print('linux')
    elif platform.startswith('darwin'):
        print('darwin')
        command = check_output('sysctl hw', shell=True).decode()
        key = create_unic_key(command)
        print_access_key(key)