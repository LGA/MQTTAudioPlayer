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



    def update(self, g):
        
        # callback
        
        self.mqtt_callback("HELLO - PLUGIN 1 is calling back ")


