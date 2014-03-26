

import json
from time import sleep
from LedStrip_WS2801 import *
import grid
import threading
from os import listdir
from os.path import isfile, join
from flask import Flask, render_template, request


app = Flask(__name__)
ledStrip = LedStrip_WS2801(75)
thread = None


class RunAnimation(threading.Thread):
    def __init__(self, data, msperframe):
        super(RunAnimation, self).__init__()
        self.data = data
        self.msperframe = msperframe
        self.stop = 0

    def run(self):
        print("running thread")
        while not self.stop:
            for frames in self.data:
                for row in range(0, 8):
                    for col in range(0, 9):
                        gridnr = grid.grid[row][col]
                        animnr = frames[(9*row)+col]
                        ledStrip.setPixel(gridnr, animnr)
                ledStrip.update()
                sleep(self.msperframe)

    def stop(self):
        self.stop = 1


def main():
    grid.populateGrid()
    print "App running on 0.0.0.0:5000"
    app.debug = True
    app.run(host='0.0.0.0')



@app.route("/api/animation")
def animation_html():
    return render_template("animation.html")


#json example: {frames:[0:[0:'rgb',1:'rgb',2:'rgb',3:'rgb'},1:{0:'rgb',1:'rgb',2:'rgb',3:'rgb'}],config{fps:float}}
@app.route("/api/runanimation")
def runanimation():
    jdata = request.args.get('jdata', '')
    global thread
    #Read json
    #jdata = request.form["jdata"]
    if thread is not None:
        thread.stop()

    json_data = open(jdata)
    data = json.load(json_data)
    json_data.close()
    msperframe = 1000/data.config.fps

    thread = RunAnimation(data, msperframe)
    thread.start()

@app.route("/api/animation_save")
def animation_save(name,jdata):
    myFile = open('json/'+name+'.json', 'w')
    myFile.write(jdata)
    myFile.close()

@app.route("/api/animation_load")
def animation_load(name):
    myFile = open('json/'+name+'.json', 'r')
    jdata = myFile.read()
    myFile.close()
    return jdata

@app.route("/api/animation_list")
def animation_run():

    files = [f for f in listdir('json/') if isfile(join('/json/', f))]
    return files

if __name__ == '__main__':
    print "Now running main"
    main()