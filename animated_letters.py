#!/usr/bin/env python
import json
import csv
import atexit
import logging
import struct
import sys
from time import sleep
from pprint import pprint
from LedStrip_WS2801 import *

alphabet_json_file = "alphabet.json"
grid = []

logging.basicConfig(filename='/var/log/grid.log', filemode='w', level=logging.DEBUG)
logger = logging.getLogger('grid')

ledStrip = LedStrip_WS2801(75)

def main():
    print alphabet_json_file
    parse_letters(alphabet_json_file)
    populateGrid()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        logger.debug("Using file: " + filename)
        animation = get_animation(filename)
    else:
        animation = get_animation('test.anim')

    while 1:
        show_animation(animation)

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

def show_animation(animation):
    for frame in animation:
        for row in range(0, 8):
            for col in range(0, 9):
                gridnr = grid[row][col]
                animnr = frame[row][col]
                ledStrip.setPixel(gridnr, animnr)
        ledStrip.update()
        sleep(0.25)

def populateGrid():
    with open('grid.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp = []
            for col in row:
                tmp.append(int(col))
            grid.append(tmp)
    grid.reverse()

def parse_letters(filename):
    json_data = open(filename)

    data = json.load(json_data)
    rowLength = len(data['A'][0])
    columnHeight = 5
    # for row in data['A']:
    for i in range(0, rowLength):
        for j in range(0, columnHeight):
            print data['A'][j][i]

        print ""
    json_data.close()


if __name__ == '__main__':
    main()