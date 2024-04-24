#!/usr/bin/env python3

from serial import Serial, serialutil
from os.path import exists, basename
from sys import argv, _getframe
from traceback import print_exc
from random import getrandbits
from time import sleep
import usb.core
import usb.backend.libusb1

port = '/dev/ttyACM1' #argv.pop()

DEBUG = True

#########################################################################
class Ring():
    def __init__(self, port):
        self.LEDS = [
            '000000',
            '000000',
            '000000',
            '000000',
            '000000',
            '000000',
            '000000',
            '000000',
            '000000',
            '000000',
            '000000',
            '000000' ]

        try:
            while not exists(port):
                print("wait port: {0}".format(port))
                sleep(1)

            self.ser = Serial()
            self.ser.port = port
            self.ser.timeout = 0.1
            if DEBUG:
                print("open port: {0}".format(port))
            self.ser.open()
        except serialutil.SerialException as ex:
            self.ser.close()
            print(ex)
            print_exc()
        except Exception as ex:
            print(ex)
            print_exc()

    def write(self, val):
        if DEBUG:
            print(_getframe(  ).f_code.co_name)
        try:
            self.ser.write(val.encode('ascii'))
            s = self.ser.readline()
            if DEBUG:
                print("{0} {1}".format(len(s),s.decode("utf-8").rstrip()))
        except serialutil.SerialException as ex:
            self.ser.close()
            print(ex)
            print_exc()
        except Exception as ex:
            print(ex)
            print_exc()

    def collor_set_all(self, b):
        for i in range(12):
            self.LEDS[i] = b
        self.led_write()

    def led_write(self):
        if DEBUG:
            print(_getframe(  ).f_code.co_name)
        try:
            for i in range(12):
                self.write('00' + '%0.2X' % i + self.LEDS[i])
            self.write('01')
        except Exception as ex:
            print(ex)
            print_exc()

    def led_off(self):
        try:
            self.write('03')
        except Exception as ex:
            print(ex)
            print_exc()

    def led_white(self, val):
        try:
            self.write('04' + '%0.2X' % val)
        except Exception as ex:
            print(ex)
            print_exc()

    def led_green(self, val):
        try:
            self.write('05' + '%0.2X' % val)
        except Exception as ex:
            print(ex)
            print_exc()

    def led_red(self, val):
        try:
            self.write('06' + '%0.2X' % val)
        except Exception as ex:
            print(ex)
            print_exc()

    def led_blue(self, val):
        try:
            self.write('07' + '%0.2X' % val)
        except Exception as ex:
            print(ex)
            print_exc()

    def color_random(self):
        r = '%0.2X' % getrandbits(8)
        g = '%0.2X' % getrandbits(8)
        b = '%0.2X' % getrandbits(8)
        return g + r + b

    def collor_set_all_random(self):
        if DEBUG:
            print(_getframe(  ).f_code.co_name)
        for i in range(12):
            self.LEDS[i] = self.color_random()
        self.led_write()

    def collor_set_random_move(self):
        if DEBUG:
            print(_getframe(  ).f_code.co_name)
        try:
            self.collor_set_all_random()
            while True:
                for i in reversed(range(12)):
                    if i == 0: break
                    self.LEDS[i] = self.LEDS[i-1]
                self.LEDS[0] = self.color_random()
                self.led_write()
                sleep(0.3)
        except KeyboardInterrupt:
            pass

    def chip_save(self):
        if DEBUG:
            print(_getframe(  ).f_code.co_name)
        try:
            self.write('08')
        except Exception as ex:
            print(ex)
            print_exc()

    def chip_read(self):
        if DEBUG:
            print(_getframe(  ).f_code.co_name)
        try:
            self.write('09')
        except Exception as ex:
            print(ex)
            print_exc()

    def led_print(self):
        if DEBUG:
            print(_getframe(  ).f_code.co_name)
        try:
            self.write('0A')
        except Exception as ex:
            print(ex)
            print_exc()

    def __deinit__(self):
        self.ser.close()

#main
if __name__ == "__main__":
    p = Ring(port)
#    p.collor_set_random_move()
#    p.led_off()
#    p.led_white(0x02)
#    p.collor_set_all_random()
#    p.chip_save()
#    p.chip_read()
    p.led_print()

