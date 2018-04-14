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
import pyaudio


class MyPlugin():

    def __init__(self, cb):
        
        self.mqtt_callback = cb
        self.path = os.path.dirname(os.path.abspath(__file__)).replace("\plugins", "\media")


    def update(self, g):
        
        # callback
        
        # Play Audiofile
        
        CHUNK = 1024

        wf = wave.open(self.path + "\A.wav", 'rb')

        p = pyaudio.PyAudio()

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(CHUNK)

        while data != '':
            stream.write(data)
            data = wf.readframes(CHUNK)

        stream.stop_stream()
        stream.close()

        p.terminate()



        self.mqtt_callback("HELLO - PLUGIN 1 is calling back ")


