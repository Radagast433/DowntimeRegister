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
import matplotlib.animation as animation
from tkinter import messagebox
import sched
#import pyautogui

from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from tkcalendar import DateEntry


class PROGRAMTASK():

    def __init__(self, parent):

        self.frame = Toplevel()
        #self.frame.geometry("+10+10")

        self.parent = parent

        self.iterator = False

        self.date_start = ''
        self.time_start = ''

        self.date_finish = ''
        self.time_finish = ''

        self.duration = ''

        self.general_frame_1 = ttk.Frame(self.frame)
        self.general_frame_1.pack(side = 'top', padx = general_padx, pady = general_pady)

        self.general_frame_2 = ttk.Frame(self.frame)
        self.general_frame_2.pack(side = 'top', padx = general_padx, pady = general_pady)

        self.general_frame_3 = ttk.Frame(self.frame)
        self.general_frame_3.pack(side = 'top', padx = general_padx, pady = general_pady)

        self.general_frame_4 = ttk.Frame(self.frame)
        self.general_frame_4.pack(side = 'top', padx = general_padx, pady = general_pady)

        ############################ GENERAL FRAME 4 SUBDIVITIONS ###########################

        self.gf4_sub_1 = ttk.Frame(self.general_frame_4)
        self.gf4_sub_1.pack(side = 'left')

        self.gf4_sub_2 = ttk.Frame(self.general_frame_4)
        self.gf4_sub_2.pack(side = 'left', padx = general_padx * 3)

        self.gf4_sub_3 = ttk.Frame(self.general_frame_4)
        self.gf4_sub_3.pack(side = 'left')

        ############################ GENERAL FRAME 1 ################################

        self.label_1 = ttk.Label(self.general_frame_1, text = 'Seleccione Prueba:')
        self.label_1.pack(side = 'top')

        self.cmbx_values = ['Prueba_de_Ping', 'Prueba_de_Perdida_de_Paquetes', 'Prueba_de_Velocidad']

        self.test_combobox = ttk.Combobox(self.general_frame_1, width = 30, state = 'readonly')
        self.test_combobox.pack(side = 'top')

        self.test_combobox['values'] = self.cmbx_values
        self.test_combobox.set(self.cmbx_values[0])

        #############################################################################
        ############################ GENERAL FRAME 2 ################################

        ################ Level 1 sub frames ################

        self.sub_gf2_1 = ttk.Frame(self.general_frame_2)
        self.sub_gf2_1.pack(side = 'left')

        self.sub_gf2_2 = ttk.Frame(self.general_frame_2)
        self.sub_gf2_2.pack(side = 'left', padx = general_padx * 3)

        self.sub_gf2_3 = ttk.Frame(self.general_frame_2)
        self.sub_gf2_3.pack(side = 'left')

        #####################################################

        ################ Level 2 sub frames #################

        self.sub_gf2_2_1 = ttk.Frame(self.sub_gf2_2)
        self.sub_gf2_2_1.pack(side = 'top')

        self.sub_gf2_2_2 = ttk.Frame(self.sub_gf2_2)
        self.sub_gf2_2_2.pack(side = 'top')

        ##############################################################################

        self.actual_date_year = datetime.datetime.now().strftime("%Y")
        self.actual_date_month = datetime.datetime.now().strftime("%m")
        self.actual_date_day = datetime.datetime.now().strftime("%d")

        self.actual_date_hour = datetime.datetime.now().strftime("%H")
        self.actual_date_minutes = datetime.datetime.now().strftime("%M")
        self.actual_date_seconds = datetime.datetime.now().strftime("%S")

        self.label_2 = ttk.Label(self.sub_gf2_1, text = 'Ingrese Fecha:')
        self.label_2.pack(side = 'top')

        self.calendar = DateEntry(self.sub_gf2_1, width = 12, year = int(self.actual_date_year), month = int(self.actual_date_month), day = int(self.actual_date_day), background = 'darkblue', foreground = 'white', borderwidth = 2, state = "readonly")
        self.calendar.pack(side = 'top')

        ###################################################################################

        self.label_3 = ttk.Label(self.sub_gf2_2_1, text = 'Ingrese Hora:')
        self.label_3.pack(side = 'top')
     
        self.hours = ttk.Spinbox(self.sub_gf2_2_2, from_= 0, to = 23, wrap = True, width = 3, state = "readonly", justify = CENTER)
        self.hours.pack(side = 'left')

        self.hours.set(int(self.actual_date_hour))

        self.minutes = ttk.Spinbox(self.sub_gf2_2_2, from_= 0, to = 59, wrap = True, width = 3, state = "readonly", justify = CENTER)
        self.minutes.pack(side = 'left')

        self.minutes.set(int(self.actual_date_minutes))

        self.seconds = ttk.Spinbox(self.sub_gf2_2_2, from_= 0, to = 59, wrap = True, width = 3, state = "readonly", justify = CENTER)
        self.seconds.pack(side = 'left')

        self.seconds.set(int(self.actual_date_seconds))

        ##############################################################################################

        self.add_button = ttk.Button(self.sub_gf2_3, text = 'Agregar', command=lambda:self.ADD())
        self.add_button.pack(side = 'top')

        ##############################################################################################

        self.interval_label = ttk.Label(self.general_frame_3, text = 'Ingrese Inicio', background = 'green', foreground = 'white')
        self.interval_label.pack(side = 'top')

        ###############################################################################################

        self.program_button = ttk.Button(self.gf4_sub_1, text = 'Programar', command=lambda:self.PROGRAM())
        self.program_button.pack(side = 'top')

        self.delete_button = ttk.Button(self.gf4_sub_1, text = 'Borrar Pruebas\n Programadas', command=lambda:self.DELETE())
        self.delete_button.pack(side = 'top', padx = general_padx * 2, pady = general_pady)

        self.cancel_button = ttk.Button(self.gf4_sub_3, text = 'Cerrar', command=lambda:self.CANCEL())
        self.cancel_button.pack(side = 'top')

        self.cancel_program_button = ttk.Button(self.gf4_sub_3, text = 'Detener Pruebas\nProgramadas', command=lambda:self.STOPALL())
        self.cancel_program_button.pack(side = 'top', pady = general_pady)

        self.frame.focus_force()
        center(self.parent, self.frame)

    def ADD(self):

        #print(self.date_hour_start)

        if not self.iterator:

            self.interval_label.configure(text = 'Ingrese Termino', background = 'red', foreground = 'yellow')

            self.iterator = True

            self.date_start = self.calendar.get_date().strftime("%d") + '-' + self.calendar.get_date().strftime("%m") + '-' + self.calendar.get_date().strftime("%Y")
            self.time_start = self.hours.get() + '-' + self.minutes.get() + '-' + self.seconds.get()

            return

        if self.iterator:

            self.interval_label.configure(text = 'Ingrese Inicio', background = 'green', foreground = 'white')

            self.iterator = False

            self.date_finish = self.calendar.get_date().strftime("%d") + '-' + self.calendar.get_date().strftime("%m") + '-' + self.calendar.get_date().strftime("%Y")
            self.time_finish = self.hours.get() + '-' + self.minutes.get() + '-' + self.seconds.get()
            
            self.duration = datetime.datetime.strptime(self.date_finish + ' ' + self.time_finish, '%d-%m-%Y %H-%M-%S') - datetime.datetime.strptime(self.date_start + ' ' + self.time_start, '%d-%m-%Y %H-%M-%S')
            self.duration = int(round(self.duration / datetime.timedelta(minutes = 1)))
    
            #program_data_fieldnames = ['Fecha_Inicio', 'Hora_Inicio', 'Fecha_Termino', 'Hora_Termino', 'Prueba', 'Duracion']

            data_info = {
                'Fecha_Inicio' : self.date_start,
                'Hora_Inicio' : self.time_start,
                'Fecha_Termino' : self.date_finish,
                'Hora_Termino' : self.time_finish,
                'Prueba' : self.test_combobox.get(),
                'Duracion' : str(self.duration)
                }
            
            with open(program_route + program_csv_route, 'a', newline = '') as csv_file:
                
                csv_writer = csv.DictWriter(csv_file, fieldnames = program_data_fieldnames)
                csv_writer.writerow(data_info)

            return

    def STOPALL(self):

        global RUNNING_PACKET_TEST
        global RUNNING_PING_TEST
        global RUNNING_SPEED_TEST
        global RUNNING_PROGRAMMER
        
        RUNNING_PACKET_TEST = False
        RUNNING_PING_TEST = False
        RUNNING_SPEED_TEST = False
        RUNNING_PROGRAMMER = False

        messagebox.showinfo(message = 'TODAS LAS PRUEBAS FUERON\nDETENIDAS EXITOSAMENTE', title = 'Detencion de Pruebas...')

    def CANCEL(self):

        self.frame.destroy()

    def DELETE(self):

        sysfile = open(program_route + program_csv_route, 'w+')
        sysfile.close()

        with open(program_route + program_csv_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = program_data_fieldnames)
            csv_writer.writeheader()
        
    def PROGRAM(self):

        if self.iterator:

            self.option = messagebox.askretrycancel(message = "Por Favor, Ingrese Fecha de Termino", title = "Revise los datos ingresados...", parent = self.frame)

            if not self.option:

                self.CANCEL()

            elif self.option:

                return

        self.info_frame = Toplevel()

        self.general_frame_5 = ttk.Frame(self.info_frame)
        self.general_frame_5.pack(side = 'top')

        self.general_frame_6 = ttk.Frame(self.info_frame)
        self.general_frame_6.pack(side = 'top')

        self.general_frame_7 = ttk.Frame(self.info_frame)
        self.general_frame_7.pack(side = 'top')

        ################################################################

        self.label_5 = ttk.Label(self.general_frame_5, text = '### Resumen ###')
        self.label_5.pack(side = 'top')

        self.label_6 = ttk.Label(self.general_frame_6, text = 'Prueba: ' + self.test_combobox.get())
        self.label_6.pack(side = 'top')

        self.label_7 = ttk.Label(self.general_frame_6, text = 'Horarios:')
        self.label_7.pack(side = 'top')

        self.data = pd.read_csv(program_route + program_csv_route, index_col = None)
        
        #self.scrolled_info = scrolledtext.ScrolledText(self.general_frame_6, width = int(round(GetSystemMetrics(0) / 21.33, 0)))
        self.scrolled_info = scrolledtext.ScrolledText(self.general_frame_6, width = 90)
        self.scrolled_info.pack(side = 'top')
        
        self.scrolled_info.delete('1.0', tk.END)

        self.scrolled_info.insert(tk.END, '\n')

        self.scrolled_info.insert(tk.END, self.data)

        self.accept_button = ttk.Button(self.general_frame_7, text = 'Aceptar', command=lambda:(self.info_frame.destroy(), self.frame.destroy(), self.START_PROGRAM()))
        self.accept_button.pack(side = 'left')

        self.label_8 = ttk.Label(self.general_frame_7)
        self.label_8.pack(side = 'left', padx = general_padx * 3)

        self.accept_button = ttk.Button(self.general_frame_7, text = 'Cancelar', command=lambda:self.info_frame.destroy())
        self.accept_button.pack(side = 'left')

        self.info_frame.focus_force()

        center(self.frame, self.info_frame)

    def START_PROGRAM(self):
        #print('START_PROGRAM Control')
        #self.programmed_thread = threading.Thread(name = 'ProgramThread', target = TEST_PROGRAMMER, daemon=True)
        #self.programmed_thread.start()

        global RUNNING_PROGRAMMER
    
        #program_data_fieldnames = ['Fecha_Inicio', 'Hora_Inicio', 'Fecha_Termino', 'Hora_Termino', 'Prueba', 'Duracion']
        #self.cmbx_values = ['Prueba de Ping', 'Prueba de Perdida de Paquetes', 'Prueba de Velocidad']
        self.test = pd.read_csv(program_route + program_csv_route)
        self.rows_list = self.test.values.tolist()

        for i in range(len(self.rows_list)):

            self.date_list = self.rows_list[i][0].split('-')
            self.time_list = self.rows_list[i][1].split('-')

            if self.rows_list[i][4] == 'Prueba_de_Ping' and not RUNNING_PING_TEST:#, 'Prueba_de_Perdida_de_Paquetes', 'Prueba_de_Velocidad']

                self.event1 = tasks_scheduler.enterabs((datetime.datetime.strptime(self.date_list[2] + '/' + self.date_list[1] + '/' + self.date_list[0] + ' ' + self.time_list[0] + ':' + self.time_list[1] + ':' + self.time_list[2], '%Y/%m/%d %H:%M:%S')).timestamp(), 1, PING_TEST_BEGIN, argument = (int(self.rows_list[i][5]) * 60, ping_log_box, ping_direction_combobox, 'task'))

                RUNNING_PROGRAMMER = True

            elif self.rows_list[i][4] == 'Prueba_de_Perdida_de_Paquetes' and not RUNNING_PACKET_TEST:

                self.event2 = tasks_scheduler.enterabs((datetime.datetime.strptime(self.date_list[2] + '/' + self.date_list[1] + '/' + self.date_list[0] + ' ' + self.time_list[0] + ':' + self.time_list[1] + ':' + self.time_list[2], '%Y/%m/%d %H:%M:%S')).timestamp(), 2, PACKET_LOSS_TEST_BEGIN, argument = (int(round(((int(self.rows_list[i][5]) * 60) + 0.9084) / 1.0123, 0)), ping_log_box, ping_direction_combobox, 'task'))
            
                RUNNING_PROGRAMMER = True

            elif self.rows_list[i][4] == 'Prueba_de_Velocidad' and not RUNNING_SPEED_TEST:

                self.event3 = tasks_scheduler.enterabs((datetime.datetime.strptime(self.date_list[2] + '/' + self.date_list[1] + '/' + self.date_list[0] + ' ' + self.time_list[0] + ':' + self.time_list[1] + ':' + self.time_list[2], '%Y/%m/%d %H:%M:%S')).timestamp(), 3, SPEED_TEST_BEGIN, argument = (int(self.rows_list[i][5]), ping_log_box, ping_direction_combobox, 'task'))
            
                RUNNING_PROGRAMMER = True

            self.programmed_thread = threading.Thread(name = 'ProgramThread', target = self.RUN_PROGRAM, daemon=True)
            self.programmed_thread.start()

        RUNNING_PROGRAMMER = False

    def RUN_PROGRAM(self):

        tasks_scheduler.run()


