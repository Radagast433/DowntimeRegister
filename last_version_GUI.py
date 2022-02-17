# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 14:27:24 2022

@author: EmanuelF
"""

from tkinter import ttk
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from win32api import GetSystemMetrics
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import threading
import datetime
import os
import csv
import time
from PIL import ImageTk, Image
import subprocess
import speedtest
import multiprocessing
import ctypes
import psutil
#import pyspeedtest
#import ping_live_graph as plg

'''
class DATE_SELECTION():
    
    def __init__(self, test_type):
        
        self.frame = Toplevel()
        self.frame.geometry("+10+10")
        
        self.lvl2_frame_1 = ttk.Frame(self.frame)
        self.lvl2_frame_1.pack(side = 'top')
        
        self.lvl2_frame_2 = ttk.Frame(self.frame)
        self.lvl2_frame_2.pack(side = 'top')
        
        self.start_date_combobox = ttk.Combobox(self.lvl2_frame_1, state = 'readonly')
        self.start_date_combobox.pack(side = 'left')
        
        self.end_date_combobox = ttk.Combobox(self.lvl2_frame_1, state = 'readonly')
        self.end_date_combobox.pack(side = 'left')
        
        self.ok_button = ttk.Button(self.lvl2_frame_2, text= 'Mostrar', command=lambda:self.SHOW())
        
        if test_type == 'ping':
            
            date_values = pd.read_csv(data_route + GET_NETWORK_NAME() + '_' + ping_csv_route, index_col = None)
            date_values = date_values['Fecha']
            
            self.start_date_combobox['values'] = date_values
            self.start_date_combobox.set(date_values[0])
            
            self.end_date_combobox['values'] = date_values
            self.end_date_combobox.set(date_values[0])
            
        def SHOW(self):
            
            self.frame.destroy()
'''

class GRAPH_LABEL():
    
    def __init__(self, path):
        
        self.frame = Toplevel()
        self.frame.geometry("+10+10")
        
        self.icon = Image.open(path)
        
        #print(path)
        #print(path.find('ping'))
        #print(path.find('speed'))
        #print(path.find('packetloss'))
        
        if path.find('ping') != -1 or path.find('speed') != -1:
            
            self.icon = self.icon.resize((GetSystemMetrics(0) - 50, GetSystemMetrics(1) - 100))
            
        elif path.find('packetloss') != -1:
            
            self.icon = self.icon.resize((GetSystemMetrics(1) + int(GetSystemMetrics(1)//3.2), GetSystemMetrics(1)))
            
        self.img = ImageTk.PhotoImage(self.icon)
        
        #self.img = ttk.PhotoImage(file = 'Graphs/test_graph.png')
        self.graph_label = ttk.Label(self.frame, image = self.img)
        self.graph_label.image = self.img
        self.graph_label.pack()

def GET_NETWORK_NAME():

    connected_ssid = str(subprocess.check_output("netsh wlan show interfaces")).strip()
    start_point = connected_ssid.find('SSID                   : ')
    end_point = connected_ssid.find('BSSID')
    
    connected_ssid = connected_ssid[start_point + 25 : end_point - 8]
    
    if len(connected_ssid) < 30:
    
        return connected_ssid
    
    else:
        
        return 'Ethernet'
        
    
def SELECT_GRAPH(test_type):

    network_name = GET_NETWORK_NAME()
    
    if test_type == 'ping':
    
        data = pd.read_csv(data_route + network_name + '_' + ping_csv_route, index_col = None)
        
        x = data.index
        y = data['Ping_(ms)']

        graph_length = round(len(y) / 36, 0)
        font_size = round((-0.41 * graph_length) + 42.5, 1)

        if graph_length < 50:

            graph_length = 50
            font_size = 12

        elif graph_length > 100:

            graph_length = 100
            font_size = 1.5
        
        plt.rcParams['font.size'] = str(font_size)
        plt.figure(figsize = (graph_length, 15))
        plt.xticks(rotation=45, ha="right")
        #plt.plot(x, y, label='download', color='r')
        #plt.scatter(x, y)

        plt.margins(0)
        plt.plot(x, y, linewidth = 1.0, color = 'b', label = 'Ping Red: ' + network_name)
        
        plt.xticks(np.arange(0, max(x) + 1, 10.0))
        
        plt.yticks(np.arange(min(y) - 5, max(y) + 5, 5.0))
        
        plt.xlabel('Tiempo Transcurrido (s)')
        plt.ylabel('Ping (ms)')
        plt.title("Ping (www.google.com)")
        plt.axhline(y=9.36, color='green', linestyle='-', label = 'Ping Promedio Red: LaRosa')
        plt.axhline(y=round(y.mean(), 2), color='red', linestyle='-', label = 'Ping Promedio Red: ' + network_name)

        plt.legend()
        graph_route = graphs_route + network_name + '_ping_graph.png'
        plt.savefig(graph_route, bbox_inches='tight', dpi = 300)
        
        GRAPH_LABEL(graph_route)
        
    elif test_type == 'packetloss':

        data = pd.read_csv(data_route + network_name + '_' + packet_loss_csv_route, index_col = None)
        
        sendp_data = data['Cantidad_de_paquetes_enviados'].sum()
        recievedp_data = data['Cantidad_de_paquetes_perdidos'].sum()
        
        data = [sendp_data, recievedp_data]
        
        description_list = ['Cantidad_de_paquetes_enviados', 'Cantidad_de_paquetes_perdidos']
        
        fig = plt.figure(figsize =(10, 7))
        plt.pie(data, labels = description_list)
        
        graph_route = graphs_route + network_name + '_packetloss_graph.png'
        
        plt.savefig(graph_route, bbox_inches='tight', dpi = 300)
        
        GRAPH_LABEL(graph_route)
        
    elif test_type == 'speed':
        
        data = pd.read_csv(data_route + network_name + '_' + speed_test_csv_route, index_col = None)
        
        fecha = data['Fecha']
        hora = data['Hora']
        download = data['Velocidad_Bajada']
        upload = data['Velocidad_Subida']
            
        plt.figure(figsize = (50, 15))
        plt.xlabel('Fecha')
        plt.ylabel('Velocidad en Mb/s')
        plt.title("Velocidad Internet")
        plt.margins(0)
        plt.xticks(rotation=30, ha="right")
        plt.plot(fecha + ' ' + hora, download, label='Bajada', color='r')
        plt.plot(fecha + ' ' + hora, upload, label='Subida', color='b')
        plt.legend()
        graph_route = graphs_route + network_name + '_speed_graph.png'
        plt.savefig(graph_route, bbox_inches='tight', dpi = 300)
        #plt.show()
        
        GRAPH_LABEL(graph_route)
    

def VALIDATE_ENTRY_BOX_VALUE(value):
    
    if len(value) == 0 or int(value) == 0:
        
        return False
    
    else: 
    
        for i in range(len(value)):
            
            if int(value[i]) < 0 or int(value[i]) > 9:
                
                return False
    
        return True
    
def GET_JITTER(ping_data, start, finish):
    
    aux = 0
    dif_sum = 0
    lost_packets = 0
    
    if ping_data.size < 3:
        
        return 0, lost_packets
    
    else:
        
        iterator = False
        
        for i in range(start, finish):
            
            if ping_data[i] == 0:
                
                lost_packets+= 1
                
                if iterator:
                    
                    iterator = False
                    continue
                
                iterator = True
                
                continue
                
                #next(i)
                #next(i)
            
            elif ping_data[i] > 0:
                
                aux = ping_data[i] - ping_data[i - 1]
                
                if aux < 0:
                    
                    aux*= (-1)
        
                dif_sum+= aux
        
        return round(dif_sum / (ping_data[ping_data > 0].count() - 1), 2), lost_packets

def PING_TEST(logbox, test_time, direction):
    
    global elapsed_time
    global acc_time
    global RUNNING_PING_TEST
    
    #delta = 0
    
    cut_time = 0
    back_online_time = 0
    acc_time = 0
    cut_duration = 0
    cut_detector = False
    
    #while RUNNING_PING_TEST:
        
    network_name = GET_NETWORK_NAME()

    for i in range(test_time):
        
        function_start_time = time.time()
        
        if not RUNNING_PING_TEST:
            
            break
        
        back_online_time = datetime.datetime.now()
        
        ping = os.popen('ping ' + direction + ' -n 1')
        
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
        
        start_point = packet_loss.find('(')
        end_point = packet_loss.find('%')
        
        packet_loss = packet_loss[start_point + 1 : end_point]
        msLine = result[-1].strip()
    
        total_ms = msLine[len(msLine) - 4: len(msLine) - 2]
            
        if total_ms == 'os':
            
            cut_time = datetime.datetime.now()
            
            total_ms = 0
            cut_detector = True
            
        #cut_duration = cut_duration.microseconds
        #cut_duration = cut_duration * 10**(-3)
        #acc_time+= cut_duration
            
        a = datetime.datetime.now().strftime("%d-%m-%Y")  # date
        
        b = datetime.datetime.now().strftime("%H-%M-%S")  # time
        
        c = round(elapsed_time + 1, 1)     # float
        
        d = int(total_ms)           # int
        
        e = packet_loss           # float
         
        f = round(cut_duration, 2)    # float
        
        g = round(acc_time, 2)       # float
        
        #ping_data_fieldnames = ['Fecha', 'Hora', 'Tiempo_Transcurrido_(s)', 'Ping_(ms)', '%_Paquetes_perdidos', 'Tiempo_Corte_(ms)', 'Tiempo_de_Fallo_Acumulado_(ms)']
        
        data_info = {
            ping_data_fieldnames[0] : a,
            ping_data_fieldnames[1] : b,
            ping_data_fieldnames[2] : c,
            ping_data_fieldnames[3] : d,
            ping_data_fieldnames[4] : e,
            ping_data_fieldnames[5] : f,
            ping_data_fieldnames[6] : g
            }

        #data = pd.read_csv(data_route + GET_NETWORK_NAME() + '_' + ping_csv_route, index_col = None)
        
        with open(data_route + network_name + '_' + ping_csv_route, 'a', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = ping_data_fieldnames)
        
            csv_writer.writerow(data_info)
        
        logbox.insert(tk.END, f"\n\n Fecha: {a}, Hora: {b}, Tiempo_Transcurrido_(s): {c}, Ping_(ms): {d}, %_Paquetes_perdidos: {e}, Tiempo_Corte_(ms): {f}, 'Tiempo_de_Fallo_Acumulado_(ms): {g}")
        logbox.see("end")
        
        cut_duration = 0
        
        elapsed_time+= ping_test_interval
        
        function_end_time = time.time()
        
        function_time = function_end_time - function_start_time
        
        if function_time > 0 and function_time <= 1:
            
            time.sleep(ping_test_interval - function_time)
        
        else:
        
            time.sleep(ping_test_interval)
        
    data = pd.read_csv(data_route + network_name + '_' + ping_csv_route, index_col = None)
    
    ping_data = data['Ping_(ms)']
    
    start = ping_data.size - elapsed_time + 1
    finish = ping_data.size
    #print(start, finish)
    
    #print(ping_data.size, test_time)
    
    ping_data = ping_data[ping_data.size - elapsed_time:]
    
    #print(ping_data)
    
    jitter, lost_packets = GET_JITTER(ping_data, start, finish)
    
    #ping_results_fieldnames = ['Nombre_de_conexion', 'Servidor', 'Duracion_(s)', 'Ping_minimo', 'Ping_maximo', 'Ping_Promedio', 'Jitter', 'Paquetes_enviados', 'Paquetes_perdidos']
    
    results_info = {
        ping_results_fieldnames[0] : network_name,
        ping_results_fieldnames[1] : direction,
        ping_results_fieldnames[2] : test_time,
        ping_results_fieldnames[3] : min(ping_data),
        ping_results_fieldnames[4] : max(ping_data),
        ping_results_fieldnames[5] : round(ping_data.mean(), 2),
        ping_results_fieldnames[6] : jitter,
        ping_results_fieldnames[7] : test_time,
        ping_results_fieldnames[8] : lost_packets
        }
    
    with open(results_route + network_name + '_' + ping_csv_results_route, 'a', newline = '') as csv_file:
        
        csv_writer = csv.DictWriter(csv_file, fieldnames = ping_results_fieldnames)
    
        csv_writer.writerow(results_info)
    
    logbox.insert(tk.END, '\n\n Ping mínimo: ' + str(min(ping_data)) + ' ms.\n\n Ping máximo: ' + str(max(ping_data)) +' ms.\n\n Ping Promedio: ' + str(round(ping_data.mean(), 2)) + ' ms.\n\n Jitter: ' + str(jitter) + ' ms.\n\n Paquetes perdidos: ' + str(lost_packets) + '/' + str(finish - start + 1) +  '.')
    logbox.see("end")
    
    logbox.insert(tk.END, '\n\n Prueba finalizada con exito...')
    logbox.see("end")
    
    elapsed_time = 0
        
    RUNNING_PING_TEST = False
    
def PING_TEST_STOP():
    
    global RUNNING_PING_TEST
    
    if RUNNING_PING_TEST:
        
        RUNNING_PING_TEST = False
        
    else: return

def PING_TEST_BEGIN(entrybox, logbox, direction_combobox):
    
    global RUNNING_PING_TEST
    
    if not VALIDATE_ENTRY_BOX_VALUE(entrybox.get()):
        
        logbox.delete('1.0', tk.END)
        
        logbox.insert(tk.END, '\n Revise el numero Ingresado...')
        
        logbox.see("end")
    
        return
    
    elif RUNNING_PACKET_TEST or RUNNING_PING_TEST:
        
        logbox.insert(tk.END, '\n\n Otra prueba se esta ejecutando\n Espere Por Favor...')
    
        return
    
    else:
        
        if os.path.exists(data_route + GET_NETWORK_NAME() + '_' + ping_csv_route):
            
            os.remove(data_route + GET_NETWORK_NAME() + '_' + ping_csv_route)
        
        with open(data_route + GET_NETWORK_NAME() + '_' + ping_csv_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = ping_data_fieldnames)
            csv_writer.writeheader()
 
        RUNNING_PING_TEST = True
        
        logbox.delete('1.0', tk.END)
        
        logbox.insert(tk.END, '\n Iniciando prueba de Ping a ' + direction_combobox.get() + '...')
        
        ping_thread = threading.Thread(name = 'PingThread', target = PING_TEST, daemon=True, args=(logbox, int(entrybox.get()), direction_combobox.get(), ))
        
        ping_thread.start()

        
def PACKET_LOSS_TEST(n_packets, logbox, direction):
    
    global RUNNING_PACKET_TEST
    
    #print(n_packets, direction)
    
    start_time = time.time()
    
    pl_test = os.popen('ping ' + direction + ' -n ' + str(n_packets))
    
    result = pl_test.readlines()
    
    end_time = time.time()
    
    result = result[len(result) - 4 : len(result) - 2]
    result = result[0].strip() + result[1].strip()
    
    #result = result[result.find('(') + 1 : result.find('%') + 1]
    #print(result)
    #print(n_packets, round(end_time - start_time, 2))
    
    RUNNING_PACKET_TEST = False
    
    a = datetime.datetime.now().strftime("%d-%m-%Y")
    
    b = datetime.datetime.now().strftime("%H-%M-%S")
    
    c = round(end_time - start_time, 2)
    
    d = n_packets
    
    e = result[result.find('recibidos = ') + 12 : result.find('perdidos = ') - 2]
    
    f = result[result.find('perdidos = ') + 11 : result.find('(')]
    
    #g = result[result.find('(') + 1 : result.find('%')]
    
    g = str(round((int(f) / int(d)) * 100, 2))
    
    data_info = {
        'Fecha' : a,
        'Hora' : b,
        'Duracion_(s)' : c,
        'Cantidad_de_paquetes_enviados' : d,
        'Cantidad_de_paquetes_recibidos' : e,
        'Cantidad_de_paquetes_perdidos' : f,
        '%_de_perdida' : g
        }
    
    logbox.insert(tk.END, '\n\n Duración del test: ' + str(c) + '\n Cantidad_de_paquetes_enviados: ' + str(d) + '\n Cantidad_de_paquetes_recibidos: ' + str(e) + '\n Cantidad_de_paquetes_perdidos: ' + str(f) + '\n %_de_perdida: ' + str(g) + '%')
    
    #print(info)
    
    with open(data_route + GET_NETWORK_NAME() + '_' + packet_loss_csv_route, 'a', newline = '') as csv_file:
        
        csv_writer = csv.DictWriter(csv_file, fieldnames = packet_loss_data_fieldnames)
        csv_writer.writerow(data_info)
        
    #packet_loss_results_fieldnames = ['Duracion', 'Cantidad_de_paquetes_enviados', 'Cantidad_de_paquetes_recibidos', 'Cantidad_de_paquetes_perdidos', '%_de_perdida']
    
    results_info = {
        packet_loss_results_fieldnames[0] : c,
        packet_loss_results_fieldnames[1] : d,
        packet_loss_results_fieldnames[2] : e,
        packet_loss_results_fieldnames[3] : f,
        packet_loss_results_fieldnames[4] : g
        }
    
    with open(results_route + GET_NETWORK_NAME() + '_' + packet_loss_csv_results_route, 'a', newline = '') as csv_file:
        
        csv_writer = csv.DictWriter(csv_file, fieldnames = packet_loss_results_fieldnames)
    
        csv_writer.writerow(results_info)
    
        
def PACKETLOSS_TEST_STOP():
    
    global RUNNING_PACKET_TEST
    
    if RUNNING_PACKET_TEST: 
        
        RUNNING_PACKET_TEST = False
        
    else: return
        

def PACKET_LOSS_TEST_BEGIN(entrybox, logbox, combobox):
    
    global RUNNING_PACKET_TEST
    
    if not VALIDATE_ENTRY_BOX_VALUE(entrybox.get()):
        
        logbox.delete('1.0', tk.END)
        
        logbox.insert(tk.END, '\n Revise el numero Ingresado...')
        
        logbox.see("end")
    
        return
    
    elif RUNNING_PACKET_TEST or RUNNING_PING_TEST:
        
        logbox.insert(tk.END, '\n Otra prueba se esta ejecutando\n Espere Por Favor...')
    
        return
    
    else:
        
        network_name = GET_NETWORK_NAME()
        
        if os.path.exists(data_route + network_name + '_' + packet_loss_csv_route):
            
            os.remove(data_route + network_name + '_' + packet_loss_csv_route)
        
        with open(data_route + network_name + '_' + packet_loss_csv_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = packet_loss_data_fieldnames)
            csv_writer.writeheader()
        
        RUNNING_PACKET_TEST = True
        
        logbox.delete('1.0', tk.END)
        
        wait_time = 1.0123 * int(entrybox.get()) - 0.9084
        
        wait_time = str(round(wait_time, 2))
        
        logbox.insert(tk.END, '\n Iniciando prueba con ' + entrybox.get() + ' paquetes a ' + combobox.get() + '...\n\n Tiempo aproximado : ' + wait_time + ' Segundos...')
        
        packet_thread = threading.Thread(name = 'PacketLossThread', target = PACKET_LOSS_TEST, daemon=True, args=(entrybox.get(), logbox, combobox.get()))
        
        packet_thread.start()
        
def SPEED_TEST(wait_time, logbox):
    
    global RUNNING_SPEED_TEST
    
    #print(dir(speedtest))
    
    s = speedtest.Speedtest()
    
    best_sv = s.get_best_server()
    
    for key in best_sv:
        logbox.insert(tk.END, '\n ' + str(key) + ' : ' + str(best_sv[key]))
        logbox.see("end")
        
    logbox.insert(tk.END, '\n ')
        #print(key, ' : ', best_sv[key])
        
    a = time.time()
    
    # Muestra velocidad en Megabytes
    #speed_trans_unit = 1048576
    
    # Muestra velocidad en Megabits
    speed_trans_unit = 10**(6)

    #for i in range(int(wait_time)):
    while RUNNING_SPEED_TEST:
        
        if not RUNNING_SPEED_TEST:
            
            break
        
        b = time.time()
        
        if round((b - a), 0) % 60 == 0:
            
            s.get_best_server()
            
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            hora = datetime.datetime.now().strftime("%H:%M:%S")
            downspeed = round((round(s.download(threads = thread_count)) / speed_trans_unit), 2)
            upspeed = round((round(s.upload(threads = thread_count)) / speed_trans_unit), 2)
            
            info = {
                'Fecha' : fecha,
                'Hora' : hora,
                'Velocidad_Bajada' : downspeed,
                'Velocidad_Subida' : upspeed
                }
            
            with open(data_route + GET_NETWORK_NAME() + '_' + speed_test_csv_route, mode='a', newline='') as speedcsv:
                
                csv_writer = csv.DictWriter(speedcsv, fieldnames = speed_test_data_fieldnames)
                csv_writer.writerow(info)
            
            logbox.insert(tk.END, f"\n\n Fecha: {fecha}, Hora: {hora}, Bajada: {downspeed} Mb/s, Subida: {upspeed} Mb/s")
            logbox.see("end")
            
            #speed_test_results_fieldnames = ['Fecha', 'Hora', 'Host', 'Bajada', 'Subida']
            
            results_info = {
                speed_test_results_fieldnames[0] : fecha,
                speed_test_results_fieldnames[1] : hora,
                speed_test_results_fieldnames[2] : best_sv['host'],
                speed_test_results_fieldnames[3] : downspeed,
                speed_test_results_fieldnames[4] : upspeed
                }
            
            with open(results_route + GET_NETWORK_NAME() + '_' + speed_test_csv_results_route, 'a', newline = '') as csv_file:
                
                csv_writer = csv.DictWriter(csv_file, fieldnames = speed_test_results_fieldnames)
            
                csv_writer.writerow(results_info)
            
            if int(round((b - a), 0) // 60) == (int(wait_time) - 1):
                
                RUNNING_SPEED_TEST = False

                data = pd.read_csv('Data/' + GET_NETWORK_NAME() + '_' + speed_test_csv_route, index_col = None)
        
                vbajada = data['Velocidad_Bajada']
                vsubida = data['Velocidad_Subida']
                
                logbox.insert(tk.END, f"\n\n Promedio Bajada: {round(vbajada.mean(), 2)}\n\n Varianza Bajada: {round(vbajada.var(), 2)}\n\n Promedio Subida: {round(vsubida.mean(), 2)}\n\n Varianza Subida: {round(vsubida.var(), 2)}\n\n Prueba finalizada con exito...\n")
                #logbox.insert(tk.END, f"\n\n Promedio Bajada: {round(vbajada.mean(), 2)}\n\n Promedio Subida: {round(vsubida.mean(), 2)}\n\n Prueba finalizada con exito...\n")
                logbox.see("end")
                return
            
    logbox.insert(tk.END, "\n\n Prueba finalizada con exito...\n")
    logbox.see("end")         
    RUNNING_SPEED_TEST = False
    
def SPEEDTEST_TEST_STOP():
    
    global RUNNING_SPEED_TEST
    
    if RUNNING_SPEED_TEST: 
        
        RUNNING_SPEED_TEST = False
        
    else: return
    

def SPEED_TEST_BEGIN(entrybox, logbox):
    
    global RUNNING_SPEED_TEST
    
    if not VALIDATE_ENTRY_BOX_VALUE(entrybox.get()):
        
        logbox.delete('1.0', tk.END)
        
        logbox.insert(tk.END, '\n Revise el numero Ingresado...')
        
        logbox.see("end")
    
        return
    
    #elif RUNNING_SPEED_TEST or RUNNING_PING_TEST or RUNNING_PACKET_TEST:
        
        #logbox.insert(tk.END, '\n Otra prueba se esta ejecutando\n Espere Por Favor...')
    
        #return
    
    else:
        
        if os.path.exists(data_route + GET_NETWORK_NAME() + '_' + speed_test_csv_route):
            
            os.remove(data_route + GET_NETWORK_NAME() + '_' + speed_test_csv_route)
        
        with open(data_route + GET_NETWORK_NAME() + '_' + speed_test_csv_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = speed_test_data_fieldnames)
            csv_writer.writeheader()
        
        RUNNING_SPEED_TEST = True
        
        logbox.delete('1.0', tk.END)
        
        #wait_time = int(entrybox.get())
        
        logbox.insert(tk.END, '\n Iniciando prueba...\n\n Conectado a : ' + GET_NETWORK_NAME() + '\n')
        
        speed_thread = threading.Thread(name = 'SpeedTestThread', target = SPEED_TEST, daemon=True, args=(entrybox.get(), logbox,))
    
        speed_thread.start()
        
def CHECK_RESOURCES(frame, label):
    
    while RESOURCES:
    
        # % de utilizacion de cpu
        
        cpu = psutil.cpu_percent(1) # tasa de uso de CPU en un segundo, unidad
        cpu_per = '% .2f %%'% cpu # se convierte en un porcentaje, mantenga dos decimales
        
        # Utilizacion de memoria
        
        mem = psutil.virtual_memory()
        mem_per = '%.2f%%' % mem[2]
        mem_total = str(int(mem[0] / 1024 / 1024)) + 'MB'
        mem_used = str(int(mem[3] / 1024 / 1024)) + 'MB'
        
        # Utilizacion del disco principal
        
        c_info = psutil.disk_usage("C:")
        c_per = '%.2f%%' % c_info[3]
        
        ##################################
        # evita que el programa intente insertar texto en label cuando el objeto se destruya
        try:

            label.configure(text = '\nPorcentaje de\nuso de CPU: ' + cpu_per + '\n\nPorcentaje de memoria\nutilizada: ' +  mem_per + '\n\nMemoria total: ' +  mem_total + '\n\nMemoria en uso: ' + mem_used + '\n\nEspacio usado en\nDisco: ' + c_per)
        
        except: pass

        if not RESOURCES:

            return

        #time.sleep(0.3)
        
        #frame.after(1000, CHECK_RESOURCES, frame, label)
        
def EXIT_APP(root):
    
    global RESOURCES
    
    RESOURCES = False
    
    time.sleep(1.5)
    
    root.destroy()

def GUI():
    
    root = Tk()
    root.title("Connection monitor")
    root.iconphoto(False, tk.PhotoImage(file = 'Icons/CM.png'))
    root.geometry("+200+60")
    #root.geometry('300x300')
    
    ########## Frame levels ##############
    
    ##### General Frames #####
    
    general_frame_1 = ttk.Frame(root)
    general_frame_1.pack(side = 'top')
    
    general_frame_2 = ttk.Frame(root)
    general_frame_2.pack(side = 'top')
    
    general_frame_3 = ttk.Frame(root)
    general_frame_3.pack(side = 'top')

    general_frame_4 = ttk.Frame(root)
    general_frame_4.pack(side = 'top')
    
    ##### Button pack frames #####
    
    button_pack_frame_1 = ttk.Frame(general_frame_1, borderwidth = frame_line_thickness)
    button_pack_frame_1.pack(side = 'left', padx = general_padx, pady = general_pady)
    
    button_pack_frame_2 = ttk.Frame(general_frame_1)
    button_pack_frame_2.pack(side = 'left', padx = general_padx*4, pady = general_pady)
    
    button_pack_frame_3 = ttk.Frame(general_frame_1)
    button_pack_frame_3.pack(side = 'left', padx = general_padx, pady = general_pady)
    
    resources_usage_frame_4 = ttk.Frame(general_frame_1)
    resources_usage_frame_4.pack(side = 'left', padx = general_padx, pady = general_pady)
    
    ############## GENERAL FRAME 1 ##############
     
    ##### Buttons and labels for  button_pack_frame_1 #####
    
    ping_label_1 = ttk.Label(button_pack_frame_1, text = '*Test de ping*\n\nSeleccione dirección\npara realizar Ping.', font=("Calibri",font_size), justify = 'center')
    ping_label_1.pack(side = 'top')
    
    ping_direction_combobox = ttk.Combobox(button_pack_frame_1, state = 'readonly')
    ping_direction_combobox.pack(side = 'top')
    
    ping_direction_combobox['values'] = directions_list
    ping_direction_combobox.set(directions_list[0])
    
    ping_label_2 = ttk.Label(button_pack_frame_1, text = '\nIngrese tiempo de\nprueba en segundos.', font=("Calibri",font_size), justify = 'center')
    ping_label_2.pack(side = 'top')
    
    duration_entrybox = ttk.Entry(button_pack_frame_1)
    duration_entrybox.pack(side = 'top')
    
    #9223372036854775807
    
    inf_ping_button = ttk.Button(button_pack_frame_1, text= 'INF', command=lambda:duration_entrybox.insert(tk.END, '9223372036854775807'))
    inf_ping_button.pack(side = 'top', pady = general_pady)
    
    ping_graph_button = ttk.Button(button_pack_frame_1, text= 'Mostrar Grafico', command=lambda:SELECT_GRAPH('ping'))
    ping_graph_button.pack(side = 'top')
    
    ping_begin_button = ttk.Button(button_pack_frame_1, text= 'Iniciar Prueba', command=lambda:PING_TEST_BEGIN(duration_entrybox, ping_log_box, ping_direction_combobox))
    ping_begin_button.pack(side = 'top', pady = general_pady)
    
    ping_stop_button = ttk.Button(button_pack_frame_1, text= 'Detener Prueba', command=lambda:PING_TEST_STOP())
    ping_stop_button.pack(side = 'top')
    
    ##### Buttons and labels for  button_pack_frame_2 #####
    
    packet_loss_label_1 = ttk.Label(button_pack_frame_2, text = '*Test de perdida\nde Paquetes*\n\nSeleccione dirección\npara enviar paquetes.', font=("Calibri",font_size), justify = 'center')
    packet_loss_label_1.pack(side = 'top', expand = True)
    
    pl_direction_combobox = ttk.Combobox(button_pack_frame_2, state = 'readonly')
    pl_direction_combobox.pack(side = 'top')
    
    pl_direction_combobox['values'] = directions_list
    pl_direction_combobox.set(directions_list[0])
    
    packet_loss_label_2 = ttk.Label(button_pack_frame_2, text = '\nIngrese cantidad\nde paquetes.', font=("Calibri",font_size), justify = 'center')
    packet_loss_label_2.pack(side = 'top')
    
    packet_loss_entrybox = ttk.Entry(button_pack_frame_2)
    packet_loss_entrybox.pack(side = 'top', expand = True)
    
    pl_graph_button = ttk.Button(button_pack_frame_2, text= 'Mostrar Grafico', command=lambda:SELECT_GRAPH('packetloss'))
    pl_graph_button.pack(side = 'top', pady = general_pady)
    
    pl_begin_button = ttk.Button(button_pack_frame_2, text= 'Iniciar Prueba', command=lambda:PACKET_LOSS_TEST_BEGIN(packet_loss_entrybox, packet_loss_log_box, pl_direction_combobox))
    pl_begin_button.pack(side = 'top')
    
    pl_stop_button = ttk.Button(button_pack_frame_2, text= 'Detener Prueba', command=lambda:PACKETLOSS_TEST_STOP())
    pl_stop_button.pack(side = 'top', pady = general_pady)
    
    ##### Buttons and labels for  button_pack_frame_3 #####
    
    speedtest_label_1 = ttk.Label(button_pack_frame_3, text = '*Test de velocidad*\n\nIngrese cantidad de\npruebas que desea\nrealizar.\n\nEl intervalo entre pruebas\nsera de ' + str(speed_test_time_interval) + ' segundos.', font=("Calibri",font_size), justify = 'center')
    speedtest_label_1.pack(side = 'top', expand = True)
    
    speedtest_entrybox = ttk.Entry(button_pack_frame_3)
    speedtest_entrybox.pack(side = 'top', expand = True)
    
    inf_speed_button = ttk.Button(button_pack_frame_3, text= 'INF', command=lambda:speedtest_entrybox.insert(tk.END, '9223372036854775807'))
    inf_speed_button.pack(side = 'top', pady = general_pady)
    
    speedtest_graph_button = ttk.Button(button_pack_frame_3, text= 'Mostrar Grafico', command=lambda:SELECT_GRAPH('speed'))
    speedtest_graph_button.pack(side = 'top')
    
    speedtest_begin_button = ttk.Button(button_pack_frame_3, text= 'Iniciar Prueba', command=lambda:SPEED_TEST_BEGIN(speedtest_entrybox, speed_log_box))
    speedtest_begin_button.pack(side = 'top', pady = general_pady)
    
    speedtest_stop_button = ttk.Button(button_pack_frame_3, text= 'Detener Prueba', command=lambda:SPEEDTEST_TEST_STOP())
    speedtest_stop_button.pack(side = 'top')
    
    ##### Buttons and labels for  resources_usage_frame_4 #####
    
    resources_title_label = ttk.Label(resources_usage_frame_4, text = "*Valores de recursos\ndel equipo*", font=("Calibri",font_size), justify = 'center')
    resources_title_label.pack(side = 'top')
    
    resources_data_label = ttk.Label(resources_usage_frame_4, font=("Calibri",int(font_size//1.2)))
    resources_data_label.pack(side = 'top')
    
    #destroy_button = ttk.Button(resources_usage_frame_4, text = "BOOM", command=lambda:general_frame_1.destroy())
    #destroy_button.pack(side = 'top')

    separation_label = ttk.Label(resources_usage_frame_4)
    separation_label.pack(side = 'top', pady = general_pady)
    
    #root.after(1000, CHECK_RESOURCES, root, resources_data_label)
    
    ############## GENERAL FRAME 2 ##############
    
    log_label = ttk.Label(general_frame_2, text = '*Ping Log*                                                    *Packet Loss Log*                                         *Speed test Log*', font=("Calibri",font_size), justify = 'center')
    log_label.pack(side = 'top', expand = True)
    
    ############## GENERAL FRAME 3 ##############
    
    ping_log_box = scrolledtext.ScrolledText(general_frame_3, wrap="word", height = int(screen_height / 50), width = int(screen_width / 45))
    ping_log_box.pack(side = 'left', padx = int(general_padx/2), pady = int(general_pady/2))

    packet_loss_log_box = scrolledtext.ScrolledText(general_frame_3, wrap="word", height = int(screen_height / 50), width = int(screen_width / 45))
    packet_loss_log_box.pack(side = 'left', padx = int(general_padx/2), pady = int(general_pady/2))

    speed_log_box = scrolledtext.ScrolledText(general_frame_3, wrap="word", height = int(screen_height / 50), width = int(screen_width / 45))
    speed_log_box.pack(side = 'left', padx = int(general_padx/2), pady = int(general_pady/2))
    
    exit_button = ttk.Button(general_frame_4, text= 'SALIR DE LA APLICACION', command=lambda:EXIT_APP(root))
    exit_button.pack(side = 'top', pady = general_pady)
    
    ##############################################################
    
    resources_thread = threading.Thread(name = 'Resources', target = CHECK_RESOURCES, daemon=True, args=(root, resources_data_label, ))
    resources_thread.start()
    
    root.focus_force()
    root.protocol("WM_DELETE_WINDOW", False)  
    root.mainloop()
    
if __name__ == '__main__':
    
    directions_list = ['www.google.com', 'www.falabella.com', 'www.emol.cl', 'www.bcentral.cl']
    
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)
    
    general_padx = int(screen_width/153.6)
    general_pady = int(screen_width/136.6)
    
    gui_lines_color = 'black'
    frame_line_thickness = 2
    
    font_size = int(screen_height/64)
    
    RUNNING_PING_TEST = False
    RUNNING_PACKET_TEST = False
    RUNNING_SPEED_TEST = False
    RESOURCES = True
    
    name = ''
    
    speed_test_time_interval = 60
    
    ping_test_interval = 1
    
    results_route = 'Results/'
    
    data_route = 'Data/'
    
    graphs_route = 'Graphs/'
    
    thread_count = multiprocessing.cpu_count()
    
    #infinite = '9223372036854775807'
    
    ########## PING INFO ###########
    
    ping_csv_route = 'ping_data.csv'
    
    ping_data_fieldnames = ['Fecha', 'Hora', 'Tiempo_Transcurrido_(s)', 'Ping_(ms)', '%_Paquetes_perdidos', 'Tiempo_Corte_(ms)', 'Tiempo_de_Fallo_Acumulado_(ms)']
    
    ping_csv_results_route = 'ping_results.csv'
    
    ping_results_fieldnames = ['Nombre_de_conexion', 'Servidor', 'Duracion_(s)', 'Ping_minimo', 'Ping_maximo', 'Ping_Promedio', 'Jitter', 'Paquetes_enviados', 'Paquetes_perdidos']
    
    if not os.path.exists(results_route + GET_NETWORK_NAME() + '_' + ping_csv_results_route):
    
        with open(results_route + GET_NETWORK_NAME() + '_' + ping_csv_results_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = ping_results_fieldnames)
            csv_writer.writeheader()
    
    elapsed_time = 0
    
    acc_time = 0
    #print(screen_width, screen_height)
    
    ########## PACKET LOSS INFO ###########
    
    packet_loss_csv_route = 'pl_data.csv'
    
    packet_loss_data_fieldnames = ['Fecha', 'Hora', 'Duracion_(s)', 'Cantidad_de_paquetes_enviados', 'Cantidad_de_paquetes_recibidos', 'Cantidad_de_paquetes_perdidos', '%_de_perdida']
    
    packet_loss_csv_results_route = 'pl_results.csv'
    
    packet_loss_results_fieldnames = ['Duracion', 'Cantidad_de_paquetes_enviados', 'Cantidad_de_paquetes_recibidos', 'Cantidad_de_paquetes_perdidos', '%_de_perdida']
    
    if not os.path.exists(results_route + GET_NETWORK_NAME() + '_' + packet_loss_csv_results_route):
    
        with open(results_route + GET_NETWORK_NAME() + '_' + packet_loss_csv_results_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = packet_loss_results_fieldnames)
            csv_writer.writeheader()
    
    ########## SPEEDTEST INFO ##########
    
    speed_test_csv_route = 'speedtest_data.csv'
    
    speed_test_data_fieldnames = ['Fecha', 'Hora', 'Velocidad_Bajada', 'Velocidad_Subida']
    
    speed_test_csv_results_route = 'speedtest_results.csv'
    
    speed_test_results_fieldnames = ['Fecha', 'Hora', 'Host', 'Bajada', 'Subida']
    
    if not os.path.exists(results_route + GET_NETWORK_NAME() + '_' + speed_test_csv_results_route):
    
        with open(results_route + GET_NETWORK_NAME() + '_' + speed_test_csv_results_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = speed_test_results_fieldnames)
            csv_writer.writeheader()
    
    ####################################
    
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    GUI()