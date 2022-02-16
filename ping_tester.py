# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 10:46:05 2022

@author: Sebafu
"""

import os
import csv
import time
import pandas as pd
import numpy as np
import datetime
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import threading

from PIL import ImageTk, Image
from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from win32api import GetSystemMetrics
    
def monitor(log_box):
    
    global elapsed_time
    global acc_time
    
    #delta = 0
    
    cut_time = 0
    back_online_time = 0
    
    cut_duration = 0
    cut_detector = False
    
    while RUNNING:
        
        back_online_time = datetime.datetime.now()
        
        ping = os.popen('ping www.google.com -n 1')
        
        #print(ping)
        
        if cut_detector:
            
            cut_duration = cut_time - back_online_time
            cut_duration = cut_duration.microseconds
            cut_duration = cut_duration * 10**(-3)
            acc_time+= cut_duration
            
            #print(cut_duration)
            
            cut_detector = False
        
        result = ping.readlines()
        packet_loss = result[6].strip()
        packet_loss = packet_loss[1:3]
        msLine = result[-1].strip()
    
        total_ms = msLine[len(msLine) - 4: len(msLine) - 2]
            
        if total_ms == 'os':
            
            cut_time = datetime.datetime.now()
            
            total_ms = 0
            cut_detector = True
            
        #cut_duration = cut_duration.microseconds
        #cut_duration = cut_duration * 10**(-3)
        #acc_time+= cut_duration
            
        a = datetime.datetime.now().strftime("%d-%m-%Y")
        
        b = datetime.datetime.now().strftime("%H-%M-%S")
        
        c = round(elapsed_time, 1)
        
        d = int(total_ms)
        
        e = packet_loss
        
        f = round(cut_duration, 2)
        
        g = acc_time
            
        info = {
            'Fecha' : a,
            'Hora' : b,
            'Tiempo_Transcurrido_(s)' : c,
            'Ping_(ms)' : d,
            '%_Paquetes_perdidos' : e,
            'Tiempo_Corte_(ms)' : f,
            'Tiempo_de_Fallo_Acumulado_(ms)' : g
            }

        
        with open('Data/ping_data.csv', 'a', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
        
            csv_writer.writerow(info)
        
        log_box.insert(tk.END, f"\n\n Fecha: {a}, Hora: {b}, Tiempo_Transcurrido_(s): {c}, Ping_(ms): {d}, %_Paquetes_perdidos: {e}, Tiempo_Corte_(ms): {f}, 'Tiempo_de_Fallo_Acumulado_(ms): {g}")
        log_box.see("end")
        
        cut_duration = 0
        
        elapsed_time+= scan_interval
        time.sleep(scan_interval)
        
def GET_JITTER(ping_data):
    
    aux = 0
    dif_sum = 0
    
    if ping_data.size < 3:
        
        return 0.0
    
    else:
    
        for i in range(1, ping_data.size):
            
            if ping_data[i] > 0:
                
                aux = ping_data[i] - ping_data[i - 1]
                
                if aux < 0:
                    
                    aux*= (-1)
        
                dif_sum+= aux
        
        return round(dif_sum / (ping_data[ping_data > 0].count() - 1), 2)
        
            
def THREAD_BEGIN(log_box):
    
    log_box.insert(tk.END, ' Iniciando...')
    
    t1 = threading.Thread(name = 'ping', target = monitor, daemon=False, args=(log_box,))
    
    t1.start()
    

def THREAD_STOP(log_box):
    
    global RUNNING
    
    RUNNING = False
    
    log_box.insert(tk.END, ' \n\nMonitoreo de Ping detenido exitosamente...')
    log_box.see("end")
    
    data = pd.read_csv('Data/ping_data.csv', index_col = None)
    
    ping_data = data['Ping_(ms)']
    
    log_box.insert(tk.END, ' \n\nJitter: ' + str(GET_JITTER(ping_data)))
    log_box.see("end")
    

class GRAPH_LABEL():
    
    def __init__(self):
        
        self.frame = Toplevel()
        
        self.icon = Image.open('Graphs/ping_graph.png')
        self.icon = self.icon.resize((GetSystemMetrics(0) - 50, GetSystemMetrics(1) - 100))
        self.img = ImageTk.PhotoImage(self.icon)
        
        #self.img = ttk.PhotoImage(file = 'Graphs/test_graph.png')
        self.graph_label = ttk.Label(self.frame, image = self.img)
        self.graph_label.image = self.img
        self.graph_label.pack()
    

def SHOW_GRAPH():

    data = pd.read_csv('Data/ping_data.csv', index_col = None)
    
    #print(data)
    
    x = data['Tiempo_Transcurrido_(s)']
    y = data['Ping_(ms)']
    
    #print(x)
    #print(y)
    
    #print(' Tiempo total de cortes (ms): ', data['Tiempo_de_Fallo_Acumulado_(ms)'].iloc[-1], '\n Cantidad de cortes: ', (data['Ping_(ms)'].values == 0).sum(), '\n Tiempo total de monitoreo (s): ', data['Tiempo_Transcurrido_(s)'].iloc[-1])
    plt.figure(figsize = (50, 15))
    #plt.plot(x, y, label='download', color='r')
    #plt.scatter(x, y)
    
    plt.margins(0)
    plt.plot(x, y, linewidth = 0.5)
    
    plt.xticks(np.arange(0, max(x) + 1, 10.0))
    
    plt.yticks(np.arange(min(y) - 5, max(y) + 5, 5.0))
    
    plt.xlabel('Tiempo Transcurrido (s)')
    plt.ylabel('Ping (ms)')
    plt.title("Ping (www.google.com)")
    #plt.legend()
    plt.savefig('Graphs/ping_graph.png', bbox_inches='tight', dpi = 300)
    
    GRAPH_LABEL()

'''
def SHOW_LIVE_GRAPH():
    
    data = pd.read_csv('Data/ping_data.csv', index_col = None)
    
    x = data['Tiempo_Transcurrido_(s)']
    y = data['Ping_(ms)']
    
    plt.margins(0)
    
    plt.cla()
    #plt.figure(figsize = (50, 15))
    plt.plot(x, y, linewidth = 0.5)
    
    plt.xticks(np.arange(0, max(x) + 1, 10.0))
    plt.yticks(np.arange(min(y) - 5, max(y) + 5, 5.0))
    
    plt.xlabel('Tiempo Transcurrido (s)')
    plt.ylabel('Ping (ms)')
    plt.title("Ping (www.google.com)")
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
'''

def SHOW_LIVE_GRAPH(ax, right_frame, fig):
        
    data = pd.read_csv('Data/ping_data.csv', index_col = None)
    
    x = data['Tiempo_Transcurrido_(s)']
    y = data['Ping_(ms)']
    
    ax.clear()
    ax.plot(x, y, linewidth = 0.5)
    
    plt.xticks(np.arange(0, max(x) + 1, 10.0))
    plt.yticks(np.arange(min(y) - 5, max(y) + 5, 5.0))
    
    plot = FigureCanvasTkAgg(fig, right_frame) 
    plot.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    
    plt.xlabel('Tiempo Transcurrido (s)')
    plt.ylabel('Ping (ms)')
    plt.title("Ping (www.google.com)")
    plt.tight_layout()
    

def INITIALIZE_LIVE_GRAPH():
    
    global ani
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    ani = FuncAnimation(fig, SHOW_LIVE_GRAPH, fargs=(ax),interval=1000)
    
    fig.show()
    
def GRAPH_THREAD():
    
    if RUNNING:
    
        t2 = threading.Thread(name = 'pinggraph', target = INITIALIZE_LIVE_GRAPH, daemon=False)
        
        t2.start()
    
def EXIT_APP(root):
    
    global RUNNING
    
    if RUNNING:
        
        RUNNING = False
    
    root.destroy()
    
            
def GUI():
    
    root = Tk()
    root.title("Connection monitor")
    #root.geometry('300x300')
    
    ########## Frame levels ##############
    
    ##### Level 1 #####
    
    left_frame = ttk.Frame(root)
    left_frame.pack(side = 'left')
    
    right_frame = ttk.Frame(root)
    right_frame.pack(side = 'right')
    
    ##### Level 2 Left #####
    
    level2L_1 = ttk.Frame(left_frame)
    level2L_1.pack(side = 'top')
    
    level2L_2 = ttk.Frame(left_frame)
    level2L_2.pack(side = 'top')
    
    level2L_3 = ttk.Frame(left_frame)
    level2L_3.pack(side = 'top')
    
    ##### Level 2 Right #####
    
    level2R_1 = ttk.Frame(left_frame)
    level2R_1.pack(side = 'top')
    
    level2R_2 = ttk.Frame(left_frame)
    level2R_2.pack(side = 'top')
    
    ################## Frame 1 ##########################
    
    label_1 = ttk.Label(level2L_1)
    label_1.pack(side = 'left')
    
    begin_button = ttk.Button(level2L_1, text= 'Iniciar', command=lambda:THREAD_BEGIN(log_box))
    begin_button.pack(side = 'left')
    
    label_2 = ttk.Label(level2L_1)
    label_2.pack(side = 'left')
    
    stop_button = ttk.Button(level2L_1, text= 'Detener', command=lambda:THREAD_STOP(log_box))
    stop_button.pack(side = 'left')
    
    label_3 = ttk.Label(level2L_1)
    label_3.pack(side = 'left')
    
    graph_button = ttk.Button(level2L_1, text= 'Mostrar Grafico', command=lambda:SHOW_GRAPH())
    graph_button.pack(side = 'left')
    
    label_4 = ttk.Label(level2L_1)
    label_4.pack(side = 'left')
    
    #live_graph_button = ttk.Button(level2L_1, text= 'Mostrar Grafico en Vivo', command=lambda:GRAPH_THREAD())
    #live_graph_button.pack(side = 'left')
    
    label_5 = ttk.Label(level2L_1)
    label_5.pack(side = 'left')
    
    exit_button = ttk.Button(level2L_1, text= 'Salir', command=lambda:EXIT_APP(root))
    exit_button.pack(side = 'left')
    
    label_6 = ttk.Label(level2L_1)
    label_6.pack(side = 'left')
    
    ################## Frame 2 ##################
    
    label_7 = ttk.Label(level2L_2, text = 'log')
    label_7.pack(side = 'top')
    
    ################## Frame 3 ##################
    
    log_box = scrolledtext.ScrolledText(level2L_3, wrap="word", height = int(GetSystemMetrics(1) // 72), width = int(GetSystemMetrics(0) // 27.4))
    log_box.pack(side = 'top')
    
    root.mainloop()
    

if __name__ == '__main__':
    
    scan_interval = 1 # seconds
    
    ani = None
    
    elapsed_time = 0
    
    acc_time = 0
    
    RUNNING = True
    
    plt.style.use('fivethirtyeight')
    #plt.rcParams['animation.html'] = 'jshtml'
    
    #fieldnames = ['Fecha', 'Tiempo_Transcurrido', 'Ping', 'Tiempo_de_Fallo_Acumulado']  # agregar tiempo de corte
    fieldnames = ['Fecha', 'Hora', 'Tiempo_Transcurrido_(s)', 'Ping_(ms)', '%_Paquetes_perdidos', 'Tiempo_Corte_(ms)', 'Tiempo_de_Fallo_Acumulado_(ms)']
    
    if not os.path.exists('Data/ping_data.csv'):
    
        with open('Data/ping_data.csv', 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
            csv_writer.writeheader()
    
    GUI()
    #monitor() 