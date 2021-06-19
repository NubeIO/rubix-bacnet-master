import time

import BAC0

bacnet = BAC0.lite('192.168.15.102/24:47808')




def start():
    def my_callback(elements):
        print("Present value is : {}".format(elements['properties']['presentValue']))

    bacnet.cov('192.168.15.100', ("analogOutput", 1), confirmed=True, lifetime=30, callback=my_callback)

    while True:
        time.sleep(0.2)


if __name__ == '__main__':
    start()
