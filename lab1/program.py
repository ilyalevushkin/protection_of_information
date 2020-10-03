from sys import platform
from subprocess import check_output
import re

def create_unic_key(command):
    res = re.findall(r': (\d+)\n', command)
    return ''.join(res)

def get_access_key():
    with open('license.key', 'r') as f:
        key = f.readlines()[0]
    return key

def check_system_specification():
    check = False
    if platform.startswith('win32'):
        print('win32')
    elif platform.startswith('linux'):
        print('linux')
    elif platform.startswith('darwin'):
        print('darwin')
        command = check_output('sysctl hw', shell=True).decode()
        key = create_unic_key(command)
        try:
            access_key = get_access_key()
            if (key == access_key):
                check = True
        except:
            pass
    else:
        print('other')
    return check



if __name__ == '__main__':
    if check_system_specification():
        print("Hello, your app works!")
    else:
        print("Access denied")