def center(parent, actual):                     # Funcion para centrar ventanas
    
    actual.update()
    actual_pos = "+" + str(((parent.winfo_width() - actual.winfo_width()) // 2) + parent.winfo_x()) + "+" + str(((parent.winfo_height() - actual.winfo_height()) // 2) + parent.winfo_y())
    actual.geometry(actual_pos)

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
        
    
def SELECT_GRAPH(test_type, is_task):

    network_name = GET_NETWORK_NAME()
    
    if test_type == 'ping':

        data = pd.read_csv(data_route + network_name + '_' + ping_csv_route, index_col = None)

        graph_name = data.iloc[-1]

        graph_name_p1 = graph_name['Fecha']
        #graph_name_p1.replace('-', '_')

        graph_name_p2 = graph_name['Hora']
        #graph_name_p2.replace('-', '_')

        graph_name = graph_name_p1 + '_' + graph_name_p2
        #graph_name = graph_name.to_string(index = False)
        
        y = data['Ping_(ms)']
        y = y[ping_graph_start + 1 : ]
            
        x = [ i for i in range(0 , y.size)]

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

        if VALIDATE_ENTRY_BOX_VALUE(sub_1_ping_min_entry.get()):

            plt.axhline(y=float(sub_1_ping_min_entry.get()), color='r', linestyle='solid', label = 'Ping Minimo Usuario')

        if VALIDATE_ENTRY_BOX_VALUE(sub_2_ping_max_entry.get()):

            plt.axhline(y=float(sub_2_ping_max_entry.get()), color='g', linestyle='solid', label = 'Ping Maximo Usuario')
        
        x_ticks = 10.0

        if len(x) < 30:

            x_ticks = 1.0

        plt.xticks(np.arange(0, max(x) + 1, x_ticks))
        
        plt.yticks(np.arange(min(y) - 5, max(y) + 5, 5.0))
        
        plt.xlabel('Tiempo Transcurrido (s)')
        plt.ylabel('Ping (ms)')
        plt.title("Ping (www.google.com)")

        #plt.axhline(y=9.36, color='green', linestyle='-', label = 'Ping Promedio Red: LaRosa')
        #plt.axhline(y=round(y.mean(), 2), color='red', linestyle='-', label = 'Ping Promedio Red: ' + network_name)

        plt.legend()
        graph_route = ping_graphs_route + network_name + '_ping_graph_' + graph_name + '.png'
        plt.savefig(graph_route, bbox_inches='tight', dpi = 300)

        if is_task == 'task':

            return
        
        GRAPH_LABEL(graph_route)
        
    elif test_type == 'packetloss':

        data = pd.read_csv(data_route + network_name + '_' + packet_loss_csv_route, index_col = None)
        
        graph_name = data.iloc[-1]

        graph_name_p1 = graph_name['Fecha']
        #graph_name_p1.replace('-', '_')

        graph_name_p2 = graph_name['Hora']
        #graph_name_p2.replace('-', '_')

        graph_name = graph_name_p1 + '_' + graph_name_p2

        sendp_data = data['Cantidad_de_paquetes_enviados'].sum()
        recievedp_data = data['Cantidad_de_paquetes_perdidos'].sum()
        
        data = [sendp_data, recievedp_data]
        
        description_list = ['Cantidad_de_paquetes_enviados', 'Cantidad_de_paquetes_perdidos']
        
        fig = plt.figure(figsize =(10, 7))
        plt.pie(data, labels = description_list)
        
        graph_route = packet_loss_graphs_route + network_name + '_packetloss_graph_' + graph_name + '.png'
        
        plt.savefig(graph_route, bbox_inches='tight', dpi = 300)
        
        GRAPH_LABEL(graph_route)
        
    elif test_type == 'speed':
        
        data = pd.read_csv(data_route + network_name + '_' + speed_test_csv_route, index_col = None)
        
        graph_name = data.iloc[-1]

        graph_name_p1 = graph_name['Fecha']
        #graph_name_p1.replace('-', '_')

        graph_name_p2 = graph_name['Hora']
        #graph_name_p2.replace('-', '_')

        graph_name = graph_name_p1 + '_' + graph_name_p2
        #graph_name = graph_name.to_string(index = False)

        fecha = data['Fecha']
        fecha = fecha[speed_graph_start + 1 : ]

        hora = data['Hora']
        hora = hora[speed_graph_start + 1 : ]

        download = data['Velocidad_Bajada']
        download = download[speed_graph_start + 1 : ]

        upload = data['Velocidad_Subida']
        upload = upload[speed_graph_start +1 : ]
            
        plt.figure(figsize = (50, 15))
        plt.xlabel('Fecha')
        plt.ylabel('Velocidad en Mb/s')
        plt.title("Velocidad Internet")
        plt.margins(0)

        if VALIDATE_ENTRY_BOX_VALUE(sub_1_speed_up_entry_speed.get()):

            plt.axhline(y=float(sub_1_speed_up_entry_speed.get()), color='black', linestyle='solid', label = 'Velocidad Subida Usuario')

        if VALIDATE_ENTRY_BOX_VALUE(sub_2_speed_down_entry_speed.get()):

            plt.axhline(y=float(sub_2_speed_down_entry_speed.get()), color='g', linestyle='solid', label = 'Velocidad Bajada Usuario')

        plt.xticks(rotation=30, ha="right")
        plt.plot(fecha + ' ' + hora, download, label='Bajada (Mbps)', color='r')
        plt.plot(fecha + ' ' + hora, upload, label='Subida (Mbps)', color='b')
        plt.legend()
        graph_route = speed_graphs_route + network_name + '_speed_graph_' + graph_name + '.png'
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

        for_return = round(dif_sum / (ping_data[ping_data > 0].count() - 1), 2)
        
        return for_return, lost_packets

def PING_TEST(logbox, test_time, direction, is_task):
    
    global elapsed_time
    global acc_time
    global RUNNING_PING_TEST
    global ping_graph_start
    
    #delta = 0
    
    cut_time = 0
    back_online_time = 0
    acc_time = 0
    cut_duration = 0
    cut_detector = False

    network_name = GET_NETWORK_NAME()

    data = pd.read_csv(data_route + network_name + '_' + ping_csv_route, index_col = None)
    
    start_cut = data.last_valid_index()
    ping_graph_start = start_cut

    data = []

    #start_date = datetime.datetime.now().strftime("%d-%m-%Y")  # date
    #start_hour = datetime.datetime.now().strftime("%H-%M-%S") 

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

        if 'Compruebe el nombre' in result[0]:

            logbox.delete('1.0', tk.END)
            logbox.insert(tk.END, '\n\n La solicitud de ping no pudo encontrar  el host ' + direction + '.\n\n Por Favor revise la dirección e intente nuevamente.')
            RUNNING_PING_TEST = False
            return

        try:
            packet_loss = result[6].strip()
            start_point = packet_loss.find('(')
            end_point = packet_loss.find('%')
        
            packet_loss = packet_loss[start_point + 1 : end_point]
        except:
            packet_loss = '100'

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
        
        data = pd.read_csv(data_route + network_name + '_' + ping_csv_route, index_col = None)

        end_cut = data.last_valid_index()

        ping_data = data['Ping_(ms)']
        ping_data = ping_data[start_cut + 1 : end_cut + 1]
        
        jitter, lost_packets = GET_JITTER(ping_data, start_cut + 2, end_cut + 1)

        try:
            
            logbox.insert(tk.END, f"\n\n Fecha: {a}, Hora: {b}, Tiempo_Transcurrido_(s): {c}, Ping_(ms): {d}, %_Paquetes_perdidos: {e}, Tiempo_Corte_(ms): {f}, 'Tiempo_de_Fallo_Acumulado_(ms): {g}, Jitter: {jitter}")
            logbox.see("end")
        
        except: pass

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

    if is_task == 'task':

        return

    #SELECT_GRAPH('ping', is_task)
    
def PING_TEST_STOP():
    
    global RUNNING_PING_TEST
    
    if RUNNING_PING_TEST:
        
        RUNNING_PING_TEST = False
        
    else: return

def PING_TEST_BEGIN(entrybox_value, logbox, direction_combobox, is_task):
    
    global RUNNING_PING_TEST
    
    if not VALIDATE_ENTRY_BOX_VALUE(str(entrybox_value)):
        
        logbox.delete('1.0', tk.END)
        
        logbox.insert(tk.END, '\n Revise el numero Ingresado...')
        
        logbox.see("end")
    
        return
    
    elif RUNNING_PACKET_TEST or RUNNING_PING_TEST or RUNNING_PROGRAMMER:
        
        logbox.insert(tk.END, '\n\n Otra prueba se esta ejecutando\n Espere Por Favor...')
    
        return
    
    else:
        
        '''if os.path.exists(data_route + GET_NETWORK_NAME() + '_' + ping_csv_route):
            
            os.remove(data_route + GET_NETWORK_NAME() + '_' + ping_csv_route)
        
        with open(data_route + GET_NETWORK_NAME() + '_' + ping_csv_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = ping_data_fieldnames)
            csv_writer.writeheader()'''

        RUNNING_PING_TEST = True
        
        logbox.delete('1.0', tk.END)
        
        logbox.insert(tk.END, '\n Iniciando prueba de Ping a ' + direction_combobox.get() + '...')
        
        ping_thread = threading.Thread(name = 'PingThread', target = PING_TEST, daemon=True, args=(logbox, int(entrybox_value), direction_combobox.get(), is_task,))
        
        ping_thread.start()

        
def PACKET_LOSS_TEST(n_packets, logbox, direction):
    
    global RUNNING_PACKET_TEST
    global pl_test
    
    #print(n_packets, direction)
    
    start_time = time.time()
    
    pl_test = os.popen('ping ' + direction + ' -n ' + str(n_packets))
    
    result = pl_test.readlines()

    if 'Compruebe el nombre' in result[0]:

            logbox.delete('1.0', tk.END)
            logbox.insert(tk.END, '\n\n La solicitud de ping no pudo encontrar  el host ' + direction + '.\n\n Por Favor revise la dirección e intente nuevamente.')
            RUNNING_PACKET_TEST = False
            return
    
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
    logbox.see("end")
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

        '''# Holds down the alt key
        pyautogui.keyDown("alt")
        # Presses the tab key once
        pyautogui.press("tab")

        # Lets go of the alt key
        pyautogui.keyUp("alt")'''
        
        RUNNING_PACKET_TEST = False
        
    else: return
        

def PACKET_LOSS_TEST_BEGIN(entrybox, logbox, combobox):
    
    global RUNNING_PACKET_TEST
    
    if not VALIDATE_ENTRY_BOX_VALUE(entrybox.get()):
        
        logbox.delete('1.0', tk.END)
        
        logbox.insert(tk.END, '\n Revise el numero Ingresado...')
        
        logbox.see("end")
    
        return
    
    elif RUNNING_PACKET_TEST or RUNNING_PING_TEST or RUNNING_PROGRAMMER:
        
        logbox.insert(tk.END, '\n Otra prueba se esta ejecutando\n Espere Por Favor...')
    
        return
    
    else:
        
        #network_name = GET_NETWORK_NAME()
        
        '''if os.path.exists(data_route + network_name + '_' + packet_loss_csv_route):
            
            os.remove(data_route + network_name + '_' + packet_loss_csv_route)
        
        with open(data_route + network_name + '_' + packet_loss_csv_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = packet_loss_data_fieldnames)
            csv_writer.writeheader()'''
        
        RUNNING_PACKET_TEST = True
        
        logbox.delete('1.0', tk.END)
        
        wait_time = 1.0123 * int(entrybox.get()) - 0.9084

        #packets_in_time = int(round((time + 0.9084) / 1.0123, 0))
        
        wait_time = str(round(wait_time, 2))
        
        logbox.insert(tk.END, '\n Iniciando prueba con ' + entrybox.get() + ' paquetes a ' + combobox.get() + '...\n\n Tiempo aproximado : ' + wait_time + ' Segundos...')
        
        packet_thread = threading.Thread(name = 'PacketLossThread', target = PACKET_LOSS_TEST, daemon=True, args=(entrybox.get(), logbox, combobox.get()))
        
        packet_thread.start()
        
def SPEED_TEST(wait_time, logbox, combobox, is_task):
    
    global RUNNING_SPEED_TEST
    global speed_graph_start

    #print(dir(speedtest))
    
    # listado de servers https://williamyaps.github.io/wlmjavascript/servercli.html
    

    '''best_sv = s.get_best_server()

    servers = s.get_servers()

    for keys in servers:

        for server in servers[keys]:

            print(server['sponsor'] + ' ' + server['name'] + ' ' + server['id'])

        #print(servers[keys])

    #print(servers)

    RUNNING_SPEED_TEST = False

    return
    
    for key in best_sv:
        logbox.insert(tk.END, '\n ' + str(key) + ' : ' + str(best_sv[key]))
        logbox.see("end")
    '''

    network_name = GET_NETWORK_NAME()
        
    logbox.insert(tk.END, '\n ')
        #print(key, ' : ', best_sv[key])
        
    a = time.time()
    
    option = combobox.get()

    start = option.find('(')
    end = option.find(')')
    server_id = option[start + 1 : end]

    try:

        s.get_servers([int(server_id)])
    
    except:

        logbox.insert(tk.END, '\n Ocurrio un Problema, por favor\n seleccione otro servidor.')
        logbox.see("end")

        RUNNING_SPEED_TEST = False

        return

    data = pd.read_csv(data_route + network_name + '_' + speed_test_csv_route, index_col = None)
    
    start_cut = data.last_valid_index()
    speed_graph_start = start_cut

    data = []
    
    # Muestra velocidad en Megabytes
    #speed_trans_unit = 1048576
    
    # Muestra velocidad en Megabits
    speed_trans_unit = 10**(6)

    speed_graph_date = datetime.datetime.now().strftime("%d-%m-%Y") + '_' + datetime.datetime.now().strftime("%H-%M-%S")

    if is_task == 'task':

        s.get_best_server()

    #for i in range(int(wait_time)):
    while RUNNING_SPEED_TEST:
        
        if not RUNNING_SPEED_TEST:
            
            break
        
        b = time.time()
        
        if round((b - a), 0) % 60 == 0:
            
            #s.get_best_server()
            
            fecha = datetime.datetime.now().strftime("%d-%m-%Y")
            hora = datetime.datetime.now().strftime("%H-%M-%S")
            downspeed = round((round(s.download(threads = thread_count)) / speed_trans_unit), 2)
            upspeed = round((round(s.upload(threads=thread_count, pre_allocate=False)) / speed_trans_unit), 2)
            
            info = {
                'Fecha' : fecha,
                'Hora' : hora,
                'Velocidad_Bajada' : downspeed,
                'Velocidad_Subida' : upspeed
                }
            
            with open(data_route + network_name + '_' + speed_test_csv_route, mode='a', newline='') as speedcsv:
                
                csv_writer = csv.DictWriter(speedcsv, fieldnames = speed_test_data_fieldnames)
                csv_writer.writerow(info)
            
            logbox.insert(tk.END, f"\n\n Fecha: {fecha}, Hora: {hora}, Bajada: {downspeed} Mb/s, Subida: {upspeed} Mb/s")
            logbox.see("end")
            
            #speed_test_results_fieldnames = ['Fecha', 'Hora', 'Host', 'Bajada', 'Subida']
            
            results_info = {
                speed_test_results_fieldnames[0] : fecha,
                speed_test_results_fieldnames[1] : hora,
                speed_test_results_fieldnames[2] : option,
                speed_test_results_fieldnames[3] : downspeed,
                speed_test_results_fieldnames[4] : upspeed
                }
            
            with open(results_route + network_name + '_' + speed_test_csv_results_route, 'a', newline = '') as csv_file:
                
                csv_writer = csv.DictWriter(csv_file, fieldnames = speed_test_results_fieldnames)
            
                csv_writer.writerow(results_info)
            
            if int(round((b - a), 0) // 60) == (int(wait_time) - 1):
                
                RUNNING_SPEED_TEST = False

                data = pd.read_csv('Data/' + network_name + '_' + speed_test_csv_route, index_col = None)
        
                vbajada = data['Velocidad_Bajada']
                vbajada = vbajada[start_cut + 1 :]

                vsubida = data['Velocidad_Subida']
                vsubida = vsubida[start_cut + 1 :]
                
                logbox.insert(tk.END, f"\n\n Promedio Bajada: {round(vbajada.mean(), 2)}\n\n D. Estandar Bajada: {round(vbajada.std(), 2)}\n\n Promedio Subida: {round(vsubida.mean(), 2)}\n\n D. Estandar Subida: {round(vsubida.std(), 2)}\n\n Prueba finalizada con exito...\n")
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
    
def VALIDATE_COMBOBOX_VALUE(combobox):

    option = combobox.get()

    if len(option) > 0:

        start = option.find('(')
        end = option.find(')')

        if start > (-1) and end > (-1) and (end - start) > 1:

            return True

        else: 

            return False

    else:

        return False
        
        #option = option[start + 1 : end]
        #print(option[start + 1 : end])
        #print(option)

def SPEED_TEST_BEGIN(entrybox, logbox, combobox, is_task):
    
    global RUNNING_SPEED_TEST
    
    if not VALIDATE_ENTRY_BOX_VALUE(entrybox.get()) or not VALIDATE_COMBOBOX_VALUE(combobox):
        
        logbox.delete('1.0', tk.END)
        
        logbox.insert(tk.END, '\n Revise los datos Ingresados...')
        
        logbox.see("end")

        RUNNING_SPEED_TEST = False
    
        return
    
    #elif RUNNING_SPEED_TEST or RUNNING_PING_TEST or RUNNING_PACKET_TEST:
        
        #logbox.insert(tk.END, '\n Otra prueba se esta ejecutando\n Espere Por Favor...')
    
        #return

    elif RUNNING_PROGRAMMER or RUNNING_SPEED_TEST:

            logbox.insert(tk.END, '\n Otra prueba se esta ejecutando\n Espere Por Favor...')
    
            return
    
    else:
        
        '''if os.path.exists(data_route + GET_NETWORK_NAME() + '_' + speed_test_csv_route):
            
            os.remove(data_route + GET_NETWORK_NAME() + '_' + speed_test_csv_route)
        
        with open(data_route + GET_NETWORK_NAME() + '_' + speed_test_csv_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = speed_test_data_fieldnames)
            csv_writer.writeheader()'''
        
        RUNNING_SPEED_TEST = True
        
        logbox.delete('1.0', tk.END)
        
        #wait_time = int(entrybox.get())
        
        logbox.insert(tk.END, '\n Iniciando prueba...\n\n Conectado a : ' + GET_NETWORK_NAME())
        
        speed_thread = threading.Thread(name = 'SpeedTestThread', target = SPEED_TEST, daemon=True, args=(entrybox.get(), logbox, combobox, is_task,))
    
        speed_thread.start()
        
def CHECK_RESOURCES(label):
    
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

            #label.configure(text = '\nPorcentaje de\nuso de CPU: ' + cpu_per + '\n\nPorcentaje de memoria\nutilizada: ' +  mem_per + '\n\nMemoria total: ' +  mem_total + '\n\nMemoria en uso: ' + mem_used + '\n\nEspacio usado en\nDisco: ' + c_per)
            #label.configure(text = 'CPU: ' + cpu_per + '  |  RAM: ' +  mem_used + '/' + mem_total + ' (' + mem_per + ')' + '  |  ALM: ' + c_per)
            label.configure(text = 'CPU: ' + cpu_per + '  |  RAM: ' +  mem_used + '/' + mem_total + ' (' + mem_per + ')')

        except: pass

        if not RESOURCES:

            return

        #time.sleep(0.3)
        
        #frame.after(1000, CHECK_RESOURCES, frame, label)
        
def EXIT_APP(root):
    
    global RESOURCES
    global RUNNING_PACKET_TEST
    global RUNNING_PING_TEST
    global RUNNING_SPEED_TEST
    global RUNNING_PROGRAMMER

    if RUNNING_PROGRAMMER:

        messagebox.showinfo(message = 'Hay tareas Programadas, Por Favor\nEspere hasta que finalicen.', title = '¡ADVERTENCIA!')
        return

    RUNNING_PACKET_TEST = False
    RUNNING_PING_TEST = False
    RUNNING_SPEED_TEST = False
    #RUNNING_PROGRAMMER = False
    RESOURCES = False

    plt.close("all")
    
    time.sleep(1.5)
    
    root.destroy()

#def PING_LIVE_GRAPH_BEGIN():

    #graph_animation = PLG_Class.PingLiveGraph(GET_NETWORK_NAME())
    #graph_animation.ANIMATE()

def SELECT_BEST_SERVER(combobox):

    best_sv = s.get_best_server()

    combobox.set(best_sv['sponsor'] + '-' + best_sv['name'] + '-(' + best_sv['id'] + ')')

def GET_SERVERS_LIST(combobox):

    servers = s.get_servers()
    
    servers_norm_list = []

    for keys in servers:

        for server in servers[keys]:

            servers_norm_list.append(server['sponsor'] + '-' + server['name'] + '-(' + server['id'] + ')')
            #print(server['sponsor'] + ' ' + server['name'] + ' ' + server['id'])

    combobox['values'] = servers_norm_list
    combobox.set(servers_norm_list[0])

    #print(best_sv['sponsor'] + '-' + best_sv['name'] + ' ' + best_sv['id'])

def GUI():
    
    global sub_1_ping_min_entry
    global sub_2_ping_max_entry
    global sub_1_speed_up_entry_speed
    global sub_2_speed_down_entry_speed
    global ping_log_box
    global ping_direction_combobox

    root = Tk()
    root.title("Connection monitor")
    root.iconphoto(False, tk.PhotoImage(file = 'Icons/CM.png'))
    root.geometry("+0+0")
    #root.geometry('300x300')
    
    ########## Frame levels ##############

    info_divition = ttk.Frame(root)
    info_divition.pack(side = 'left')
    
    graphs_divition = ttk.Frame(root)
    graphs_divition.pack(side = 'left')

    ##### General Frames #####
    
    general_frame_1 = ttk.Frame(info_divition)
    general_frame_1.pack(side = 'top')
    
    general_frame_2 = ttk.Frame(info_divition)
    general_frame_2.pack(side = 'top')
    
    general_frame_3 = ttk.Frame(info_divition)
    general_frame_3.pack(side = 'top')

    general_frame_4 = ttk.Frame(info_divition)
    general_frame_4.pack(side = 'top')
    
    ##### Button pack frames #####
    
    button_pack_frame_1 = ttk.Frame(general_frame_1, borderwidth = frame_line_space, relief = RIDGE)
    button_pack_frame_1.pack(side = 'left', padx = general_padx)
    
    button_pack_frame_2 = ttk.Frame(general_frame_1)
    button_pack_frame_2.pack(side = 'left', padx = general_padx * 10, pady = general_pady)
    
    button_pack_frame_3 = ttk.Frame(general_frame_1, borderwidth = frame_line_space, relief = RIDGE)
    button_pack_frame_3.pack(side = 'left', padx = general_padx)
    
    #resources_usage_frame_4 = ttk.Frame(general_frame_1)
    #resources_usage_frame_4.pack(side = 'left', padx = general_padx, pady = general_pady)

    ##### Graphs pack frames #######

    ping_graph_frame = ttk.Frame(graphs_divition)
    ping_graph_frame.pack(side = 'top')

    ping_graph_label = ttk.Frame(ping_graph_frame)
    ping_graph_label.pack(side = 'top')

    speed_graph_frame = ttk.Frame(graphs_divition)
    speed_graph_frame.pack(side = 'top')
    
    ############## GENERAL FRAME 1 ##############
     
    ##### Buttons and labels for  button_pack_frame_1 #####
    
    ping_label_1 = ttk.Label(button_pack_frame_1, text = '*Test de ping*\n\nIngrese dirección\npara realizar Ping:', font=("Calibri",font_size), justify = 'center')
    ping_label_1.pack(side = 'top')
    
    #ping_direction_combobox = ttk.Combobox(button_pack_frame_1, state = 'readonly')
    ping_direction_combobox = ttk.Combobox(button_pack_frame_1)
    ping_direction_combobox.pack(side = 'top')
    
    ping_direction_combobox['values'] = directions_list
    ping_direction_combobox.set(directions_list[0])

    #####################################################################################

    reference_values_text = ttk.Label(button_pack_frame_1, text = '\nValores de referencia (Opt)', font=("Calibri",font_size), justify = 'center')
    reference_values_text.pack(side = 'top')

    sub_ping_frame_reference = ttk.Frame(button_pack_frame_1)
    sub_ping_frame_reference.pack(side = 'top')

    sub_1_min_reference_values = ttk.Frame(sub_ping_frame_reference)
    sub_1_min_reference_values.pack(side = 'left')

    sub_sep_label = ttk.Label(sub_ping_frame_reference, width = 2)
    sub_sep_label.pack(side = 'left')

    sub_2_max_reference_values = ttk.Frame(sub_ping_frame_reference)
    sub_2_max_reference_values.pack(side = 'left')

    sub_1_min_label = ttk.Label(sub_1_min_reference_values, text = 'Ping Min:')
    sub_1_min_label.pack(side = 'top')

    sub_1_ping_min_entry = ttk.Entry(sub_1_min_reference_values, width = 5)
    sub_1_ping_min_entry.pack(side = 'top')
    
    sub_2_max_label = ttk.Label(sub_2_max_reference_values, text = 'Ping Max:')
    sub_2_max_label.pack(side = 'top')

    sub_2_ping_max_entry = ttk.Entry(sub_2_max_reference_values, width = 5)
    sub_2_ping_max_entry.pack(side = 'top')

    ##########################################################################################################

    ping_label_3 = ttk.Label(button_pack_frame_1, text = '\nIngrese tiempo de\nprueba en segundos:', font=("Calibri",font_size), justify = 'center')
    ping_label_3.pack(side = 'top')
    
    duration_entrybox = ttk.Entry(button_pack_frame_1)
    duration_entrybox.pack(side = 'top')
    
    #9223372036854775807
    
    ################################### PING TEST ###################################
    ########### Sub Buttons for button_pack_frame_1 ################

    #sub_1 = ttk.Frame(button_pack_frame_1)
    #sub_1.pack(side = 'top', pady = general_pady)

    sub_2 = ttk.Frame(button_pack_frame_1)
    sub_2.pack(side = 'top', pady = general_pady)

    sub_3 = ttk.Frame(button_pack_frame_1)
    sub_3.pack(side = 'top', pady = general_pady)
    
    ping_begin_button = ttk.Button(sub_2, text= 'Iniciar Prueba', command=lambda:PING_TEST_BEGIN(duration_entrybox.get(), ping_log_box, ping_direction_combobox, 'normal'))
    ping_begin_button.pack(side = 'left')

    #sub_3_label_1 = ttk.Label(sub_2)
    #sub_3_label_1.pack(side = 'left', padx = round(general_padx * 1.5))
    
    ping_stop_button = ttk.Button(sub_2, text= 'Detener Prueba', command=lambda:PING_TEST_STOP())
    ping_stop_button.pack(side = 'left')

    inf_ping_button = ttk.Button(sub_3, text= 'INF', command=lambda:duration_entrybox.insert(tk.END, '9223372036854775807'))
    inf_ping_button.pack(side = 'left')

    ping_graph_button = ttk.Button(sub_3, text= 'Mostrar Grafico', command=lambda:SELECT_GRAPH('ping', 'normal'))
    ping_graph_button.pack(side = 'left')

    #sub_2_label_1 = ttk.Label(sub_3)
    #sub_2_label_1.pack(side = 'left', padx = round(general_padx * 1.5))
    # aux = PLG_Class.PingLiveGraph() aux.animate()
    #ping_live_graph_button = ttk.Button(sub_3, text= 'Grafico en Vivo', command=lambda:None)
    #ping_live_graph_button.pack(side = 'left')
    
    ################################### PACKET LOSS TEST ###################################
    ##### Buttons and labels for  button_pack_frame_2 #####
    
    pl_subdivition_1 = ttk.Frame(button_pack_frame_2, borderwidth = frame_line_space, relief = RIDGE)
    pl_subdivition_1.pack(side = 'top')

    pl_subdivition_2 = ttk.Frame(button_pack_frame_2)
    pl_subdivition_2.pack(side = 'top')

    packet_loss_label_1 = ttk.Label(pl_subdivition_1, text = '*Test de perdida\nde Paquetes*\n\nIngrese dirección\npara enviar paquetes:', font=("Calibri",font_size), justify = 'center')
    packet_loss_label_1.pack(side = 'top', expand = True)
    
    #pl_direction_combobox = ttk.Combobox(button_pack_frame_2, state = 'readonly')
    pl_direction_combobox = ttk.Combobox(pl_subdivition_1)
    pl_direction_combobox.pack(side = 'top')
    
    pl_direction_combobox['values'] = directions_list
    pl_direction_combobox.set(directions_list[0])
    
    packet_loss_label_2 = ttk.Label(pl_subdivition_1, text = '\nIngrese cantidad\nde paquetes:', font=("Calibri",font_size), justify = 'center')
    packet_loss_label_2.pack(side = 'top')
    
    packet_loss_entrybox = ttk.Entry(pl_subdivition_1)
    packet_loss_entrybox.pack(side = 'top', expand = True)

    ############################################################################################
    sub_top_buttons_pl_1 = ttk.Frame(pl_subdivition_1)
    sub_top_buttons_pl_1.pack(side = 'top')

    sub_top_buttons_pl_2 = ttk.Frame(pl_subdivition_1)
    sub_top_buttons_pl_2.pack(side = 'top', pady = general_pady)

    ################################################################################################

    pl_begin_button = ttk.Button(sub_top_buttons_pl_1, text= 'Iniciar Prueba', command=lambda:PACKET_LOSS_TEST_BEGIN(packet_loss_entrybox, packet_loss_log_box, pl_direction_combobox))
    pl_begin_button.pack(side = 'left')
    
    pl_stop_button = ttk.Button(sub_top_buttons_pl_1, text= 'Detener Prueba', command=lambda:PACKETLOSS_TEST_STOP())
    pl_stop_button.pack(side = 'left', pady = general_pady)

    pl_graph_button = ttk.Button(sub_top_buttons_pl_2, text= 'Mostrar Grafico', command=lambda:SELECT_GRAPH('packetloss', 'normal'))
    pl_graph_button.pack(side = 'left')

    ######################################## Programar Pruebas ########################################

    program_test = ttk.Button(pl_subdivition_2, text = 'Programar Pruebas', command=lambda:PROGRAMTASK(root))
    program_test.pack(side = 'top', pady = general_pady * 2)
    
    ################################### SPEED TESTS ###################################
    ##### Buttons and labels for  button_pack_frame_3 #####
    
    speedtest_label_1 = ttk.Label(button_pack_frame_3, text = '*Test de velocidad*\n\nIngrese ID del server:', font=("Calibri",font_size), justify = 'center')
    speedtest_label_1.pack(side = 'top', expand = True)

    top_speed_buttons_frame = ttk.Frame(button_pack_frame_3)
    top_speed_buttons_frame.pack(side = 'top')
    
    speedtest_best_server_button = ttk.Button(top_speed_buttons_frame, text = 'Mejor Server', command=lambda:SELECT_BEST_SERVER(speedtest_servers_combobox))
    speedtest_best_server_button.pack(side = 'left', pady = general_pady)

    sep_top_speed_buttons_label = ttk.Label(top_speed_buttons_frame, width = 2)
    sep_top_speed_buttons_label.pack(side = 'left')

    speedtest_servers_update_button = ttk.Button(top_speed_buttons_frame, text = 'Actualizar Lista', command=lambda:GET_SERVERS_LIST(speedtest_servers_combobox))
    speedtest_servers_update_button.pack(side = 'left')

    speedtest_servers_combobox = ttk.Combobox(button_pack_frame_3, width = 35)
    speedtest_servers_combobox.pack(side = 'top', pady = general_pady)
    
    #################################################################################

    reference_values_text_speed = ttk.Label(button_pack_frame_3, text = 'Valores de referencia (Opt)', font=("Calibri",font_size), justify = 'center')
    reference_values_text_speed.pack(side = 'top')

    sub_speed_frame_reference = ttk.Frame(button_pack_frame_3)
    sub_speed_frame_reference.pack(side = 'top', pady = general_pady - 3)

    sub_1_down_reference_values = ttk.Frame(sub_speed_frame_reference)
    sub_1_down_reference_values.pack(side = 'left')

    sub_sep_speed_label = ttk.Label(sub_speed_frame_reference, width = 3)
    sub_sep_speed_label.pack(side = 'left')

    sub_2_up_reference_values = ttk.Frame(sub_speed_frame_reference)
    sub_2_up_reference_values.pack(side = 'left')

    sub_1_down_label = ttk.Label(sub_1_down_reference_values, text = 'Subida:')
    sub_1_down_label.pack(side = 'top')

    sub_1_speed_up_entry_speed = ttk.Entry(sub_1_down_reference_values, width = 5)
    sub_1_speed_up_entry_speed.pack(side = 'top')
    
    sub_2_up_label = ttk.Label(sub_2_up_reference_values, text = 'Bajada:')
    sub_2_up_label.pack(side = 'top')

    sub_2_speed_down_entry_speed = ttk.Entry(sub_2_up_reference_values, width = 5)
    sub_2_speed_down_entry_speed.pack(side = 'top')

    #################################################################################

    speedtest_label_2 = ttk.Label(button_pack_frame_3, text = 'Ingrese cantidad de pruebas:\n(Intervalos de ' + str(speed_test_time_interval) + ' segundos)', font=("Calibri",font_size), justify = 'center')
    speedtest_label_2.pack(side = 'top')

    speedtest_entrybox = ttk.Entry(button_pack_frame_3)
    speedtest_entrybox.pack(side = 'top', expand = True)
    
    ########## Sub divitions #############

    sub_4 = ttk.Frame(button_pack_frame_3)
    sub_4.pack(side = 'top')

    sub_5 = ttk.Frame(button_pack_frame_3)
    sub_5.pack(side = 'top')

    ######################################

    speedtest_begin_button = ttk.Button(sub_4, text= 'Iniciar Prueba', command=lambda:SPEED_TEST_BEGIN(speedtest_entrybox, speed_log_box, speedtest_servers_combobox, 'normal'))
    speedtest_begin_button.pack(side = 'left', pady = general_pady)
    
    speedtest_stop_button = ttk.Button(sub_4, text= 'Detener Prueba', command=lambda:SPEEDTEST_TEST_STOP())
    speedtest_stop_button.pack(side = 'left')

    inf_speed_button = ttk.Button(sub_5, text= 'INF', command=lambda:speedtest_entrybox.insert(tk.END, '9223372036854775807'))
    inf_speed_button.pack(side = 'left', pady = general_pady)
    
    speedtest_graph_button = ttk.Button(sub_5, text= 'Mostrar Grafico', command=lambda:SELECT_GRAPH('speed', 'normal'))
    speedtest_graph_button.pack(side = 'left')
    
    ##### Buttons and labels for  resources_usage_frame_4 #####
    
    '''resources_title_label = ttk.Label(resources_usage_frame_4, text = "*Valores de recursos\ndel equipo*", font=("Calibri",font_size), justify = 'center')
    resources_title_label.pack(side = 'top')
    
    resources_data_label = ttk.Label(resources_usage_frame_4, font=("Calibri",int(font_size//1.2)))
    resources_data_label.pack(side = 'top')'''
    
    #destroy_button = ttk.Button(resources_usage_frame_4, text = "BOOM", command=lambda:resources_usage_frame_4.destroy())
    #destroy_button.pack(side = 'top')

    #separation_label = ttk.Label(resources_usage_frame_4)
    #separation_label.pack(side = 'top', pady = general_pady)
    
    #root.after(1000, CHECK_RESOURCES, root, resources_data_label)
    
    ############## GENERAL FRAME 2 ##############
    
    log_label = ttk.Label(general_frame_2, text = '*Ping Log*                                                    *Packet Loss Log*                                         *Speed test Log*', font=("Calibri",font_size), justify = 'center')
    log_label.pack(side = 'top', expand = True)
    
    ############## GENERAL FRAME 3 ##############
    
    ping_log_box = scrolledtext.ScrolledText(general_frame_3, wrap="word", height = int(screen_height / 60), width = int(screen_width / 45))
    ping_log_box.pack(side = 'left', padx = int(general_padx/2), pady = int(general_pady/2))

    packet_loss_log_box = scrolledtext.ScrolledText(general_frame_3, wrap="word", height = int(screen_height / 60), width = int(screen_width / 45))
    packet_loss_log_box.pack(side = 'left', padx = int(general_padx/2), pady = int(general_pady/2))

    speed_log_box = scrolledtext.ScrolledText(general_frame_3, wrap="word", height = int(screen_height / 60), width = int(screen_width / 45))
    speed_log_box.pack(side = 'left', padx = int(general_padx/2), pady = int(general_pady/2))
    
    ################### general_frame_4 ###################

    gf4_label_1 = ttk.Label(general_frame_4, text = version, font=("Calibri",int(font_size//1.5)), width = general_padx * 3)
    gf4_label_1.pack(side = 'left', padx = general_padx * 2)

    exit_button = ttk.Button(general_frame_4, text= 'SALIR DE LA APLICACION', command=lambda:EXIT_APP(root))
    exit_button.pack(side = 'left', padx = general_padx * 10, pady = general_pady)

    resources_data_label = ttk.Label(general_frame_4, font=("Calibri",int(font_size//1.5)))
    resources_data_label.pack(side = 'right')

    ##############################################################
    
    resources_thread = threading.Thread(name = 'Resources', target = CHECK_RESOURCES, daemon=True, args=(resources_data_label, ))
    resources_thread.start()
    
    root.focus_force()
    root.protocol("WM_DELETE_WINDOW", False)  
    root.mainloop()
    
if __name__ == '__main__':
    
    directions_list = ['www.google.com', 'www.falabella.com', 'www.emol.cl', 'www.bcentral.cl', 'www.bing.com', 'www.facebook.com']
    
    screen_width = GetSystemMetrics(0)
    screen_height = GetSystemMetrics(1)
    
    general_padx = int(screen_width / 153.6)
    general_pady = int(screen_width / 136.6)

    tasks_scheduler = sched.scheduler(time.time, time.sleep)
    
    gui_lines_color = 'black'
    frame_line_space = 4

    frame_line_thickness = 1
    
    font_size = int(screen_height/64)
    
    RUNNING_PING_TEST = False
    RUNNING_PACKET_TEST = False
    RUNNING_SPEED_TEST = False
    RUNNING_PROGRAMMER = False
    RESOURCES = True
    
    name = ''
    
    speed_test_time_interval = 60
    
    ping_test_interval = 1
    
    results_route = 'Results/'
    
    program_route = 'Program/'

    data_route = 'Data/'
    
    #graphs_route = 'Graphs/'

    ping_graphs_route = 'Graphs/Ping/'

    packet_loss_graphs_route = 'Graphs/PacketLoss/'

    speed_graphs_route = 'Graphs/Speed/'
    
    program_csv_route = 'test_program.csv'

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
    
    ping_graph_start = pd.read_csv(data_route + GET_NETWORK_NAME() + '_' + ping_csv_route, index_col = None).last_valid_index()

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
    
    speed_graph_start = 0

    speed_graph_date = 0

    s = speedtest.Speedtest()

    ################## Program csv data ###########################

    program_data_fieldnames = ['Fecha_Inicio', 'Hora_Inicio', 'Fecha_Termino', 'Hora_Termino', 'Prueba', 'Duracion']

    if not os.path.exists(program_route + program_csv_route):
    
        with open(program_route + program_csv_route, 'w+', newline = '') as csv_file:
            
            csv_writer = csv.DictWriter(csv_file, fieldnames = program_data_fieldnames)
            csv_writer.writeheader()

    ############### Ping Reference values Entry boxes #####################

    sub_1_ping_min_entry = None

    sub_2_ping_max_entry = None

    ############### Speed Reference values Entry boxes #####################

    sub_1_speed_up_entry_speed = None
    
    sub_2_speed_down_entry_speed = None
    
    ################################# Programmed tasks (Bool) #####################################

    ping_programmed = False

    packet_loss_programmed = False

    speed_programmed = False

    ######################################################################

    ping_log_box = None
    ping_direction_combobox = None
    
    ######################################################################

    pl_test = None

    ######################################################################

    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    version = 'Connection Monitor V1.0'

    GUI()