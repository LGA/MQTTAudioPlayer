#!/usr/bin/env python

"""
Receives MQTT Messages, maps sensor names to coordinates,
stores sensor status & connects to plugins

Sources:
[Plugin Mechanism]      https://codereview.stackexchange.com/questions/2892/minimal-python-plugin-mechanism
[Dynamic Imports]       https://www.blog.pythonlibrary.org/2012/07/31/advanced-python-how-to-dynamically-load-modules-or-classes/
[Threading]             http://sebastiandahlgren.se/2014/06/27/running-a-method-as-a-background-thread-in-python/
"""

__author__ = "Lukas Gartlehner"
__copyright__ = "Lukas Gartlehner"
__version__ = "0.1"
__email__ = "l.gartlehner@gmx.at"
__status__ = "Development"

# ---------------------------------------------------
# Standard Libs
from glob import glob
import os.path
import time
import sys
import json
import pkgutil
from threading import Thread

# ---------------------------------------------------
# 3rd Party Libs (install with pip)
import numpy
import paho.mqtt.client as mqtt

# ---------------------------------------------------
# Custom Modules
import appconfig as conf
import plugins




class AudioApp():

    processBar =  '<<==>>                               '
    processBarLeft = True
    seperator = "-----------------------------------------"
    printVal = []
    activePlugin = ''
    userInput = ''
    printedLines = 0
    appRunning=True

    def build(self):
        
        # init mqtt
        self.client = mqtt.Client(conf.brokerSettings['client'])
        self.client.connect(conf.brokerSettings['address'], conf.brokerSettings['port'])

        # wait for MQTT connection
        # TODO: implement proper callback https://www.eclipse.org/paho/clients/python/docs/
        #       with error handling on failed connection
        time.sleep(0.5)

        self.client.subscribe(conf.brokerSettings['topic'])

        # setup callback
        self.client.on_message=self.on_message
        self.client.loop_start()

        print("MQTT Config: " + str(conf.brokerSettings))
        print('')

        # Build 5x5 numpy grids
        self.gridModel = numpy.zeros((5, 5), dtype=numpy.int16)
        self.gridSubtract = (numpy.ones((5, 5), dtype=numpy.int8))*4 
        
        Thread(target=self.user_input, args=()).start() 
            
        
        self.available_plugins()


        self.drawGrid(False)
        self.use_plugin(0)

          


    def available_plugins(self):
        
        """ Gets all python files from /plugins """

        pluginsPath = os.path.dirname(plugins.__file__)
        pluginModules = [name for _, name, _ in pkgutil.iter_modules([pluginsPath])]
        self.allPlugins = []

        print("Available Plugins:")
        for plugin in pluginModules:
            self.allPlugins.append(plugin)
            print(str(len(self.allPlugins)) + ". " +plugin)
        print(self.seperator)





    def use_plugin(self, pluginNumber):

        """ imports and instantiates a plugin from the list """

        try:
            pluginName ="plugins."+self.allPlugins[pluginNumber]
            __import__(pluginName)
            sys.modules[pluginName]
            self.plugin = sys.modules[pluginName].MoonMelonPlugin(self.on_plugin_receive, conf)
            self.activePlugin = self.allPlugins[pluginNumber]

        except:
            self.print_proxy("Error loading plugin")
        



    def on_plugin_receive(self, payload, topic=conf.brokerSettings['topic']):

        """ Callback for the plugin """

        self.print_proxy(str(payload))

        """
        ->>> uncomment this block to publish payload on MQTT

        payload = json.dumps(payload)
        self.print_proxy("sent payload " + payload)
        self.client.publish(topic, json.dumps(payload))
        """


    def on_message(self, client, userdata, message):

        '''
        Callback for MQTT messages
        {"k": "XXX", "v": 100}
        '''

        val = json.loads(str(message.payload.decode("utf-8")))   

        try:
            sensorId = val['k']
            pos = conf.SensorMapping[sensorId]
            sensorName = conf.SensorNames[sensorId]
            v = int(val['v'])

            self.gridModel[pos] = v
            self.print_proxy('Added ' + str(message.payload.decode("utf-8")))

            #Thread(target=self.plugin.update, args=(self.gridModel, sensorName)).start() 
            self.plugin.update(self.gridModel, sensorName)

        except:
            self.print_proxy('Could not digest ' + str(message.payload.decode("utf-8")))



    def drawGrid(self, removePrevOut=True):

        '''
        Pseudo-GUI for status overview
        Draws out the [5x5] array and prints user-input and app-status to bash
        '''

        # delete previous outputs from bash
        if removePrevOut:
            for x in range (0,9):
                sys.stdout.write("\033[F") #back to previous line
                sys.stdout.write("\033[K") #clear line

        # check user-input
        if self.userInput != '':

            if (self.userInput == 'c'):
                self.clear_printed_lines()

            elif (self.userInput == 'x'):
                self.appRunning=False
                sys.exit()

            else:
                self.print_proxy("Command: " + str(self.userInput))
                try:
                    self.use_plugin(int(self.userInput)-1)
                except ValueError as ex:
                    self.print_proxy("Invalid command sequence")
                self.userInput='' 


        # send all collected std-out to bash
        for line in self.printVal:
            print(line)
        self.printVal = []

        print(self.seperator)

        # pseudo-GUI
        self.processBar, self.processBarLeft = self.updateProcessBar(self.processBar, self.processBarLeft)
        print("[",self.processBar,"]")

        for row in self.gridModel:
            rowToStr = ''
            for cell in row: 
                rowToStr += " [" + str(cell).zfill(3) + "] "
            print(rowToStr)

        print("[",self.processBar,"]")
        print("Using Plugin: ", self.activePlugin)

        # subtract from values in the matrix
        self.gridModel = numpy.clip(self.gridModel - self.gridSubtract, 0, 256)



    def print_proxy(self, msg):

        """ use this method instead of print() to keep interactive bash output """
        self.printedLines += 1
        self.printVal.append(str(msg))

    def clear_printed_lines(self):
        for x in range (0,self.printedLines):
            sys.stdout.write("\033[F") #back to previous line
            sys.stdout.write("\033[K") #clear line

        self.printedLines=0


    def updateProcessBar(self, bar, left):
        
        """ Fancy Bash-Processing-Bar """

        bar = bar[-1] + bar[:-1] if left else bar[1:] + bar[0]
        if (bar[0]=='<') or (bar[-1]=='>'): left=(not left)
        
        return bar, left


    def user_input(self):

        """ Wait for user input - start as Thread to allow non-blocking I/O """
        
        while self.appRunning:
            self.userInput = raw_input("")
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")


    def run(self):
        self.build()

        while self.appRunning:
            time.sleep(0.1)
            self.drawGrid()



if __name__ == '__main__':
    AudioApp().run()
