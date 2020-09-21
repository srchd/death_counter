import sys, os 
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

from tkinter import *
from win32api import GetSystemMetrics
from pynput.keyboard import KeyCode, Listener, Key
import queue

deaths = 0
filename = 'deaths.txt'
APP_WIDTH = 400
APP_HEIGHT = 400
SCREEN_WIDTH = GetSystemMetrics(0)
addOneKey = KeyCode(char='+')
nullifyKey = KeyCode(char='0')
exitKey = KeyCode(char='e')

with open(filename, 'r') as file:
    
    deaths = int(file.read())

class Deathcounter:
    def __init__(self, w, h, sw, deaths):
        self.callbackID = None
        self.eventqueue = queue.Queue()
        
        self.deaths = deaths
        self.app_width = w
        self.app_height = h
        self.screen_width = sw
        self.res = str(self.app_width) + "x" + str(self.app_height) + "+" + str(self.screen_width - self.app_width) + "+0"
        
        self.root = Tk()
        self.root.overrideredirect(1)
        self.root.attributes("-alpha", 1.0)
        #self.res = str(APP_WIDTH) + "x" + str(APP_HEIGHT) + "+" + str(SCREEN_WIDTH - APP_WIDTH) + "+0"
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.geometry(self.res)
        self.root.config(bg='black')
        self.var = StringVar()
        self.label = Label(self.root, textvariable=self.var, bg='black', font='Courier 40 bold')
        self.label.pack()
        self.label.config(fg='white')
        self.root.attributes("-transparentcolor", "black")
        self.var.set(deaths)
        
        self.listener_thread()
        self.root.after(0, self.update)
        
    def listener_thread(self):
        def on_press(key):
            #print(key)
            if key == addOneKey or key == nullifyKey or key == exitKey:
                self.eventqueue.put_nowait(key)
        listener = Listener(on_press=on_press)
        listener.start()
            
    def update(self):
        try:
            while True:
                key = self.eventqueue.get_nowait()
                self.process_key(key)
        except queue.Empty:
            pass
        self.root.after(100, self.update)
        
    def process_key(self, key):
        if key == addOneKey:
            self.deaths += 1
            self.var.set(self.deaths)
        elif key == nullifyKey:
            self.deaths = 0
            self.var.set(self.deaths)
        elif key == exitKey:
            self.root.destroy()
def main():
    master = Deathcounter(APP_WIDTH, APP_HEIGHT, SCREEN_WIDTH, deaths)
    master.root.mainloop()

    with open(filename, 'w') as file:
        file.write(str(master.deaths))
        
if __name__ == "__main__":
    main()