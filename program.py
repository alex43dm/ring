#!/usr/bin/env python3

from serial import Serial, serialutil
from os.path import exists, basename
from sys import argv
from traceback import print_exc
from random import getrandbits
from time import sleep

port = "/dev/ttyACM3" #argv.pop()

LEDS = [
    b'000000',
    b'000000',
    b'000000',
    b'000000',
    b'000000',
    b'000000',
    b'000000',
    b'000000',
    b'000000',
    b'000000',
    b'000000',
    b'000000' ]

#########################################################################
def collor_set_all(b):
    for i in range(12):
        LEDS[i] = bytes(b)
    led_write()

def led_write():
    try:
        while not exists(port):
            print("wait port: {0}".format(port))
            sleep(1)

        ser = Serial()
        ser.port = port
        ser.timeout = 0.1

#        print("open port: {0}".format(port))
        ser.open()

        for i in range(12):
            ser.write(LEDS[i])
            s = ser.readline()
#            print("{0}".format(s.decode("utf-8").rstrip()))

        ser.close()
    except serialutil.SerialException as ex:
        ser.close()
        print(ex)
        print_exc()
    except Exception as ex:
        print(ex)
        print_exc()

def color_random():
    r = b'%0.2X' % getrandbits(8)
    g = b'%0.2X' % getrandbits(8)
    b = b'%0.2X' % getrandbits(8)
    return g + r + b

def collor_set_all_random():
    for i in range(12):
        LEDS[i] = color_random()
    led_write()

def collor_set_random_move():
    for i in reversed(range(12)):
        LEDS[i] = LEDS[i-1]
    LEDS[0] = color_random()
    led_write()

#main
if __name__ == "__main__":
    collor_set_all(b'000000')
    while(True):
        #collor_set_all_random()
#        collor_set_all(color_random())
        collor_set_random_move()
        sleep(0.3)
