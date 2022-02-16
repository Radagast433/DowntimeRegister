# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 14:48:49 2022

@author: Sebafu
"""

import pandas as pd
import numpy as np
import speedtest
from datetime import datetime, timedelta
import time
import csv
import os

#import tkinter as tk
from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext

import threading
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
from win32api import GetSystemMetrics
#import matplotlib.ticker as ticker
    
def THREAD_BEGIN(log_box):
    
    log_box.insert(tk.END, ' Iniciando...')
    
    t1 = threading.Thread(name = 'connection', target = CHECK_SPEED, daemon=False, args=(log_box,))
    t1.start()
    
    #CHECK_PINGS()
    
def THREAD_STOP(log_box):
    
    global TESTING
    
    TESTING = False
    
    log_box.insert(tk.END, ' \n\nMonitoreo de velocidad detenido exitosamente...')
    log_box.see("end")

    
def EXIT_APP(root):
    
    global TESTING
    
    if TESTING:
        
        TESTING = False
    
    root.destroy()
    
def CHECK_SPEED(log_box):
        
        a = time.time()
    
        while TESTING:
            
            b = time.time()
            
            if round((b - a), 0) % 60 == 0:
                
                fecha = datetime.now().strftime("%d-%m-%Y")
                hora = datetime.now().strftime("%H:%M:%S")
                downspeed = round((round(s.download()) / 1048576), 2)
                upspeed = round((round(s.upload()) / 1048576), 2)
                
                info = {
                    'Fecha' : fecha,
                    'Hora' : hora,
                    'Velocidad_Bajada' : downspeed,
                    'Velocidad_Subida' : upspeed
                    }
                
                with open('Data/speed_data.csv', mode='a', newline='') as speedcsv:
                    
                    csv_writer = csv.DictWriter(speedcsv, fieldnames = speed_test_results_fieldnames)
                    csv_writer.writerow(info)
                
                log_box.insert(tk.END, f"\n Fecha: {time_now}, bajada: {downspeed} Mb/s, Subida: {upspeed} Mb/s")
                log_box.see("end")
                #print(f"Fecha: {time_now}, bajada: {downspeed} Mb/s, Subida: {upspeed} Mb/s")
            
            #time.sleep(60)
            
#def CHECK_PINGS():
    
    #s.get_servers(servers)
    #print(s.results.ping)
            
class GRAPH_LABEL():
    
    def __init__(self):
        
        self.frame = Toplevel()
        
        self.icon = Image.open('Graphs/speed_graph.png')
        self.icon = self.icon.resize((GetSystemMetrics(0) - 50, GetSystemMetrics(1) - 100))
        self.img = ImageTk.PhotoImage(self.icon)
        
        #self.img = ttk.PhotoImage(file = 'Graphs/test_graph.png')
        self.graph_label = ttk.Label(self.frame, image = self.img)
        self.graph_label.image = self.img
        self.graph_label.pack()
        
            
def SHOW_GRAPH():
    
    #frame = ttk.Toplevel()
    
    global TESTING
    
    if TESTING:
        
        TESTING = False
        
    data = pd.read_csv('Data/speed_data.csv', index_col = None)
    
    times = data['Tiempo']
    download = data['Velocidad_Bajada']
    upload = data['Velocidad_Subida']
        
    plt.figure(figsize = (50, 15))
    plt.xlabel('Tiempo')
    plt.ylabel('Velocidad en Mb/s')
    plt.title("Velocidad Internet")
    plt.margins(0)
    plt.xticks(rotation=30, ha="right")
    plt.plot(times, download, label='Bajada', color='r')
    plt.plot(times, upload, label='Subida', color='b')
    plt.legend()
    plt.savefig('Graphs/speed_graph.png', bbox_inches='tight', dpi = 300)
    #plt.show()
    
    GRAPH_LABEL()
    
    '''
    img = ttk.PhotoImage(file = 'Graphs/test_graph.png')
    graph_label = ttk.Label(frame, image = img)
    graph_label.pack()
    '''
        
def GUI():
    
    root = Tk()
    root.title("Connection Uptime")
    #root.geometry('300x300')
    
    ########## Frame levels ##############
    
    ###### Level 1 ######
    
    level1_1 = ttk.Frame(root)
    level1_1.pack(side = 'top')
    
    level1_2 = ttk.Frame(root)
    level1_2.pack(side = 'top')
    
    level1_3 = ttk.Frame(root)
    level1_3.pack(side = 'top')
    
    ################## Frame 1 ##########################
    
    label_1 = ttk.Label(level1_1)
    label_1.pack(side = 'left')
    
    begin_button = ttk.Button(level1_1, text= 'Iniciar', command=lambda:THREAD_BEGIN(log_box))
    begin_button.pack(side = 'left')
    
    label_2 = ttk.Label(level1_1)
    label_2.pack(side = 'left')
    
    stop_button = ttk.Button(level1_1, text= 'Detener', command=lambda:THREAD_STOP(log_box))
    stop_button.pack(side = 'left')
    
    label_3 = ttk.Label(level1_1)
    label_3.pack(side = 'left')
    
    graph_button = ttk.Button(level1_1, text= 'Mostrar Grafico', command=lambda:SHOW_GRAPH())
    graph_button.pack(side = 'left')
    
    label_4 = ttk.Label(level1_1)
    label_4.pack(side = 'left')
    
    exit_button = ttk.Button(level1_1, text= 'Salir', command=lambda:EXIT_APP(root))
    exit_button.pack(side = 'left')
    
    label_5 = ttk.Label(level1_1)
    label_5.pack(side = 'left')
    
    ################## Frame 2 ##################
    
    label_6 = ttk.Label(level1_2, text = 'log')
    label_6.pack(side = 'top')
    
    ################## Frame 3 ##################
    
    log_box = scrolledtext.ScrolledText(level1_3, wrap="word", height = int(GetSystemMetrics(1) // 72), width = int(GetSystemMetrics(0) // 27.4))
    log_box.pack(side = 'top')
    
    root.mainloop()
    
if __name__ == '__main__':
    
    s = speedtest.Speedtest()
    best_sv = s.get_best_server()
    
    for key in best_sv:
        print(key, ' : ', best_sv[key])
    
    TESTING = True
    
    #servers = ['www.google.com', 'www.emol.cl', 'www.bcentral.cl']
    servers = []
    
    speed_test_results_fieldnames = ['Fecha', 'Hora', 'Velocidad_Bajada', 'Velocidad_Subida']
    
    if not os.path.exists('Data/speed_data.csv'):
    
        with open('Data/speed_data.csv', 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
            csv_writer.writeheader()
    
    plt.rc('xtick', labelsize = 5)
    
    GUI()