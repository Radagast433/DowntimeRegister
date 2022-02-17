# -*- coding: utf-8 -*-
"""
Created on Thu May 13 02:50:07 2021

@author: Equipo
"""

from tkinter import *
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import subprocess
import threading
import ctypes
import time
import matplotlib.transforms as transforms

class PingLiveGraph():

    def __init__(self):
        self.root = Tk()
        self.root.geometry('1200x700+200+100')
        self.root.title('Live Ping Graph')
        #self.root.iconphoto(False, PhotoImage(file = 'Icons/LPG.png'))
        self.root.state('zoomed')
        self.root.config(background='#fafafa')

        style.use('ggplot')
        self.fig = plt.figure(figsize=(14, 6), dpi=100)
        #fig = plt.figure(figsize = (15, 5), dpi = 100)
        self.ax1 = self.fig.add_subplot(1, 1, 1)
        self.ax1.axhline(y=9.36, color='g', linestyle='-', label = 'Ping Promedio Red: LaRosa')
        self.ax1.legend()
        #ax1.set_ylim(0, 100)
        #line, = ax1.plot(x, y, 'r', marker='o')
        #ser = serial.Serial('com3', 9600)

        plt.xlabel('Tiempo Transcurrido (s)')
        plt.ylabel('Ping (ms)')
        plt.title("Ping (www.google.com)")

        self.i = 0
        self.PAUSE = False
        self.connected_ssid = ''
        self.data = []

        self.GET_NETWORK_NAME()

        self.plotcanvas = FigureCanvasTkAgg(self.fig, self.root)
        self.plotcanvas.get_tk_widget().grid(column=1, row=1)
        #self.ani = animation.FuncAnimation(self.fig, self.animate(), interval=1000)

        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

        self.root.mainloop()

    def GET_NETWORK_NAME(self):

        self.connected_ssid = str(subprocess.check_output("netsh wlan show interfaces")).strip()
        self.start_point = self.connected_ssid.find('SSID                   : ')
        self.end_point = self.connected_ssid.find('BSSID')
        
        self.connected_ssid = self.connected_ssid[self.start_point + 25 : self.end_point - 8]
        
        #return self.connected_ssid

    def ANIMATION(self):
    
        if not self.PAUSE:
        
            self.data = pd.read_csv('Data/' + self.connected_ssid + '_' + 'ping_data.csv', index_col = None)
            
            self.x = self.data['Tiempo_Transcurrido_(s)']
            self.y = self.data['Ping_(ms)']
            
            print(self.x)
            print(self.y)

            line, = self.ax1.plot(self.x, self.y, 'b', marker='o')
            
            line.set_data(self.x, self.y)
            #ax1.set_ylim(min(y) - 15, max(y) + 15, 10.0)
            
            self.ax1.set_ylim(0 - 5, max(self.y) + 15, 10.0)
            self.ax1.plot(self.x, self.y, linewidth = 0.3)
            self.ax1.set_xlim(max(1, self.x.iloc[-1] - 50), self.x.iloc[-1] + 50, 30)
            
            if self.x.iloc[-1] == self.x.iloc[-2]:
                
                self.PAUSE = True
                
            elif self.x.iloc[-1] != self.x.iloc[-2]:
                
                self.PAUSE = False
            
            self.i+= 1

            time.sleep(1)

    def ANIMATE(self):

        animation_thread = threading.Thread(name = 'LivePingGraphThread', target = self.ANIMATION(), daemon=True)
        animation_thread.start()

        #self.ani = animation.FuncAnimation(self.fig, self.ANIMATION(), interval=1000)

''' 
root = Tk()
root.geometry('1200x700+200+100')
root.title('Live Ping Graph')
root.iconphoto(False, PhotoImage(file = 'Icons/LPG.png'))
root.state('zoomed')
root.config(background='#fafafa')

style.use('ggplot')
fig = plt.figure(figsize=(14, 6), dpi=100)
#fig = plt.figure(figsize = (15, 5), dpi = 100)
ax1 = fig.add_subplot(1, 1, 1)
ax1.axhline(y=9.36, color='g', linestyle='-', label = 'Ping Promedio Red: LaRosa')
ax1.legend()
#ax1.set_ylim(0, 100)
#line, = ax1.plot(x, y, 'r', marker='o')
#ser = serial.Serial('com3', 9600)

plt.xlabel('Tiempo Transcurrido (s)')
plt.ylabel('Ping (ms)')
plt.title("Ping (www.google.com)")

i = 0
PAUSE = False

plotcanvas = FigureCanvasTkAgg(fig, root)
plotcanvas.get_tk_widget().grid(column=1, row=1)
ani = animation.FuncAnimation(fig, animate,fargs = (i), interval=1000)

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

root.mainloop()
'''