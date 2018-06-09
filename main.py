from Tkinter import *
import os
import appconfig as conf

class Application(Frame):
    
    playStates = {"looping": False}
    buttons = {}

    def say_hi(self, someText):
        print "hi there, everyone!", someText
    
    def load(self):
        print "loading sounds into PD.."
        command = ""
        for k in conf.SensorNames:
            v = conf.SensorNames[k]
            command += v + " load ../media/loops1/" + v.replace(" ", "") + ".wav,"
        print "command: "+command
        self.sendToPd(command)
    
    def playAll(self):
        if(self.playStates.get("looping")):
            self.sendToPd("loop stop")    
        else:
            self.sendToPd("loop start 60") 
        self.playStates["looping"] = not self.playStates["looping"]   
        
    def buttonPress(self, sensorName):
        command = sensorName
        if(self.playStates.get(sensorName)):
            self.playStates[sensorName] = False
            command += " volume 0"
        else:
            self.playStates[sensorName] = True
            command += " volume 1"
        color = 'black' if self.playStates.get(sensorName) else 'white'
        self.buttons[sensorName].configure(highlightbackground=color)
        return command
        
    def sendToPd(self, command):
        print("sending command to PD: "+command)
        os.system("echo '" + command + "' | "+conf.SystemSettings["pdSendPath"]+" 3000 localhost udp")

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
        
        for c in range(len(cols)):
            for r in range(len(rows)):
                button = Button(self)
                sensorName = str(rows[r])+" "+str(cols[c])
                button["text"] = sensorName
                button["command"] = lambda sn=sensorName:self.sendToPd(self.buttonPress(sn))
                button.grid(row=r, column=c)
                self.buttons[sensorName] = button
                
        self.loadButton = Button(self, text="Load", command=self.load)
        self.loadButton.grid(row=5, column=0, columnspan=2)

        self.playAllButton = Button(self, text="PlayAll", command=self.playAll)
        self.playAllButton.grid(row=5, column=2, columnspan=2)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
