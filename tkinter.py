from Tkinter import *
import os
import appconfig as conf

class Application(Frame):
    def makeFunc(self, x):
        return lambda: x

    def say_hi(self, someText):
        print "hi there, everyone!", someText
    
    def load(self):
        print "loading sounds into PD.."
        command = ""
        for k in conf.SensorNames:
            v = conf.SensorNames[k]
            command += v + " load ../media/loops1/" + v.replace(" ", "") + ".wav,"
        print "command: "+command
        os.system("echo '" + command + "' | /Applications/Pd-0.48-1.app/Contents/Resources/bin/pdsend 3000 localhost udp")

    def sendToPd(self, sensorName):
        print sensorName
        os.system("echo '" + sensorName + " play' | /Applications/Pd-0.48-1.app/Contents/Resources/bin/pdsend 3000 localhost udp")

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        #self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        #self.hi_there.pack({"side": "left"})

        cols = [1, 2, 3, 4, 5]
        rows = ["A", "B", "C", "D", "E"]
        buttons = []
        for c in range(len(cols)):
            for r in range(len(rows)):
                button = Button(self)
                sensorName = str(rows[r])+" "+str(cols[c])
                button["text"] = sensorName
                button["command"] = lambda sn=sensorName:self.sendToPd(sn)
                button.grid(row=r, column=c)
                
        self.loadButton = Button(self, text="Load", command=self.load)
        self.loadButton.grid(row=5, column=0, columnspan=5)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
