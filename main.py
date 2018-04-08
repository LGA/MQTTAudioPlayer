from glob import glob
from os.path import dirname, join, basename

import json

import paho.mqtt.client as mqtt

import time
import numpy
import sys


class AudioApp():

    appStatus = ''
    processBar =  '<<==>>                               '
    processBarLeft = True
    zones = {'Zone1': 0, 'Zone2': 0, 'Zone3': 0, 'Zone4': 0}

    def build(self):

        # Start MQTT Subscription
        self.broker_settings = {'address': '192.168.0.28', 'topic': 'sensorHit', 'client': 'Luke'}

        self.client = mqtt.Client(self.broker_settings['client'])
        self.client.connect(self.broker_settings['address'], 1883)
        self.client.subscribe(self.broker_settings['topic'])
        self.client.on_message=self.on_message
        self.client.loop_start()

        print("Waiting for MQTT Input")
        print(self.broker_settings)
        print('')

        # Build 5x5 numpy grids
        self.gridModel = numpy.zeros((5, 5), dtype=numpy.int8)
        self.gridSubtract = (numpy.ones((5, 5), dtype=numpy.int8))*3
        self.drawGrid(False)

        


    def on_message(self, client, userdata, message):

        '''
        Callback for MQTT messages
        Reads a value for x/y coordinate and writes it in to numpy matrix

        Example JSON

        {"x": 1, "y": 1, "v": 100}
        '''

        val = json.loads(str(message.payload.decode("utf-8")))    

        try:
            x = val['x']
            y = val['y']
            v = int(val['v'])

            self.gridModel[y,x] = v
            self.appStatus = 'Added ' + str(message.payload.decode("utf-8"))
        except:
            self.appStatus = 'Could not digest ' + str(message.payload.decode("utf-8"))



    def drawGrid(self, removePrevOut=True):

        '''
        Draws out the [5x5] array to print
        '''

        if removePrevOut:
            for x in range (0,11):
                sys.stdout.write("\033[F") #back to previous line
                sys.stdout.write("\033[K") #clear line

        

        if len(self.appStatus) > 0:
            print(str(self.appStatus).replace('\n', ' ').replace('\r', ''))
            self.appStatus=''

        bar = self.updateProcessBar()
        print(bar)

        for row in self.gridModel:
            rowToStr = ''
            for cell in row:
                rowToStr += " [" + str(cell).zfill(3) + "] "
            print(rowToStr)

        print(bar)
        self.gridModel = numpy.clip(self.gridModel - self.gridSubtract, 0, 100)


        self.zones['Zone1'] = numpy.average(self.gridModel[:3,:3])
        self.zones['Zone2'] = numpy.average(self.gridModel[:3,2:])
        self.zones['Zone3'] = numpy.average(self.gridModel[2:,:3])
        self.zones['Zone4'] = numpy.average(self.gridModel[2:,2:])

        for x,y in self.zones.iteritems():
            print(x + ': ' + str(round(y,2)))


    def updateProcessBar(self):
        '''
        Super-Nice bash process bar
        '''
        if self.processBar[0]=='<':
            self.processBarLeft=True

        if self.processBar[-1]=='>':
            self.processBarLeft=False

        if self.processBarLeft:
            self.processBar = self.processBar[-1] + self.processBar[:-1]
        else:
            self.processBar = self.processBar[1:] + self.processBar[0]


        return "[" + self.processBar + "]"


    def run(self):
        self.build()

        while True:
            time.sleep(0.2)
            self.drawGrid()




if __name__ == '__main__':
    AudioApp().run()
