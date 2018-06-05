#!/usr/bin/env python

__author__ = "Lukas Gartlehner"
__copyright__ = "Lukas Gartlehner"
__version__ = "0.1"
__email__ = "l.gartlehner@gmx.at"
__status__ = "Development"

# ---------------------------------------------------
# Standard Libs
import os
import wave
import sys

# ---------------------------------------------------
# 3rd Party Libs (install with pip)


class MyPlugin():

    def __init__(self, cb):
        
        self.mqtt_callback = cb
        self.path = os.path.dirname(os.path.abspath(__file__)).replace("\plugins", "\media")
        command = ""
        for ...
            command += "l A 1 ../media/soundset1/A1.wav,"

        os.system("echo '" + command + "' | /Applications/Pd-0.48-1.app/Contents/Resources/bin/pdsend 3000 localhost udp")


    def update(self, gridModel, sensorName):
        os.system("echo 'p " + sensorName + "' | /Applications/Pd-0.48-1.app/Contents/Resources/bin/pdsend 3000 localhost udp")

        self.mqtt_callback("HELLO - PLUGIN 1 is calling back ")


