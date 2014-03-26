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

animation = []
xlen=9
ylen=8
alphabet=[]

def load():
    a = parse_letters(alphabet_json_file)
    if len(alphabet) > 0:
        del alphabet[:]
    for y in range(0,len(a)):
        alphabet.append(a[y])
    populateGrid()

def set_animation(animstring,color,bgcolor):
    print "set_animation(" + animstring+","+color +","+bgcolor+")"
    anim = []
    #
    # frame=[]
    # for x in xlen:
    #     for y in ylen:
    anim.append(get_background_frame(bgcolor))
    anim.append(get_background_frame(bgcolor))


    left_shift(get_background_frame(bgcolor),animstring,color)


    anim.append(get_background_frame(bgcolor))
    anim.append(get_background_frame(bgcolor))
    anim.append(get_background_frame(bgcolor))
    anim.append(get_background_frame(bgcolor))
    anim.append(get_background_frame(bgcolor))
    clear_all()
    if len(animation) > 0:
        del animation[:]

    for y in range(0,len(anim)):
        animation.append(anim[y])

    while 1:
        show_animation(animation)

def left_shift(startframe,animstring,color):
    anim = []
    initframe = startframe
    letters = []
    # for letter in animstring:
    #     letters.append(alphabet[letter])
    letters.append(alphabet) #A
    for num in range(0,len(letters[0])):
        nextframe = shift_one_left(initframe)
        for y in range(0,ylen):
            if (y>1&y<7):
                nextframe[xlen-1][y]=letters[num][y-2]
        anim.append(nextframe)
    animation.append(anim)







    #
    #
    # framenumber = 0
    # for row in range (0,ylen):
    #     for col in range (0, xlen):
    #         if (y>1&y<7):


def shift_one_left(list):
    newlist=[]
    for row in range(0,ylen):
        innerlist = list[row]
        newlist.append(innerlist[1:])
    return newlist

def get_background_frame(bgcolor):
    frame=[]
    for x in range(0,ylen):
        tmp = []
        for y in range(0,xlen):
            tmp.append(hex_to_rgb(bgcolor))
        frame.append(tmp)
    frame.reverse()
    return frame

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
        for row in range(0, ylen):
            for col in range(0, xlen):
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
            var = data['A'][j][i]

    json_data.close()
    return data['A']

# if __name__ == '__main__':
#     main()