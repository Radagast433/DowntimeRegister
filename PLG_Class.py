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
import ctypes
import matplotlib.transforms as transforms

class PingLiveGraph():

    def __init__(self):
        self.root = Tk()
        self.root.geometry('1200x700+200+100')
        self.root.title('Live Ping Graph')
        self.root.iconphoto(False, PhotoImage(file = 'Icons/LPG.png'))
        self.root.state('zoomed')
        self.root.config(background='#fafafa')

        style.use('ggplot')
        self.fig = plt.figure(figsize=(14, 6), dpi=100)
        #fig = plt.figure(figsize = (15, 5), dpi = 100)
        self.ax1 = fig.add_subplot(1, 1, 1)
        self.ax1.axhline(y=9.36, color='g', linestyle='-', label = 'Ping Promedio Red: LaRosa')
        self.ax1.legend()
        #ax1.set_ylim(0, 100)
        #line, = ax1.plot(x, y, 'r', marker='o')
        #ser = serial.Serial('com3', 9600)

        plt.xlabel('Tiempo Transcurrido (s)')
        plt.ylabel('Ping (ms)')
        plt.title("Ping (www.google.com)")

        self.i = 0
        PAUSE = False

        self.plotcanvas = FigureCanvasTkAgg(self.fig, self.root)
        self.plotcanvas.get_tk_widget().grid(column=1, row=1)
        ani = animation.FuncAnimation(self.fig, self.animate, interval=1000)

        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

        root.mainloop()

def GET_NETWORK_NAME():

    connected_ssid = str(subprocess.check_output("netsh wlan show interfaces")).strip()
    start_point = connected_ssid.find('SSID                   : ')
    end_point = connected_ssid.find('BSSID')
    
    connected_ssid = connected_ssid[start_point + 25 : end_point - 8]
    
    return connected_ssid


def animate(i):
    
    global PAUSE
    #global ax1
    #global i
    
    if not PAUSE:
    
        data = pd.read_csv('Data/' + GET_NETWORK_NAME() + '_' + 'ping_data.csv', index_col = None)
        
        x = data['Tiempo_Transcurrido_(s)']
        y = data['Ping_(ms)']
        
        line, = ax1.plot(x, y, 'b', marker='o')
        
        line.set_data(x, y)
        #ax1.set_ylim(min(y) - 15, max(y) + 15, 10.0)
        
        ax1.set_ylim(0 - 5, max(y) + 15, 10.0)
        ax1.plot(x, y, linewidth = 0.3)
        ax1.set_xlim(max(1, x.iloc[-1] - 50), x.iloc[-1] + 50, 30)
        
        if x.iloc[-1] == x.iloc[-2]:
            
            PAUSE = True
            
        elif x.iloc[-1] != x.iloc[-2]:
            
            PAUSE = False
        
        i+=1

    
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