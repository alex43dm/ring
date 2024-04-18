#!/usr/bin/env python3

from serial import Serial, serialutil
from os.path import exists, basename
from sys import argv
from traceback import print_exc

#########################################################################
#########################################################################
#main
if __name__ == "__main__":
    try:
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

        while not exists(port):
            print("wait port: {0}".format(port))
            sleep(1)


        ser = Serial()
        ser.port = port
        ser.timeout = 0.1

        print("open port: {0}".format(port))
        ser.open()

        for i in range(12):
            ser.write(LEDS[i])
            s = ser.readline()
            print("{0}".format(s.decode("utf-8").rstrip()))

        ser.close()
    except serialutil.SerialException as ex:
        ser.close()
    except Exception as ex:
        print(ex)
        print_exc()

