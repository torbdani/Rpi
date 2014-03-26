__author__ = 'marius'


import json
from time import sleep
from LedStrip_WS2801 import *
import grid
import threading
from os import listdir
from os.path import isfile, join

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
        while not self.stop:
            for frames in self.data:
                for row in range(0, 8):
                    for col in range(0, 9):

                        gridnr = grid.grid[row][col]
                        animnr = frames[row*col]
                        ledStrip.setPixel(gridnr, animnr)
                ledStrip.update()
                sleep(self.msperframe)

    def stop(self):
        self.stop = 1

def main():
    grid.populateGrid()


@app.route("/api/animation")
def animation_html():
    return render_template("animation.html")



#json example: {frames:[0:{rgb,rgb,rgb,rgb},1:{rgb,rgb,rgb,rgb}],config{fps:float}}
@app.route("/api/animation_run")
def animation_run(jdata):
#Read json

    if thread is not None:
        thread.stop()

    json_data = open(jdata)
    data = json.load(json_data)
    json_data.close()

    msperframe = 1000/data.config.fps

    thread = RunAnimation(data,msperframe)
    thread.start()

@app.route("/api/animation_save")
def animation_save(name,jdata):
    myFile = open('/json/'+name+'.json', 'w')
    myFile.write(jdata)
    myFile.close()

@app.route("/api/animation_load")
def animation_load(name):
    myFile = open('/json/'+name+'.json', 'r')
    jdata = myFile.read()
    myFile.close()
    return jdata

@app.route("/api/animation_list")
def animation_run():

    files = [f for f in listdir('/json/') if isfile(join('/json/', f))]
    return files

main()