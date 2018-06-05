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


class MoonMelonPlugin():

    def __init__(self, cb, conf):
        
        self.mqtt_callback = cb
        self.conf = conf

        self.path = os.path.dirname(os.path.abspath(__file__)).replace("\plugins", "\media")
        command = ""

        for k, v in sorted(conf.SensorNames.iteritems()):
            command += "l " + v + "../media/soundset1/" + v.replace(" ", "") + ".wav,"

        os.system("echo '" + command + "' | /Applications/Pd-0.48-1.app/Contents/Resources/bin/pdsend 3000 localhost udp")


    def update(self, gridModel, sensorName):
        os.system("echo 'p " + sensorName + "' | /Applications/Pd-0.48-1.app/Contents/Resources/bin/pdsend 3000 localhost udp")

        self.mqtt_callback("HELLO - PLUGIN 1 is calling back ")


