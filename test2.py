import time


def delay():
    time.sleep(5)
    with open('finished.txt', 'w') as f:
        f.write('Finished')


if __name__ == '__main__':
    print('Deamon Process')
    delay()
    print('Deamon finished')