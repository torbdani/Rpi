#!/usr/bin/env python
import atexit
import logging
import struct
from time import sleep
import csv
import sys

from LedStrip_WS2801 import *


logging.basicConfig(filename='/var/log/grid.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger('grid')

ledStrip = LedStrip_WS2801(75)

grid = []


def main():
    populateGrid()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        logger.debug("Using file: " + filename)
        animation = get_animation(filename)
    else:
        animation = get_animation('test.anim')

    while 1:
        show_animation(animation)


def show_animation(animation):
    for frame in animation:
        for row in range(0, 8):
            for col in range(0, 9):
                gridnr = grid[row][col]
                animnr = frame[row][col]
                ledStrip.setPixel(gridnr, animnr)
        ledStrip.update()
        sleep(0.5)


def populateGrid():
    with open('grid.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp = []
            for col in row:
                tmp.append(int(col))
            grid.append(tmp)
    grid.reverse()


def get_animation(filename):
    anim = []
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        frame = []
        for row in reader:
            if len(row) == 0:
                frame.reverse()
                anim.append(frame)
                frame = []
            else:
                tmp = []
                for col in row:
                    tmp.append(hex_to_rgb(col))
                frame.append(tmp)
    frame.reverse()
    anim.append(frame)
    return anim


def hex_to_rgb(hexvalue):
    return struct.unpack('BBB', hexvalue.decode('hex'))


def clear_all():
    ledStrip.setAll([0, 0, 0])
    ledStrip.update()

@atexit.register
def cleanup():
    logger.debug('cleaning up')
    clear_all()

if __name__ == '__main__':
    main()