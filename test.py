import subprocess
import time
import os


if __name__ == '__main__':
    print('Main')
    #subprocess.Popen(['python', 'test2.py'])
    DETACHED_PROCESS = 8
    proc = subprocess.Popen('python test2.py', creationflags=DETACHED_PROCESS, close_fds=True)
    subprocess.Popen(f'taskkill /F /im {proc.pid}')
    print('Main End')