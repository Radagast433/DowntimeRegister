# -*- coding: utf-8 -*-
"""
Created on Thu May 13 02:50:07 2021

@author: Equipo
"""

from win32api import GetSystemMetrics   #%     # para obtener resolucion del monitor huesped
import serial.tools.list_ports    #%             # para obtener los puertos de comunicacion disponibles
import speech_recognition as sr    #%          # para reconocimiento de voz                         # para correcciones ortograficas
import pyttsx3     #%                        # Offline TTS   ~  https://pypi.org/project/pyttsx3/
from gtts import gTTS    #%                  # Online Google TTS
import requests       #%                   # para testear conexion a internet
from BrailleAlf import BrailleDictionary, PaperSheets
import time          #%            
import os      #%
from pathlib import Path  #%    
from tkinter import scrolledtext #%
import tkinter as tk #%                     
from PIL import ImageTk, Image, ImageDraw, ImageFont #%   # para menjo de imagenes
from tkinter.font import Font   #%             # para fuente tkinter
from pygame import mixer    #%            # Para reproducir audio            
import shutil      #%
import math      #%                 # para redondear numeros enteros al siguiente numero entero
import numpy as np    #%
import serial      #%           # para comunicacion con arduino
import threading   #%              # para ejecutar hilo para obtener callbacks
import matplotlib.pyplot as plt   #%
import csv
import ctypes   # para esconder consola durante ejecucion

class ToolTip(object):                          # Clase para desplegar informacion y reproducir audio cuando el cursor se situa sobre un boton.

    def __init__(self, widget):                 # Constructor
    
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.icon_audio = None
        self.x = self.y = 0

    def showtip(self, text, audio):
        
        "Display text in tooltip window"
        self.text = text
        
        if self.tipwindow or not self.text:
            return
        
        x, y, cx, cy = self.widget.bbox("insert")
        x+= self.widget.winfo_rootx() 
        y+= self.widget.winfo_rooty() - round(GetSystemMetrics(1) / 19.63)
        #print(x, y)
        self.tipwindow = tw = tk.Toplevel(self.widget)
        
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        
        label = tk.Label(tw, text=self.text, justify = tk.LEFT, background="#ffffe0", relief = tk.SOLID, borderwidth=1, font=(text_font, text_font_size, "normal"))
        label.grid(ipadx=1)
        
        if contrast_state:
            
            label.config(background = 'yellow')
        
        self.icon_audio = mixer.Sound(audio)
        
        if audio_state:
        
            mixer.Sound.set_volume(self.icon_audio, 0.0)
            
            if audio == 'sounds/habilitar_audio_spanish_penelope.mp3':
        
                mixer.Sound.set_volume(self.icon_audio, 1.0)
                
        elif not audio_state:
            
            if audio == "sounds/escuchar_texto_spanish_penelope.mp3" and mixer.music.get_busy() :
                mixer.Sound.set_volume(self.icon_audio, 0.0)
            
            else:
                mixer.Sound.set_volume(self.icon_audio, 1.0)
        
        if audio == "sounds/escuchar_texto_spanish_penelope.mp3":
            mixer.music.set_volume(1.0)
        elif audio != "sounds/escuchar_texto_spanish_penelope.mp3":
            mixer.music.set_volume(0.4)    # Argumento de 0.0 a 1.0, define el volumen de la musica, en este caso se le baja el volumen a la reproduccion del tts cuando el cursor se situa sobre un boton que reproduce audio.
        
        time.sleep(0.1)        # Tiempo para mostrar informacion y audio sobre el boton en el que se situa el cursor.
        self.icon_audio.play()
        
    
    def hidetip(self):
        
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
            mixer.music.set_volume(1.0)        # Devuelve el volumen al maximo del audio tts cuando el cursor ya no esta sobre un boton.
            self.icon_audio.stop()

def CreateToolTip(widget, text, audio):
    
    toolTip = ToolTip(widget)
    
    def enter(event):
        toolTip.showtip(text, audio)
        
    def leave(event):
        toolTip.hidetip()
        
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def resize_icon(image_name, icon_individual_size_factor, image_type):
    
    if image_type == 'icon':    # si es un icono, se reescala a proporciones cuadradas
    
        icon = Image.open(image_name)
        icon = icon.resize((int(tamano_icon/icon_individual_size_factor), int(tamano_icon/icon_individual_size_factor)))
        icon = ImageTk.PhotoImage(icon)
        return icon
    
    if image_type == 'image':    # si es imagen, se reescala segun la proporcion de las medidas de la hoja seleccionada
        
        image = Image.open(image_name)
        image = image.resize((int((tamano_icon/icon_individual_size_factor)*(PaperSheets.sheet_size[selected_sheet_size][0]/PaperSheets.sheet_size[selected_sheet_size][1])), int(tamano_icon/icon_individual_size_factor)))
        image = ImageTk.PhotoImage(image)
        return image

def get_tts_text(root, input_text_box):
    
    #global start_time
    #start_time = time.perf_counter()
    
    text = ' '
    text = input_text_box.get("1.0", tk.END)
    
    select_tts(root, text)

def check_internet_connection():
    
    try:
        request = requests.get('https://www.google.com/', timeout=3)
        return True
    except:
        return False

def select_tts(root, text): # Verifica la conexion a internet y selecciona tts online u offline /// Cuando existe una conexion a internet, el programa selecciona gTTS, en caso contrario se utiliza PYTTSX3

    #text = ' '
    #text = input_text_box.get("1.0", tk.END)

    if (len(text) == 1): 
        mixer.stop()
        no_text = mixer.Sound("sounds/no_text_spanish_penelope.mp3")
        no_text.play()     
    
    elif (len(text) > 1):
    
        global audio_temp
            
        wait = WaitPlease(root)
        
        if check_internet_connection() and tts_type == 'Online':
            audio_temp = "temp/audio/tts_temp_audio.mp3"                 # Para gTTS establece la ruta del archivo temporal de audio como formato mp3
            tts_gTTS(text)                         
    
        elif not check_internet_connection() or tts_type == 'Offline':
            audio_temp = "temp/audio/tts_temp_audio.wav"                 # Para PYTTSX3 establece la ruta del archivo temporal de audio como formato wav
            tts_PYTTSX3(text)
        
        wait.destroy_wait()
        
        #global end_time
        #global start_time
        #end_time = time.perf_counter()
        #print('Inicio: ' + str(start_time) + ' s\nTermino: ' + str(end_time) + ' s\nDuracion: ' + str(end_time - start_time) + ' s')
        #end_time = 0
        #start_time = 0

def activate_audio():
    
    button_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    button_audio.play()
    
    global audio_state
    audio_state = False

def deactivate_audio():
    
    button_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    button_audio.play()
    
    global audio_state
    audio_state = True
    
############################## TTS ###################################
    
def tts_gTTS(text):                     # Online text to speech
    
    mixer.music.stop()
    mixer.music.unload()
    
    if (file_comprobation(audio_temp)):
        time.sleep(1)
        os.remove(audio_temp)
    
    tts = gTTS(text, lang = tts_lang)
    tts.save(audio_temp)
    mixer.music.load(audio_temp)
    mixer.music.play()
    
def tts_PYTTSX3(text):                        # Offline text to speech
    
    mixer.music.stop()                    
    mixer.music.unload()
    
    if (file_comprobation(audio_temp)):
        os.remove(audio_temp)
        time.sleep(1)
    
    pyttsx3engine.save_to_file(text , audio_temp)
    pyttsx3engine.runAndWait()
    
    mixer.music.load(audio_temp)
    mixer.music.play()
    
def stop_tts():
    mixer.music.stop()
    mixer.music.unload()
    pyttsx3engine.stop()
    
###########################################################################
        
def file_comprobation(file_name):     # Funcion para comprobar la existencia de un archivo en un directorio especifico
    fileObj = Path(file_name)
    return fileObj.is_file()          # Retorna dato de tipo bool, True si el archivo existe, si no, retorna False
        
def input_text_size(option, font):     # Funcion para cambiar el tamaño de texto de la caja de entrada de texto
    
    global scrolled_font_size         # Para modificar variable global
  
    button_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    button_audio.play()
    
    if (option):                                   # Si el parametro es True, aumenta el tamano de texto en dos unidades
        scrolled_font_size+= 2
        font.configure(size = scrolled_font_size)

    if (not option and scrolled_font_size > 15):     # Si el parametro es False, reduce el tamano de texto en dos unidades con tamaño minimo de texto 10
        scrolled_font_size-= 2
        font.configure(size = scrolled_font_size)

    
def cambiar_tamano(root, option, input_text_box):      # Funcion para modificar el tamaño de los elementos de la aplicaión

    button_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    button_audio.play()    

    global tamano_icon              # Para modificar variable global
    global text_font_size           # Para modificar variable global
    global button_separation_X      # Para modificar variable global
    global button_separation_Y      # Para modificar variable global
    global icon_separation          # Para modificar variable global
    global Bar_1_label_spacing
    
    if (option):              # Se aumenta el tamaño en las unidades especificadas
        if tamano_icon >= round(GetSystemMetrics(1)/9) - 5:   # limita la reduccion de ventana para no alterar espaciado de la aplicacion
            return
        tamano_icon+= 5
    
    if (not option):        # Se reduce el tamaño en las unidades especificadas
        if tamano_icon <= math.floor(GetSystemMetrics(1)/13.5):   # limita la reduccion de ventana para no alterar espaciado de la aplicacion
            return    
        tamano_icon-= 5
        
    if contrast_state:
        #center
        ###################### Bar_1 ######################
        icon01 = resize_icon('icons/hc/icon01.png', 1, 'icon')    # Reescalado de icono con factor de ajuste individual, segundo argumento ==1 (tamano normal), <1 agrandar icono, >1 reducir icono
        icon02 = resize_icon('icons/hc/icon02.png', 1, 'icon')    
        icon03 = resize_icon('icons/hc/icon03.png', 1, 'icon')   
        icon04 = resize_icon('icons/hc/stop_tts.png', 1, 'icon')    
        icon05 = resize_icon('icons/hc/icon04.png', 1, 'icon')   
        icon06 = resize_icon('icons/hc/pausa.png', 1, 'icon')   
        icon07 = resize_icon('icons/hc/icon06.png', 1, 'icon')   
        
        ###################### Bar_2 ######################
        icon08 = resize_icon('icons/hc/letter_max.png', 2, 'icon')   
        icon09 = resize_icon('icons/hc/letter.png', 2, 'icon')     
        icon10 = resize_icon('icons/hc/letter_min.png', 2, 'icon')
        icon11 = resize_icon('icons/hc/microphone.png', 2, 'icon')
        if recording:
            icon11 = resize_icon('icons/hc/microphone_rec.png', 2, 'icon')
        icon12 = resize_icon('icons/hc/contraste.png', 2, 'icon')     
        
        ###################### Bar_3 ######################
        icon13 = resize_icon('icons/hc/expand.png', 2, 'icon')      
        icon14 = resize_icon('icons/hc/shrink.png', 2, 'icon')
        icon15 = resize_icon('icons/hc/icon05_1.png', 2, 'icon')      
        icon16 = resize_icon('icons/hc/icon05_2.png', 2, 'icon')
        icon17 = resize_icon('icons/hc/settings.png', 2, 'icon')
        icon18 = resize_icon('icons/hc/erase_text.png', 2, 'icon')
        icon19 = resize_icon('icons/hc/redo.png', 2, 'icon')
        icon20 = resize_icon('icons/hc/undo.png', 2, 'icon')
        
    elif not contrast_state:
        
        ###################### Bar_1 ######################
        icon01 = resize_icon('icons/icon01.png', 1, 'icon')    # Reescalado de icono con factor de ajuste individual, segundo argumento ==1 (tamano normal), <1 agrandar icono, >1 reducir icono
        icon02 = resize_icon('icons/icon02.png', 1, 'icon')    
        icon03 = resize_icon('icons/icon03.png', 1, 'icon')   
        icon04 = resize_icon('icons/stop_tts.png', 1, 'icon')    
        icon05 = resize_icon('icons/icon04.png', 1, 'icon')   
        icon06 = resize_icon('icons/pausa.png', 1, 'icon')   
        icon07 = resize_icon('icons/icon06.png', 1, 'icon')   
        
        ###################### Bar_2 ######################
        icon08 = resize_icon('icons/letter_max.png', 2, 'icon')   
        icon09 = resize_icon('icons/letter.png', 2, 'icon')     
        icon10 = resize_icon('icons/letter_min.png', 2, 'icon')   
        icon11 = resize_icon('icons/microphone.png', 2, 'icon')
        if recording:
            icon11 = resize_icon('icons/microphone_rec.png', 2, 'icon')
        icon12 = resize_icon('icons/contraste.png', 2, 'icon')     
        
        ###################### Bar_3 ######################
        icon13 = resize_icon('icons/expand.png', 2, 'icon')      
        icon14 = resize_icon('icons/shrink.png', 2, 'icon')
        icon15 = resize_icon('icons/icon05_1.png', 2, 'icon')      
        icon16 = resize_icon('icons/icon05_2.png', 2, 'icon')
        icon17 = resize_icon('icons/settings.png', 2, 'icon')
        icon18 = resize_icon('icons/erase_text.png', 2, 'icon')
        icon19 = resize_icon('icons/redo.png', 2, 'icon')
        icon20 = resize_icon('icons/undo.png', 2, 'icon')
    
    image_list = [icon01, icon02, icon03, icon04, icon05, icon06, icon07, icon08, icon09, icon10, 
                  icon11, icon12, icon13, icon14, icon16, icon15, icon20, icon19, icon18, icon17]
    
    button_cont = 0
    
    for bar in root.winfo_children():
        for widget in bar.winfo_children():
            
            if 'button' in str(widget).split(".")[-1] or 'label' in str(widget).split(".")[-1] and widget.cget("text") == 'A':
                widget.configure(image = image_list[button_cont], font =(text_font, text_font_size))
                widget.image = image_list[button_cont]
                button_cont+= 1
            
            elif 'label' in str(widget).split(".")[-1]:
                
                if widget.cget("text") == 'Impresora Conectada.     ' or widget.cget("text") == 'Impresora Desconectada.':
                    
                    continue
                
                if '!frame2' in str(bar).split(".")[-1]:
                    widget.configure(height = int(tamano_icon/16))
                    
                elif '!frame3' in str(bar).split(".")[-1]:
                    
                    if option:
                       
                        widget.configure(width = int(tamano_icon//3.4) - 15)
                
                elif '!frame' == str(bar).split(".")[-1]:
                    
                    widget.configure(width = int(tamano_icon//34)) 
                
                else:
                    
                    widget.configure(width = int(tamano_icon//3.4))
          
            elif '!label' == str(widget).split(".")[-1]:
    
                widget.configure(font = (text_font, int(text_font_size//1.3)))
            
            else: continue
              
    text_font_size = int(tamano_icon/6)             # Modifica el tamaño del texto de los botones de acuerdo al nuevo tamaño
    button_separation_X = int(tamano_icon/4)        # Modifica el valor de la separacion de los botones/iconos de acuerdo al nuevo tamaño en el eje X
    button_separation_Y = int(tamano_icon/16)       # Modifica el valor de la separacion de los botones/iconos de acuerdo al nuevo tamaño en el eje Y
    icon_separation = int(tamano_icon/6)            # Modifica el valor de la separacion del icono salir de acuerdo al nuevo valor de tamaño    
    input_text_box.update()
    
    # Acualiza la ventana root, permitiendo obtener los valores de las dimensiones de la ventana creada de acuerdo a los elementos que contiene
    #498 1012
    if root.winfo_width() != 1012:
        input_text_box.configure(height = round(tamano_icon/3), width = round(tamano_icon/0.8))
    
   
    root.update()
    
    
class WaitPlease(object):    # Clase para mostrar ventana de espera
    
    def __init__(self, frame):                 # Constructor
    
        self.log = tk.Toplevel()
        self.log.iconphoto(False, tk.PhotoImage(file='icons/window_icon.png'))
        self.log.resizable(0,0)
        self.image_wait = resize_icon('icons/wait.png', 0.5, 'icon')
        self.label_1 = tk.Label(self.log, text = '  Espere un momento  \nPor Favor...', font =(text_font, text_font_size*2), bg = button_color)
        self.label_2 = tk.Label(self.log, image = self.image_wait, bg = button_color)
        self.frame = frame
        self.log.grab_set()
        
        self.log.title("Espere un momento...")
        self.log.configure(bg = button_color)
        
        self.label_1.pack(side = "top")
        self.label_2.pack(side = "top")
        
        mixer.stop()
        self.wait_audio = mixer.Sound('sounds/espere_spanish_penelope.mp3')
        self.wait_audio.play()
        
        center(self.frame, self.log)
        self.log.focus_force()
        self.log.update()
        
    def destroy_wait(self):
        
        mixer.Sound(self.wait_audio).stop()
        self.log.destroy()

# No tocar esta funcion, magia negra
def text_eval(text):               # Evalua el texto ingresado segun alfabeto braille espanol, separando palabras, contandolas y prepara el texto ingresado para ajustarse al formato Braille
                                         # Tambien cuenta los espacios como caracteres
    caracteres_imprimibles = 0
    caracteres_totales_Braille = 0
    
    #print('control 1')        # print de control
    
    words = []

    text = text + ' '     # para que funcion split agregue una sola plabra si solo una es ingresada.
    
    for i, letra in enumerate(text):                          # i es el indice, letra el elemento, para contar caracteres totales
        
        if letra in BrailleDictionary.b_characters:           # Si letra esta en diccionario, la cuenta
            caracteres_imprimibles+= 1
            
        elif chr(ord(letra)+32) in BrailleDictionary.b_characters:    # condicion para contar mayusculas
            caracteres_imprimibles+= 1
            
        elif ord(letra) < 58 and ord(letra) > 47:        # Condicion para contar numeros
            caracteres_imprimibles+= 1
            
        else:
            if not letra == '\n':                         # deja el texto con saltos de linea
                
                text = text.replace(letra, '')            # Elimina del texto ingresado cualquier caracter que no este en el diccionario braille
            
            else:
                
               text = text.replace(letra, ' | ')      # Para marcar los saltos de linea
    
    words = text.split(' ')      # Separa el texto por palabras y son agregadas a la lista words
    text = ''       # reinicia variable text
    
    #print('control 2')        # print de control
    
    for i, palabra in enumerate(words):  # for para agregar identificadores de mayuscula o numero para formato braille
        
        for j, letra in enumerate(palabra):            # '«' para mayusculas, '»' para numeros
        
            if chr(ord(letra)+32) in BrailleDictionary.b_characters:
                
                words[i] = words[i].replace(letra, '«' + letra, 1)      # Mayusculas
                caracteres_totales_Braille+= 1
                
                words[i] = words[i].lower()            # Transforma mayusculas a minusculas
                break
                
            if ord(letra) > 47 and ord(letra) < 58:
                
                words[i] = palabra.replace(letra, '»' + letra, 1)      # Numeros
                caracteres_totales_Braille+= 1
                
                try:                                                 # try para cambiar notacion 'er' a 'r' para representar ordinal, para esto tiene que encontrar un numero seguido por 'er' como: 1er
                    
                    if palabra[j+1] == 'e' and palabra[j+2] == 'r':   # ordinal er
                        
                        words[i] = words[i].replace('er', 'r')
                        caracteres_imprimibles-= 1
                        
                except:
                    
                    break
                
                if palabra[len(palabra) - 1] == 'K':        # Condicion para Ruts que terminen en -K
                    
                    words[i] = words[i].replace(palabra[len(palabra) - 1], '«' + chr(ord(palabra[len(palabra) - 1]) + 32), 1)
                    caracteres_totales_Braille+= 1
                
                break
            
    #print('control 3')        # print de control
    #print(words)
    
    for i in range(len(words)):                                        # convierte numeros a letras, segun equivalencia en braille
        for j in range(len(words[i])):
            if ord(words[i][j]) < 58 and ord(words[i][j]) > 47:
                if ord(words[i][j]) == 48:
                    words[i] = words[i].replace(words[i][j], chr(ord(words[i][j]) + 58))   # para 1 a 9
                else:
                    words[i] = words[i].replace(words[i][j], chr(ord(words[i][j]) + 48))   # para el 0
    
    #print('control 4')        # print de control
    #print(words)
    
    cont = 0
    
    while cont < len(words):                            # Elimina espacios y caracteres en blanco innecesarios
        
        if words[cont] == '' or words[cont] == ' ':
            words.pop(cont)
            cont-= 1
    
        cont+= 1
    
    ##############################################################
    
    # La siguiente parte separa el texto de acuerdo a los saltos de linea presentes
    # y un limite de 30 letras por linea horizontal, para no cortar palabras si queda en el limite de los 30 caracteres
    
    words_temp = []  # array para guardar texto en formato con saltos de linea
    words_aux = []   # array para guardar palabras hasta que se presenta un salto de linea
    words_sum = 0    # suma de palabras para que no se corten cuando acabe la linea de 30 caracteres
    jump_count = words.count('|') + 1   # contador de saltos de linea
    iterations = 0                  # iterador variable
    
    #print('control 5')        # print de control
    #print(words)
    
    while iterations < jump_count:         
        for j, palabra in enumerate(words):
            
            words_sum+= len(palabra) + 1       # + 1 por el espacio entre palabras que tambien cuenta como caracter    
            
            if palabra == '|': 
                words = words[j + 1:]
                break
            
            if selected_sheet_size == 'Carta' or selected_sheet_size == 'Oficio':
            
                if words_sum > 31:
                    iterations-= 1
                    words = words[j:]
                    break
            
            if selected_sheet_size == 'A4':
            
                if words_sum > 30:
                    iterations-= 1
                    words = words[j:]
                    break
                
            words_aux.append(palabra)
    
        words_temp.append(words_aux)
        words_sum = 0
        words_aux = []
        iterations+= 1
    
    #print('control 6')        # print de control
    #print(words_temp)
    
    words = []
    
    for i in range(len(words_temp)):
        words.append(' '.join(words_temp[i]))
    
    caracteres_imprimibles-= 1                                 # (caracteres_imprimibles-1) compensacion por el espacio agregado
    caracteres_totales_Braille+= caracteres_imprimibles        # a la cantidad de caracteres totales suma el espacio para indicar mayusculas y numeros
    
    words_temp = []  # array para guardar texto en formato con saltos de linea
    words_aux = []
    
    #print('control 7')        # print de control
    
    return caracteres_imprimibles, caracteres_totales_Braille, words

def make_dot(array, posi, posj, dot_exists, function):              # Funcion para crear punto segun radio
    
    if dot_exists == '1' and function == 'preview':         # crea un punto solo si se lo requiere ``` dot_exist == '1' con radio si viene de la funcion preview
        for i in range(posi - radius, posi + radius):
            for j in range(posj - radius, posj + radius):
                if ((i-posi)**2 + (j-posj)**2) < (radius**2):      # Condicion para poner un 0 solo si la coordenada i, j esta dentro del perimetro del circulo
                    array[i][j] = 0
                    
    elif dot_exists == '0' and function == 'preview':  # elif de uso interno
        array[posi][posj] = 0
    
    elif dot_exists == '1' and function == 'printtest':  # elif de uso interno
        array[posi][posj] = 0
    
    elif dot_exists == '1' and function == 'print': # para imprimir braille
        #array[posi][posj] = 1
        return posj, posi       # se cambia posicion posi por posj y viceversa, por formato cartesiano de G-code
    
    else: return -1, -1

def make_images(printable_text, printable_braille_characters, function):
    
    # limites horizontales y verticales de la hoja seleccionada en mm*10
    horizontal_limit = PaperSheets.sheet_size[selected_sheet_size][0]*10 - (margin_h + dot_spacing_h)
    vertical_limit = PaperSheets.sheet_size[selected_sheet_size][1]*10 - (margin_v + dot_spacing_v*2)
    
    # Cantidad de caracteres que caben horizontal y verticalmente en la hoja seleccionada
    horizontal_characters = math.ceil(((PaperSheets.sheet_size[selected_sheet_size][0]*10) - (2*margin_h)) / character_spacing_h)
    vertical_characters = math.ceil(((PaperSheets.sheet_size[selected_sheet_size][1]*10) - (2*margin_v)) / character_spacing_v)
    # numero total de paginas
    n_pages = math.ceil(len(printable_text) / vertical_characters)
    
    temp_text = printable_text
    
    '''
    # uso interno
    for line in range(len(printable_text)):
        printable_text[line] = printable_text[line] [::-1]
    '''
    
    # Offset horizontal agregado por diferencia de medidas entre medidas oficiales y placa para escribir braille, 
    # si quiere quitar el offset comente la casilla offset_h = round((1766 - 1740) / horizontal_characters)
    # y descomente la casilla offset_h = 0
    
    offset_h = round((1766 - 1740) / horizontal_characters)   # 1766 medida horizontal de caracter 1 a 30 sobre el primer punto del mismo (Pizarra braille)
    #offset_h = 0                                               # 1740 medida oficial horizontal de caracter 1 a 30 sobre el primer punto del mismo
    
    #print('Numero de procesadores: ', mp.cpu_count()//2)
    
    #pool = mp.Pool(mp.cpu_count()//2)
  
    for page in range(n_pages):
       
        # Matriz base para imprimir en braille
        temp_sheet = np.ones(((PaperSheets.sheet_size[selected_sheet_size][1]*10), (PaperSheets.sheet_size[selected_sheet_size][0]*10)), dtype = int)
        
        character = ''
    
        for cont_char_text_v, i in enumerate(range(margin_v, vertical_limit, character_spacing_v)):                # hasta el termino de este for, se crean los puntos braille
            
            if cont_char_text_v == len(printable_text): break # detiene el for principal cuando llega al final del texto
           
            
            for cont_char_text_h, j in enumerate(range((margin_h - (offset_h * horizontal_characters) // 2), horizontal_limit, character_spacing_h)):
            #for cont_char_text_h, j in enumerate(range((horizontal_limit - 1 - (offset_h * horizontal_characters) // 2), margin_h - (offset_h * horizontal_characters) // 2, -character_spacing_h)):
                
                if cont_char_text_h == len(printable_text[cont_char_text_v]):  # detiene for secundario cuando se acaban las palabras de una linea
                    break
                
                character = printable_text[cont_char_text_v][cont_char_text_h]
                
                make_dot(temp_sheet, i, j + (cont_char_text_h * offset_h), BrailleDictionary.b_characters[character][0], function)                    # solo se crea un punto si hay un '1' presente en el formato braille en el diccionario
                
                make_dot(temp_sheet, i, j + dot_spacing_h + (cont_char_text_h * offset_h), BrailleDictionary.b_characters[character][1], function)
                
                make_dot(temp_sheet, i + dot_spacing_v, j + (cont_char_text_h * offset_h), BrailleDictionary.b_characters[character][2], function)
                
                make_dot(temp_sheet, i + dot_spacing_v, j + dot_spacing_h + (cont_char_text_h * offset_h), BrailleDictionary.b_characters[character][3], function)
                
                make_dot(temp_sheet, i + dot_spacing_v*2, j + (cont_char_text_h * offset_h), BrailleDictionary.b_characters[character][4], function)
                
                make_dot(temp_sheet, i + dot_spacing_v*2, j + dot_spacing_h + (cont_char_text_h * offset_h), BrailleDictionary.b_characters[character][5], function)
            
            if cont_char_text_v == vertical_characters:     # detiene el for principal cuando la cantidad de lineas verticales igualan a la cantidad maxima de lineas verticales de la hoja
                break
            
        printable_text = printable_text[vertical_characters:]     # recorta el array de texto a la cantidad de linesas maximas verticales soportadas por la hoja
        
        # guarda el array generado como imagen en carpeta temporal
        plt.imsave("temp/images/Braille_view_" + str(page + 1) + ".png",temp_sheet,vmin=0,vmax=1)      #guarda imagen generada, 1 es blanco, 0 es negro
        
        #unique, counts = np.unique(temp_sheet, return_counts=True)
        #print(counts[0].item())
        
        ############### Para agregar letras a imagen #################
        
        # Flag para detectar numeros
        is_number = False
        
        letter_numbers_list = ['j', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']   # array para imprimir numeros sobre los caracteres braille que correspondan
        
        editable_image_0 = Image.open("temp/images/Braille_view_" + str(page + 1) + ".png")
        editable_image_1 = ImageDraw.Draw(editable_image_0)        # para dibujar caracteres normales en en imagen
        
        for cont_char_text_v, i in enumerate(range(margin_v, vertical_limit, character_spacing_v)):                # hasta el termino de este for, se crean los puntos braille
        
            if cont_char_text_v == len(temp_text): break             # detiene el for principal cuando llega al final del texto
        
            for cont_char_text_h, j in enumerate(range(margin_h - (offset_h * horizontal_characters) // 2, horizontal_limit, character_spacing_h)):
            #for cont_char_text_h, j in enumerate(range((horizontal_limit - 1 - (offset_h * horizontal_characters) // 2), margin_h - (offset_h * horizontal_characters) // 2, -character_spacing_h)):   
                
                if cont_char_text_h == len(temp_text[cont_char_text_v]):   # detiene for secundario cuando se acaban las palabras de una linea
                    break
                
                character = temp_text[cont_char_text_v][cont_char_text_h]
                
                if is_number:
                    
                    try:
                        character = str(letter_numbers_list.index(character))
                        
                    except:
                        pass
                    
                editable_image_1.text((j + ((dot_spacing_h - font_size)//2 + (cont_char_text_h * offset_h)), i - (radius + 30)), character, fill = (0, 0, 0), font = top_font)
                
                if character == '»':      # activa el flag para indicar que la palabra tiene numeros
                    is_number = True
                    
                if character == '«' or ord(character) > 96 and ord(character) < 123 or character == 'ñ' or character == ' ':  # resetea is_number cuando encuentra un caracter que no es un numero, o cuendo empieza una nueva palabra
                    is_number = False
                
            if cont_char_text_v == vertical_characters:
                break
        
        editable_image_0.save("temp/images/Braille_view_" + str(page + 1) + ".png")
        
        temp_text = temp_text[vertical_characters:]
        
        
class ViewImages(object):
    
    def __init__(self, parent_frame, dir_text):
        
        self.parent_frame = parent_frame
        self.direction_text = save_route + dir_text + '/'
        self.image_list = os.listdir('temp/images')    # carga imagenes a una lista
        self.image_list.sort(key = len)                 # ordena la lista de imagenes por el largo del string
        self.image_count = 0
        self.sheet_size_divisor = 0.125         # 0.125
        
        mixer.stop()
        self.wait_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav').play()
    
        self.path01 = ''         # Variable para cambiar direccion de imagenes segun contraste
    
        if contrast_state:
           self.path01 = 'hc/'
    
        if not contrast_state:
            self.path01 = ''
        
        self.save_img = resize_icon('icons/' + self.path01 + 'guardar.png', 2.5, 'icon')
        self.close_icon = resize_icon('icons/' + self.path01 + 'icon02.png', 2.5, 'icon')
        self.back_image = resize_icon('icons/' + self.path01 + 'atras.PNG', 1.5, 'icon')
        self.forward_image = resize_icon('icons/' + self.path01 + 'adelante.PNG', 1.5, 'icon')
        
        self.preview_window = tk.Toplevel()
        self.preview_window.title("Vista Preliminar...")
        self.preview_window.iconphoto(False, tk.PhotoImage(file='icons/window_icon.png'))
        self.preview_window.resizable(0,0)
        self.preview_window.grab_set()
        
        self.Bar_1 = tk.Frame(self.preview_window, bg = background_color)       # Frame superior de labels
        self.Bar_2 = tk.Frame(self.preview_window, bg = background_color)       # Frame de botones medios
        self.Bar_3 = tk.Frame(self.preview_window, bg = background_color)       # Frame de botones inferiores
        
        self.Bar_1.pack(side = 'top', fill = 'x')
        self.Bar_2.pack(side = 'top', fill = 'x')
        self.Bar_3.pack(side = 'bottom', fill = 'x')
        
        ################### Bar_1 ###################
        
        # Boton para guardar imagenes
        self.boton_guardar = tk.Button(self.Bar_1, image = self.save_img, bg = button_color, command=lambda:save_images(self))
        CreateToolTip(self.boton_guardar, "Guardar imágenes.<Control-s>", 'sounds/guardar_imagenes_spanish_penelope.mp3')
        
        # Label para numero de imagen
        self.label_1 = tk.Label(self.Bar_1, text = (str(self.image_count + 1) + ' / ' + str(len(self.image_list))), font =(text_font, round(text_font_size*1.3)), bg = button_color)    
         # Boton cerrar ventana
        self.Boton_close = tk.Button(self.Bar_1, image = self.close_icon, bg = button_color, command=lambda:[__destroy__(self), close_windows(self.preview_window)]) 
        CreateToolTip(self.Boton_close, "Cerrar Ventana.<Escape>", "sounds/cerrar_ventana_spanish_penelope.mp3")
        
        self.boton_guardar.pack(side = "left", padx=button_separation_X)
        self.label_1.pack(side = "left", expand = True, padx=button_separation_X)
        self.Boton_close.pack(side = "left", padx=button_separation_X, pady=button_separation_Y)
        
        ################### Bar_2 ###################
    
        self.braille_img = resize_icon('temp/images/' + self.image_list[self.image_count], (self.sheet_size_divisor), 'image')
        
        # Boton atras
        self.back_button = tk.Button(self.Bar_2, image = self.back_image, bg = button_color, command=lambda:previous_image(self))
        CreateToolTip(self.back_button, 'Imagen\nAnterior', 'sounds/anterior_img_spanish_penelope.mp3')
        
        self.Bar_1.update()
        
        # Label donde se muestra la imagen
        self.image_label = tk.Label(self.Bar_2, image = self.braille_img)
        #self.image_label = Label(self.Bar_2, image = self.braille_img, width = self.braille_img.width(), height = (self.braille_img.height()//2))
        
        ######################################
        
        # Boton adelante
        self.forward_button = tk.Button(self.Bar_2, image = self.forward_image, bg = button_color, command=lambda:next_image(self))
        CreateToolTip(self.forward_button, 'Imagen\nSiguiente', 'sounds/siguiente_img_spanish_penelope.mp3')
        
        # Packs
        self.back_button.pack(side = "left", padx=button_separation_X/2)
        self.image_label.pack(side = 'left', expand = True)
        self.forward_button.pack(side = "left", padx=button_separation_X/2)
        
        ################### Bar_3 ###################
        
        # Label para nombre de imagen
        self.label_2 = tk.Label(self.Bar_3, text = ('Imagen: ' + self.image_list[self.image_count]), font =(text_font, text_font_size), bg = button_color)
        self.label_2.pack(pady=button_separation_Y, expand = True)
        
        #############################################
        # binds para teclas
        
        self.preview_window.bind('<Control-s>', lambda event: save_images(self))
        self.preview_window.bind('<Escape>', lambda event: [__destroy__(self), close_windows(self.preview_window)])
        self.preview_window.bind('<Left>', lambda event: previous_image(self))
        self.preview_window.bind('<Right>', lambda event: next_image(self))
        
        ############################################
        
        # Configuraciones adicionales
        self.preview_window.protocol("WM_DELETE_WINDOW", False)
        center(self.parent_frame, self.preview_window)
        self.preview_window.focus_force()
        self.preview_window.update()
        
        ################################################
        
        def previous_image(self):
            
            previous_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
            previous_audio.play()
            
            if self.image_count == 0:
                self.image_count = len(self.image_list)
            
            self.image_count-= 1
            
            self.label_1.config(text = (str(self.image_count + 1) + ' / ' + str(len(self.image_list))))
            self.braille_img = resize_icon('temp/images/' + self.image_list[self.image_count],(self.sheet_size_divisor), 'image')
            self.image_label.config(image = self.braille_img)
            self.label_2.config(text = ('Imagen: ' + self.image_list[self.image_count]))
        
        def next_image(self):
            
            next_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
            next_audio.play()
            
            self.image_count+= 1
            
            if self.image_count == len(self.image_list):
                self.image_count = 0
            
            self.label_1.config(text = (str(self.image_count + 1) + ' / ' + str(len(self.image_list))))
            self.braille_img = resize_icon('temp/images/' + self.image_list[self.image_count], (self.sheet_size_divisor), 'image')
            self.image_label.config(image = self.braille_img)
            self.label_2.config(text = ('Imagen: ' + self.image_list[self.image_count]))
            
        def save_images(self):
            
            save_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
            save_audio.play()
            
            if not os.path.exists(save_route):
                os.mkdir(save_route)
                
            elif os.path.exists(save_route):
                
                if not os.path.exists(self.direction_text):
                    os.mkdir(self.direction_text)
                    
                elif os.path.exists(self.direction_text):
                    shutil.rmtree(self.direction_text)
                    time.sleep(1)
                    os.mkdir(self.direction_text)
            #print('control')
            
            #os.mkdir(save_route + self.direction_text)
            time.sleep(1)
            
            for files in self.image_list:
                shutil.copy2(os.path.join('temp/images/', files), self.direction_text)
                
            mixer.Sound('sounds/img_guardadas_satis_spanish_penelope.mp3').play()
              
        def __destroy__(self):   # Evita la coleccion de basura
            
            destroy = mixer.Sound('sounds/cerrar_ventana_sfx.wav')
            destroy.play()
            
            self.braille_img = None
                    
def normalize(s):            # para normalizar palabras (quitar tildes, espacios y caracteres que no son admitidos al crer un archivo o carpeta en windows 10)  ñandu

    for letter in s:
        if letter == BrailleDictionary.normalized_characters[letter]:
            continue
        else:
            if letter in BrailleDictionary.normalized_characters:
                s = s.replace(letter, BrailleDictionary.normalized_characters[letter])
            elif letter not in BrailleDictionary.normalized_characters:
                s = s.replace(letter, "_")
    return s

def preview(frame, input_text_box):                                   # Terminar

    global last_sheet_selected    
    
    button_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    button_audio.play()
    
    text = ' '
    dir_text = ''
    text = input_text_box.get("1.0", tk.END)
    
    caracteres_totales = 0    

    if len(text) > 1:
        
        if len(text) > 20:
            dir_text = normalize(text[:20])               # para crear directorio con las primeras 20 letras del texto ingresado
        
        elif len(text) <= 20:
            dir_text = normalize(text[:len(text) - 1])
        
        #print(dir_text)
        
        caracteres_totales = len(text)
        
        if not os.path.exists('temp/images'):        # Condicion para no volver a hacer imagenes si no se ha hecho un cambio en el texto
        
            os.mkdir('temp/images')
        
        if input_text_box.edit_modified() or last_sheet_selected != selected_sheet_size:
            
            last_sheet_selected = selected_sheet_size    
        
            shutil.rmtree('temp/images')
            os.mkdir('temp/images')
            
            for char in text:
                if char == '\n':
                    caracteres_totales-= 1
    
            wait = WaitPlease(frame)
           
            #start_time = time.process_time()
            
            caracteres_imprimibles, printable_braille_characters, printable_text = text_eval(text)
            
            '''
            print(' Caracteres Ingresados: ', caracteres_totales)
            print(' Caracteres Imprimibles: ', caracteres_imprimibles)
            print(' Total de Caracteres Braille: ', printable_braille_characters)
            
            result = str(caracteres_totales) + 'Caracteres Ingresados, ' + str(caracteres_imprimibles) + 'Caracteres Imprimibles y, ' + str(printable_braille_characters) + 'Total de Caracteres Braille a imprimir'
            select_tts(frame, result)
            '''
            #print(' Texo Interno Resultante: ', printable_text)
    
            ########### Para configurar ventana donde se van a mostrar las imagenes #####################
    
            #height = frame.winfo_height()
            #width = round(height*(PaperSheets.sheet_size[selected_sheet_size][0]/PaperSheets.sheet_size[selected_sheet_size][1]))
            
            #######################################################################################################
            
            make_images(printable_text, printable_braille_characters, 'preview')  # Crea las imagenes para la visualizacion # 'preview' por defecto
            
            #end_time = time.process_time()
        
            wait.destroy_wait()
            
            #print('Inicio: ' + str(start_time) + ' s\nTermino: ' + str(end_time) + ' s\nDuracion: ' + str(end_time - start_time) + ' s')
            
            ViewImages(frame, dir_text)
            
            input_text_box.edit_modified(False)   # resetea el flag a false.
            
        else:
            ViewImages(frame, dir_text)
        
            # Caben 31 x 26 (806) caracteres en una hoja carta  (Ancho x Alto)
            # Caben 31 x 31 (961) caracteres en una hoja oficio  (Ancho x Alto)
            # Caben 30 x 28 (840) caracteres en una hoja A4  (Ancho x Alto)
        
def erase_text(input_text_box):
    
    button_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    button_audio.play()
    time.sleep(0.5)
    input_text_box.delete("1.0", tk.END)
    mixer.stop()
    var = mixer.Sound('sounds/borrado_exitoso_spanish_penelope.mp3')
    var.play()
    
    input_text_box.focus_force()

def close_windows(frame):
    
    frame.destroy()
    mixer.stop()
    settings_audio = mixer.Sound('sounds/cerrar_ventana_sfx.wav')
    settings_audio.play()

class Settings(object):
    
    def __init__(self, widget):
        
        mixer.stop()
        settings_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
        settings_audio.play()
        
        self.parent_frame = widget
        
        if not contrast_state:
            self.icon21 = resize_icon('icons/uno.png', 0.8, 'icon')      # Reescalado de icono con factor de ajuste individual
            self.icon22 = resize_icon('icons/dos.png', 0.8, 'icon')      # Reescalado de icono con factor de ajuste individual
            self.icon23 = resize_icon('icons/tres.png', 0.8, 'icon')      # Reescalado de icono con factor de ajuste individual
            self.icon24 = resize_icon('icons/info.png', 2.5, 'icon')
            self.icon25 = resize_icon('icons/icon02.png', 2.5, 'icon')
            
        elif contrast_state:
            self.icon21 = resize_icon('icons/hc/uno.png', 0.8, 'icon')      # Reescalado de icono con factor de ajuste individual
            self.icon22 = resize_icon('icons/hc/dos.png', 0.8, 'icon')      # Reescalado de icono con factor de ajuste individual
            self.icon23 = resize_icon('icons/hc/tres.png', 0.8, 'icon')      # Reescalado de icono con factor de ajuste individual
            self.icon24 = resize_icon('icons/hc/info.png', 2.5, 'icon')
            self.icon25 = resize_icon('icons/hc/icon02.png', 2.5, 'icon')
        
        self.log = tk.Toplevel()
        self.log.title("Seleccionar Tamaño de hoja")
        self.log.iconphoto(False, tk.PhotoImage(file='icons/window_icon.png'))
        
        self.Bar_5 = tk.Frame(self.log, bg = background_color)       # Frame superior de labels
        self.Bar_5.pack(side = 'top', fill = 'x')
        
        self.Bar_6 = tk.Frame(self.log, bg = background_color)       # Frame de botones medios
        self.Bar_6.pack(fill = 'x')
        
        self.Bar_7 = tk.Frame(self.log, bg = background_color)       # Frame de botones inferiores
        self.Bar_7.pack(side = 'bottom', fill = 'x')
        
        ######## Bar_5 ######## 
        
        self.label_1 = tk.Label(self.Bar_5, text = 'Carta', font =(text_font, text_font_size), bg = button_color, width = icon_separation)
        self.label_1.pack(side = "left", expand = True, padx=button_separation_X, pady=button_separation_Y)
        
        self.label_2 = tk.Label(self.Bar_5, text = 'Oficio', font =(text_font, text_font_size), bg = button_color, width = icon_separation)
        self.label_2.pack(side = "left", expand = True, padx=button_separation_X, pady=button_separation_Y)
        
        self.label_3 = tk.Label(self.Bar_5, text = 'A4', font =(text_font, text_font_size), bg = button_color, width = icon_separation)
        self.label_3.pack(side = "left", expand = True, padx=button_separation_X, pady=button_separation_Y)
        
        ######## Bar_6 ######## 
        
        # Boton uno
        self.Boton_uno = tk.Button(self.Bar_6, compound = tk.BOTTOM, image= self.icon21, bg = button_color, command=lambda:sheet_selection(self, 'Carta')) 
        CreateToolTip(self.Boton_uno, "Boton para seleccionar\ntamaño Carta.<F1>", "sounds/seleccionar_carta_spanish_penelope.mp3")
        self.Boton_uno.pack(side = "left", expand = True, padx=button_separation_X, pady=button_separation_Y)
        
        # Boton dos
        self.Boton_dos = tk.Button(self.Bar_6, compound = tk.BOTTOM, image= self.icon22, bg = button_color, command=lambda:sheet_selection(self, 'Oficio')) 
        CreateToolTip(self.Boton_dos, "Boton para seleccionar\ntamaño Oficio.<F2>", "sounds/seleccionar_oficio_spanish_penelope.mp3")
        self.Boton_dos.pack(side = "left", expand = True, padx=button_separation_X, pady=button_separation_Y)
        
        # Boton tres
        self.Boton_tres = tk.Button(self.Bar_6, compound = tk.BOTTOM, image= self.icon23, bg = button_color, command=lambda:sheet_selection(self, 'A4')) 
        CreateToolTip(self.Boton_tres, "Boton para seleccionar\ntamaño A4.<F3>", "sounds/seleccionar_a4_spanish_penelope.mp3")
        self.Boton_tres.pack(side = "left", expand = True, padx=button_separation_X, pady=button_separation_Y)
        
        ######## Bar_7 ######## 
        
        self.label_4 = tk.Label(self.Bar_7, image= self.icon24, bg = button_color)
        self.label_4.pack(side = "left", padx=button_separation_X, pady=button_separation_Y)
        
        self.temp = ' '
        
        if selected_sheet_size == 'Carta':
            
            self.temp = 'sounds/carta_seleccionado_spanish_penelope.mp3'
            
        if selected_sheet_size == 'Oficio':
            
            self.temp = 'sounds/oficio_seleccionado_spanish_penelope.mp3'
            
        if selected_sheet_size == 'A4':
            
            self.temp = 'sounds/a4_seleccionado_spanish_penelope.mp3'
        
        CreateToolTip(self.label_4, 'Información.', self.temp)
        
        self.label_5 = tk.Label(self.Bar_7, text = 'Tamaño actual: ' + selected_sheet_size, font =(text_font, text_font_size), bg = button_color)
        self.label_5.pack(side = "left", padx=button_separation_X, pady=button_separation_Y)
        
        # Boton cerrar ventana
        self.Boton_close = tk.Button(self.Bar_7, compound = tk.BOTTOM, image= self.icon25, bg = button_color, command=lambda:close_windows(self.log)) 
        CreateToolTip(self.Boton_close, "Cerrar Ventana.<Escape>", "sounds/cerrar_ventana_spanish_penelope.mp3")
        self.Boton_close.pack(side = "right", padx=button_separation_X, pady=button_separation_Y)
        
        ########################
        
        self.log.bind('<Escape>', lambda event: close_windows(self.log))
        self.log.bind('<F1>', lambda event: sheet_selection(self, 'Carta'))
        self.log.bind('<F2>', lambda event: sheet_selection(self, 'Oficio'))
        self.log.bind('<F3>', lambda event: sheet_selection(self, 'A4'))
        
        center(self.parent_frame, self.log)       # Centrar ventana toplevel (log) en ventana main
        
        self.log.grab_set()
        self.log.focus_force()
    
        def sheet_selection(self, opt):
            
            global selected_sheet_size
            
            mixer.stop()
            
            if opt == 'Carta':
                var = mixer.Sound('sounds/carta_seleccionado_spanish_penelope.mp3')
                var.play()
                
                selected_sheet_size = opt
                
                time.sleep(1)
                
            if opt == 'Oficio':
                var = mixer.Sound('sounds/oficio_seleccionado_spanish_penelope.mp3')
                var.play()
                
                selected_sheet_size = opt
                
                time.sleep(1)
                
            if opt == 'A4':
                var = mixer.Sound('sounds/a4_seleccionado_spanish_penelope.mp3')
                var.play()
                
                selected_sheet_size = opt
                
                time.sleep(1)
            
            self.log.destroy()
            self.log.grab_release()
    
def closeApp(root, error):      # Funcion para detener los procesos del programa

    global sending_information

    if error:
        root.destroy()       # Destruye ventana principal
        
    if not error:
        
        if arduino_serial != None and arduino_serial.isOpen():   # cierra la conexion serial si esta abierta
        
            if sending_information:
                
                AlertMessages(root, 'Se está imprimiendo un documento,\n¿Desea SALIR de la aplicación?', 'sounds/advertencia_salir_spanish_penelope.mp3')
                
            else:
                
                arduino_serial.close()
                
                if recording:
                    stop_listening(wait_for_stop=False)
            
                stop_tts()           # Detiene el texto a voz, por si algo se esta reproduciendo
                close_windows(root)
                time.sleep(1)
                mixer.stop()         # Detiene mixer, por si se esta reproduciendo alguna descripcion de boton
                mixer.quit()         # Desinicializa mixer
                shutil.rmtree('temp/')   # Elimina la carpeta de archivos temporales al cerrar el programa
                # borra lo que contenga el archivo csv (truncar, lo deja sin contenido)
                sysfile = open('config/sysfile.csv', 'w+')
                sysfile.close()
                
        else:
                
            #arduino_serial.close()
                
            if recording:
                stop_listening(wait_for_stop=False)
            
            stop_tts()           # Detiene el texto a voz, por si algo se esta reproduciendo
            close_windows(root)
            time.sleep(1)
            mixer.stop()         # Detiene mixer, por si se esta reproduciendo alguna descripcion de boton
            mixer.quit()         # Desinicializa mixer
            shutil.rmtree('temp/')   # Elimina la carpeta de archivos temporales al cerrar el programa
            # borra lo que contenga el archivo csv (truncar, lo deja sin contenido)
            sysfile = open('config/sysfile.csv', 'w+')
            sysfile.close()
       
    
def center(parent, actual):                     # Funcion para centrar ventanas
    
    actual.update()
    actual_pos = "+" + str(((parent.winfo_width()-actual.winfo_width())//2)+parent.winfo_x()) + "+" + str(((parent.winfo_height()-actual.winfo_height())//2)+parent.winfo_y())
    actual.geometry(actual_pos)
    
def change_contrast(frame, input_text_box):    # funcion para cambiar el color de los elementos de la aplicacion
    
    global background_color
    global button_color
    global contrast_state
    
    contrast_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    contrast_audio.play()
    
    if not contrast_state:
        contrast_state = True
        background_color = 'black'
        button_color = 'yellow'
        
        ###################### Bar_1 ######################
        icon01 = resize_icon('icons/hc/icon01.png', 1, 'icon')    # Reescalado de icono con factor de ajuste individual, segundo argumento ==1 (tamano normal), <1 agrandar icono, >1 reducir icono
        icon02 = resize_icon('icons/hc/icon02.png', 1, 'icon')    
        icon03 = resize_icon('icons/hc/icon03.png', 1, 'icon')   
        icon04 = resize_icon('icons/hc/stop_tts.png', 1, 'icon')    
        icon05 = resize_icon('icons/hc/icon04.png', 1, 'icon')   
        icon06 = resize_icon('icons/hc/pausa.png', 1, 'icon')   
        icon07 = resize_icon('icons/hc/icon06.png', 1, 'icon')   
        
        ###################### Bar_2 ######################
        icon08 = resize_icon('icons/hc/letter_max.png', 2, 'icon')   
        icon09 = resize_icon('icons/hc/letter.png', 2, 'icon')     
        icon10 = resize_icon('icons/hc/letter_min.png', 2, 'icon')   
        icon11 = resize_icon('icons/hc/microphone.png', 2, 'icon')
        if recording:
            icon11 = resize_icon('icons/hc/microphone_rec.png', 2, 'icon')
        icon12 = resize_icon('icons/hc/contraste.png', 2, 'icon')     
        
        ###################### Bar_3 ######################
        icon13 = resize_icon('icons/hc/expand.png', 2, 'icon')      
        icon14 = resize_icon('icons/hc/shrink.png', 2, 'icon')
        icon15 = resize_icon('icons/hc/icon05_1.png', 2, 'icon')      
        icon16 = resize_icon('icons/hc/icon05_2.png', 2, 'icon')
        icon17 = resize_icon('icons/hc/settings.png', 2, 'icon')
        icon18 = resize_icon('icons/hc/erase_text.png', 2, 'icon')
        icon19 = resize_icon('icons/hc/redo.png', 2, 'icon')
        icon20 = resize_icon('icons/hc/undo.png', 2, 'icon')
        
    elif contrast_state:
        contrast_state = False
        background_color = 'gray60'
        button_color = 'gray90'
        
        ###################### Bar_1 ######################
        icon01 = resize_icon('icons/icon01.png', 1, 'icon')    # Reescalado de icono con factor de ajuste individual, segundo argumento ==1 (tamano normal), <1 agrandar icono, >1 reducir icono
        icon02 = resize_icon('icons/icon02.png', 1, 'icon')    
        icon03 = resize_icon('icons/icon03.png', 1, 'icon')   
        icon04 = resize_icon('icons/stop_tts.png', 1, 'icon')    
        icon05 = resize_icon('icons/icon04.png', 1, 'icon')   
        icon06 = resize_icon('icons/pausa.png', 1, 'icon')   
        icon07 = resize_icon('icons/icon06.png', 1, 'icon')   
        
        ###################### Bar_2 ######################
        icon08 = resize_icon('icons/letter_max.png', 2, 'icon')   
        icon09 = resize_icon('icons/letter.png', 2, 'icon')     
        icon10 = resize_icon('icons/letter_min.png', 2, 'icon')   
        icon11 = resize_icon('icons/microphone.png', 2, 'icon')
        if recording:
            icon11 = resize_icon('icons/microphone_rec.png', 2, 'icon')
        icon12 = resize_icon('icons/contraste.png', 2, 'icon')     
        
        ###################### Bar_3 ######################
        icon13 = resize_icon('icons/expand.png', 2, 'icon')      
        icon14 = resize_icon('icons/shrink.png', 2, 'icon')
        icon15 = resize_icon('icons/icon05_1.png', 2, 'icon')      
        icon16 = resize_icon('icons/icon05_2.png', 2, 'icon')
        icon17 = resize_icon('icons/settings.png', 2, 'icon')
        icon18 = resize_icon('icons/erase_text.png', 2, 'icon')
        icon19 = resize_icon('icons/redo.png', 2, 'icon')
        icon20 = resize_icon('icons/undo.png', 2, 'icon')
    
    image_list = [icon01, icon02, icon03, icon04, icon05, icon06, icon07, icon08, icon09, icon10, 
                  icon11, icon12, icon13, icon14, icon16, icon15, icon20, icon19, icon18, icon17]
    
    button_cont = 0
    
    frame.configure(bg = background_color)
    for bar in frame.winfo_children():
        bar.configure(bg = background_color)
        for widget in bar.winfo_children():
            if 'button' in str(widget).split(".")[-1]:
                    widget.configure(image = image_list[button_cont])
                    widget.image = image_list[button_cont]
                    button_cont+= 1
            if 'label' in str(widget).split(".")[-1]:
                if widget.cget("text") == 'Impresora Conectada.     ' or widget.cget("text") == 'Impresora Desconectada.':
                    continue
                if widget.cget("text") == 'A':
                    widget.configure(bg = button_color)
                    button_cont+= 1
                    continue
                else:
                    widget.configure(bg = background_color)
            else:
                if 'frame' in str(widget).split(".")[-1]:
                    input_text_box.config(bg = button_color)
                widget.configure(bg = button_color)

def directory_check():
    
    # comprueba la existencia del directorio de archivos temporales, si no lo encuentra, lo crea.
    
    if not os.path.exists('temp'):
        os.mkdir('temp')
        os.mkdir('temp/audio')
        os.mkdir('temp/images')

    if not os.path.exists('icons'):
        tk.messagebox.showerror('Error!', 'No se han encontrado algunos archivos necesarios\n para el buen fucnionamiento de la aplicación.')
        #closeApp(frame, True)
        
    if not os.path.exists('sounds'):
        tk.messagebox.showerror('Error!', 'No se han encontrado algunos archivos necesarios\n para el buen fucnionamiento de la aplicación.')
        #closeApp(frame, True)


def speech_recognition(Boton_voz, input_text_box):     # Funcion para recoconimiento de voz

    global recording
    global stop_listening
    
    rec_img = resize_icon('icons/microphone_rec.png', 2, 'icon')
    
    if check_internet_connection():      # esta funcion necesita conexion a internet, por lo que comprueba la conexion primero
    
        if recording:        # si se esta ocupando el microfono, al presionar el boton de nuevo, se apaga el microfono
        
            rec_img = resize_icon('icons/microphone.png', 2, 'icon')     # configuracion para cambiar la imagen del boton
                        
            Boton_voz.configure(image = rec_img)
            Boton_voz.image = rec_img
        
            stop_listening(wait_for_stop=False)
            
            mixer.Sound('sounds/cerrar_ventana_sfx.wav').play()
            
            recording = False
            
            return
        
        elif not recording:
        
            time.sleep(0.5)
            
            #r = sr.Recognizer()
            
            try:
             
                with sr.Microphone() as source:
            
                    r.adjust_for_ambient_noise(source, duration = 3)
                    
                def recognize_worker(recognizer, audio):
                    
                    global recording
                    
                    try:
                    
                        #audio = r.listen(source, timeout = 3, phrase_time_limit = 3)
                        
                        text = r.recognize_google(audio, language="es-ES")
                        
                        input_text_box.insert(tk.END, text)
                        
                        #mixer.Sound('sounds/cerrar_ventana_sfx.wav').play()
                    
                    except:
                        
                        stop_listening(wait_for_stop=False)
                        
                        #global recording
                        recording = False
                        
                        rec_img = resize_icon('icons/microphone.png', 2, 'icon')
                        
                        Boton_voz.configure(image = rec_img)
                        Boton_voz.image = rec_img
                        
                        mixer.Sound('sounds/no_entendi_spanish_penelope.mp3').play()
                
                mixer.Sound('sounds/ventana_emergente_sfx.wav').play()
                
                Boton_voz.configure(image = rec_img)
                Boton_voz.image = rec_img
                
                #global recording
                #global stop_listening
                
                recording = True
                
                stop_listening = r.listen_in_background(sr.Microphone(), recognize_worker, phrase_time_limit = 3)
            
            except:
                mixer.Sound('sounds/no_mic_spanish_penelope.mp3').play()
            
        elif not check_internet_connection():
            mixer.Sound('sounds/necesito_internet_spanish_penelope.mp3').play()
            
class AlertMessages(object):
    
    def __init__(self, frame, message, audio):
        
        self.image1 = resize_icon('icons/option_cancel.png', 0.5, 'icon')
        self.image2 = resize_icon('icons/option_yes.png', 0.5, 'icon')
        
        self.log = tk.Toplevel()
        self.log.iconphoto(False, tk.PhotoImage(file='icons/window_icon.png'))
        self.log.resizable(0,0)
        self.log.title("Seleccione una opción...")
        self.log.configure(bg = background_color)
        
        self.message = message
        self.audio = audio
        self.frame = frame
        
        self.frame1 = tk.Frame(self.log, bg = background_color)
        self.frame1.pack(side = "top", padx = button_separation_X, pady = button_separation_Y)
        
        self.frame2 = tk.Frame(self.log, bg = background_color)
        self.frame2.pack(side = "top", pady = button_separation_Y)
        
        self.label_1 = tk.Label(self.frame1, text = self.message, font =(text_font, text_font_size*2), bg = button_color)
        self.label_1.pack(side = "left")
        
        self.button_1 = tk.Button(self.frame2, image = self.image1, bg = button_color, command=lambda:self.__destroy__('sounds/cerrar_ventana_sfx.wav'))
        CreateToolTip(self.button_1, "No.", "sounds/no_spanish_penelope.mp3")
        self.button_1.pack(side = "left")
        
        self.label = tk.Label(self.frame2, bg = background_color)
        self.label.pack(side = "left", padx = button_separation_X*2)
        
        self.button_2 = tk.Button(self.frame2, image = self.image2, bg = button_color, command=lambda:self.play_action())
        CreateToolTip(self.button_2, "Si.", "sounds/si_spanish_penelope.mp3")
        self.button_2.pack(side = "left")
        
        center(self.frame, self.log)
        self.log.update()
        self.log.grab_set()
        self.log.focus_force()
        self.log.protocol("WM_DELETE_WINDOW", False)
        
        self.log.bind('<Escape>', lambda event: self.__destroy__('sounds/cerrar_ventana_sfx.wav'))
        self.log.bind('<Return>', lambda event: self.play_action())
        
        mixer.Sound(audio).play()
        
    def play_action(self):
        
        global sending_information
        global pause_signal
        global cancel_signal
        global pause_row
        
        #print('control1')
        
        if 'IMPRIMIR' in self.message and not sending_information:
            
            ########### Threads ###########
     
            # Thread para enviar datos a arduino
            t1 = threading.Thread(name = 'communication', target = communication_module, args = (self.frame,))
            
            # thread para recibir datos de arduino
            t2 = threading.Thread(name = 'callbacks', target = get_callbacks)
            
            t1.start()
            t2.start()
            
            if not pause_signal and printer_connection_status:
                
                #mixer.Sound('sounds/imprimiendo_spanish_penelope.mp3').play()
                self.__destroy__('sounds/imprimiendo_spanish_penelope.mp3')
            
            elif pause_signal:
                
                #mixer.Sound('sounds/reanudada_spanish_penelope.mp3').play()
            
                pause_signal = False
            
                self.__destroy__('sounds/reanudada_spanish_penelope.mp3')
            
        elif 'PAUSAR' in self.message:
         
            #mixer.Sound('sounds/pausada_spanish_penelope.mp3').play()
         
            #pause_audio = None
            
            pause_signal = True
            self.__destroy__('sounds/pausada_spanish_penelope.mp3')
            
        elif 'CANCELAR' in self.message:
           
            #mixer.Sound('sounds/cancelada_spanish_penelope.mp3').play()
            
            #cancel_audio = None
            pause_row = 0
            sending_information = False
            cancel_signal = True
            #sending_information = False
            self.__destroy__('sounds/cancelada_spanish_penelope.mp3')
            
        elif 'SALIR' in self.message:

            self.__destroy__('sounds/cerrar_ventana_sfx.wav')
            
            arduino_serial.write('endprint\n'.encode('ascii'))
            
            sending_information = False
            cancel_signal = True
                
            if recording:
                stop_listening(wait_for_stop=False)
            
            stop_tts()           # Detiene el texto a voz, por si algo se esta reproduciendo
            close_windows(self.frame)
            time.sleep(1)
            mixer.stop()         # Detiene mixer, por si se esta reproduciendo alguna descripcion de boton
            mixer.quit()         # Desinicializa mixer
            shutil.rmtree('temp/')   # Elimina la carpeta de archivos temporales al cerrar el programa
            # borra lo que contenga el archivo csv (truncar, lo deja sin contenido)
            sysfile = open('config/sysfile.csv', 'w+')
            sysfile.close()
            #arduino_serial.close()
            
        elif 'problema' in self.message:
    
            arduino_serial.write('endprint\n'.encode('ascii'))
            arduino_serial.write('breakpause\n'.encode('ascii'))
            pause_row = 0
            sending_information = False
            cancel_signal = True
            self.__destroy__('sounds/cerrar_ventana_sfx.wav')
        
    def __destroy__(self, specefic_sound):
        
        mixer.stop()
        #mixer.Sound('sounds/cerrar_ventana_sfx.wav').play()
        self.log.destroy()
        
        mixer.Sound(specefic_sound).play()

        
def cancel_print(root):
    
    button_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    button_audio.play()
    
    if sending_information:
    
        AlertMessages(root, '¿Desea CANCELAR la impresión?', 'sounds/desea_cancelar_spanish_penelope.mp3')
    

def pause_print(root):
    button_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    button_audio.play()
    
    if sending_information:
        
        AlertMessages(root, '¿Desea PAUSAR la impresión?', 'sounds/desea_pausar_spanish_penelope.mp3')
    

def get_callbacks():           # Funcion para recibir callbacks desde arduino
    global callback
    if printer_connection_status and arduino_serial.isOpen():
        while sending_information:
            
            callback = arduino_serial.readline().decode('ascii').strip()
            
            '''
            if callback == 'revisar_hoja':
                break
            
            try:
                
                #print(arduino_serial.readline().decode('ascii').strip())
                
                if arduino_serial.readline().decode('ascii').strip() == 'waiting':
                    callback = 'waiting'
                    #print(callback)
                    
                elif arduino_serial.readline().decode('ascii').strip() == 'busy':
                    callback = 'busy'
                
                elif arduino_serial.readline().decode('ascii').strip() == 'revisar_hoja':
                    
                    callback = 'revisar_hoja'
                    
                    print("################")
                    print(callback)
                    print("################")
                    break
                
            except:
                pass
            
    return
'''
def support_for_communication(row):   # funcion que envia informacion segun el callback que retorne arduino   
    
    global cancel_signal
    time.sleep(3) 

    if callback == 'waiting':
        
        if not cancel_signal:
            #print(" ", callback, " ", row)
            arduino_serial.write(row.encode('ascii'))
            
            if row == 'endprint\n':
                
                mixer.Sound('sounds/finalizada_spanish_penelope.mp3').play()  
                
            return
        
        else: 

            return
    
    elif callback == 'finish' or callback == 'revisar_hoja':
        
        cancel_signal = True
        
        return
    
    else:
        #print(callback)
        support_for_communication(row)

        
def communication_module(frame):      # funcion para enviar datos de impresion

    global pause_row
    global sending_information
    global cancel_signal
    global pause_signal
    
    if printer_connection_status and arduino_serial.isOpen():
        
        sending_information = True
        
    #if not printer_connection_status:
        
        # Envia string de configuracion
        config_print = 'config:' + str(PaperSheets.sheet_size[selected_sheet_size][1]) + '/' + str(margin_v/10) + '\n'
        arduino_serial.write(config_print.encode('ascii'))
        
        #print(config_print)
        
        with open('config/sysfile.csv') as csv_file:
            
            #csv_total_rows = len(list(csv_file))
            #print(csv_rows)
            #row_list = csv.reader(csv_file)
           
            for row_index, row in enumerate(csv_file):
                
                if pause_signal:
                    pause_row = row_index
                    break
                
                if cancel_signal and callback == 'waiting' or callback == 'revisar_hoja':
                    
                    arduino_serial.write('endprint\n'.encode('ascii'))
                    print("control")
                    cancel_signal = False
                    
                    if callback == 'revisar_hoja':
                        
                        AlertMessages(frame, '¡Hay un problema con la hoja!\nPor favor revise la impresora.\nPresione Enter o Escape para continuar.', 'sounds/revisar_hoja_spanish_penelope.mp3')
                        break
                    
                    break
                
                else:
                
                    if row_index < pause_row:
                        continue
                    
                    else:
                        
                        pause_signal = False
                        row_index = 0
                        
                        #print(callback, " ", row)
                        support_for_communication(row)
                    
                    #print(row_index, row)
        
        #pause_signal = False
        sending_information = False
        return
        
    else:
        #if not printer_connection_status or not arduino_serial.isOpen():
            #arduino_serial.write('endprint\n'.encode('ascii'))
        sending_information = False
        return


'''

########### Callbacks enviados desde arduino ###############

'waiting'   :   Arduino esta esperando a recibir informacion
'busy'      :   Arduino esta ejecutando una accion
'finish'    :   Arduino termino de imprimir un documento
'''
############################################################

# Esta funcion verifica la conexion de la impresora, abriendo el puerto serial cuando se conecta.
# Cerrandolo si esta abierto.
# se ejecuta cada 1 segundo (1000 milisegundos) para comprobar la conexion recurrentemente

def check_printer_connection(frame, label):

    global printer_connection_status    
    global arduino_serial
    
    #print('Control', myports)
    
    my_ports_hwid = []
    myports = serial.tools.list_ports.comports()

    if len(myports) > 0 and not printer_connection_status:
        
        for port, desc, hwid in sorted(myports):
            
            device_id = "{}".format(hwid)
      
            if device_id[:len(printer_id)] == printer_id:
                
                arduino_serial = serial.Serial("{}".format(port), 9600, timeout = 1)
                label.configure(text = 'Impresora Conectada.     ', font = (text_font, int(text_font_size//1.3)), bg = 'green', fg = 'white')
                mixer.Sound('sounds/conectada_spanish_penelope.mp3').play()
                printer_connection_status = True
                break
    
    elif printer_connection_status:
        
        for port, desc, hwid in sorted(myports):
            
            device_id = "{}".format(hwid)
            my_ports_hwid.append(device_id[:len(printer_id)])
        
        if printer_id not in my_ports_hwid:
            
            label.configure(text = 'Impresora Desconectada.', font = (text_font, int(text_font_size//1.3)), bg = 'red', fg = 'yellow')
            mixer.Sound('sounds/desconectada_spanish_penelope.mp3').play()
            printer_connection_status = False
      
            if arduino_serial.isOpen():
                arduino_serial.close()
    
    frame.after(1000, check_printer_connection, frame, label)   # loop after propio de tkinter para no irrumpir el el loop principal
    
        
def print_braille(frame, input_text_box):       # Guarda las coordenadas de los puntos en un archivo csv para posteriormente ser enviados a arduino

    button_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    button_audio.play()
    
    #print(printer_connection_status, arduino_serial.isOpen())
    
    if printer_connection_status and arduino_serial.isOpen():

        text = ''
        text = input_text_box.get("1.0", tk.END)
        
        if (len(text) > 1):
            
            # borra lo que contenga el archivo csv (truncar, lo deja sin contenido)
            sysfile = open('config/sysfile.csv', 'w+')
            sysfile.close()
            
            temp1, temp2, printable_text = text_eval(text)            # se utiliza solo el texto que se retorna en la variable printable_text
            
            temp1 = None
            
            function = 'print'
            
            # limites horizontales y verticales de la hoja seleccionada en mm*10
            #horizontal_limit = PaperSheets.sheet_size[selected_sheet_size][0]*10 - (margin_h + dot_spacing_h)
            #vertical_limit = PaperSheets.sheet_size[selected_sheet_size][1]*10 - (margin_v + dot_spacing_v*2)
            
            # Cantidad de caracteres que caben horizontal y verticalmente en la hoja seleccionada
            #horizontal_characters = ((PaperSheets.sheet_size[selected_sheet_size][0]*10) - (margin_h*2)) // character_spacing_h
            horizontal_characters = 29
            vertical_characters = math.ceil(((PaperSheets.sheet_size[selected_sheet_size][1]*10) - (2*margin_v))/character_spacing_v)
            
            # numero total de paginas
            n_pages = math.ceil(len(printable_text) / vertical_characters)
            
            braille_board_dist = 1790   # distancia desde el primer punto hasta el ultimo de una fila
            
            #offset_h = round((1766 - 1740) / horizontal_characters)    # 1766 medida horizontal del  caracter 1 a 30 sobre el primer punto del mismo (Pizarra braille)
            offset_h = (1766 - 1740) / horizontal_characters
            #offset_h = 0
            # ancho original 1764
            # ancho de pizarra 
            
            for line in range(len(printable_text)):
                printable_text[line] = printable_text[line] [::-1]   # para revertir orden de las palabras por lineas
                
            #print(printable_text)
            
            # Iterador para concatenar cadenas para optimizacion de caminos
            iterator = False
            
            # array para guardar totalidad de coordenadas del texto ingresado
            total_coordinates = []
            
            # Contador de pagina
            page_cont = 1
            
            horizontal_shape = braille_board_dist
            vertical_shape = (vertical_characters * (2 * dot_spacing_v)) + ((vertical_characters - 1) * (character_spacing_v - (2 * dot_spacing_v)))
            
            #print(horizontal_shape, vertical_shape)
            
            for page in range(n_pages):
                
                total_coordinates.append(['newsheet'])  # agrega identificador de nueva hoja
                
                # Matriz base para imprimir en braille
                #print_sheet = np.zeros(((PaperSheets.sheet_size[selected_sheet_size][1]*10), (PaperSheets.sheet_size[selected_sheet_size][0]*10)), dtype = int)
                print_sheet = np.zeros((vertical_shape, horizontal_shape), dtype = int)
                
                character = ''
                
                sheet_coordinates = []   # array para guardar todas las coordenadas de puntos de una sola hoja
                array_top = []    # array para guardar coordenadas de la primera fila de puntos de un caracter en una hoja
                array_mid = []    # array para guardar coordenadas de la fila de puntos de la mitad de un caracter en una hoja
                array_bot = []    # array para guardar coordenadas de la ultima fila de puntos de un caracter en una hoja
                
                # auxiliares para guardar posiciones
                x = 0   
                y = 0
                
                for cont_char_text_v, i in enumerate(range(0, vertical_shape, character_spacing_v)):                # hasta el termino de este for, se crean los puntos braille
                    
                    if cont_char_text_v == len(printable_text): break # detiene el for principal cuando llega al final del texto
                    
                    for cont_char_text_h, j in enumerate(range(horizontal_shape, dot_spacing_h, -character_spacing_h)):
                        
                        if cont_char_text_h == len(printable_text[cont_char_text_v]):  # detiene for secundario cuando se acaban las palabras de una linea
                            break
                        
                        #print(cont_char_text_h, j, j - (cont_char_text_h * offset_h))
                        
                        character = printable_text[cont_char_text_v][(len(printable_text[cont_char_text_v]) - 1) - cont_char_text_h]
                        #print(character)
                        # solo se crea un punto si hay un '1' presente en el formato braille en el diccionario
                        
                        x, y = make_dot(print_sheet, i, j - (cont_char_text_h * offset_h), BrailleDictionary.b_characters[character][0], function)#backwards_b_characters[character][1], function)
                        
                        if x != -1 and y != -1:
                            array_top.append('X' + str(x/10) + 'Y' + str(y/10))
                            #print(x, ' ', y, '\n')
                            
                        x, y = make_dot(print_sheet, i, j - (dot_spacing_h + (cont_char_text_h * offset_h)), BrailleDictionary.b_characters[character][1], function)
                        
                        if x != -1 and y != -1:
                            array_top.append('X' + str(x/10) + 'Y' + str(y/10))
                            #print(x, ' ', y, '\n')
                        
                        x, y = make_dot(print_sheet, i + dot_spacing_v, j - (cont_char_text_h * offset_h), BrailleDictionary.b_characters[character][2], function)
                        
                        if x != -1 and y != -1:
                            array_mid.append('X' + str(x/10) + 'Y' + str(y/10))
                            #print(x, ' ', y, '\n')
                        
                        x, y = make_dot(print_sheet, i + dot_spacing_v, j - (dot_spacing_h + (cont_char_text_h * offset_h)), BrailleDictionary.b_characters[character][3], function)
                        
                        if x != -1 and y != -1:
                            array_mid.append('X' + str(x/10) + 'Y' + str(y/10))
                            #print(x, ' ', y, '\n')
                        
                        x, y = make_dot(print_sheet, i + dot_spacing_v*2, j - (cont_char_text_h * offset_h), BrailleDictionary.b_characters[character][4], function)
                        
                        if x != -1 and y != -1:
                            array_bot.append('X' + str(x/10) + 'Y' + str(y/10))
                            #print(x, ' ', y, '\n')
                        
                        x, y = make_dot(print_sheet, i + dot_spacing_v*2, j - (dot_spacing_h + (cont_char_text_h * offset_h)), BrailleDictionary.b_characters[character][5], function)
                        
                        if x != -1 and y != -1:
                            array_bot.append('X' + str(x/10) + 'Y' + str(y/10))
                            #print(x, ' ', y, '\n')
                            
                        x = 0
                        y = 0
                    
                    if cont_char_text_v == vertical_characters:     # detiene el for principal cuando la cantidad de lineas verticales igualan a la cantidad maxima de lineas verticales de la hoja
                        break
                    
                    if not iterator:
                        
                        a = list(reversed(array_top))
                        b = array_mid
                        c = list(reversed(array_bot))
                        
                        #a = array_top
                        #b = list(reversed(array_mid))
                        #c = array_bot
                        
                        #print(a, '\n\n', b, '\n\n', c, '\n')
                        
                        sheet_coordinates+= a + b + c
                        
                        sheet_coordinates.append('calibratex')
                        
                        #print(sheet_coordinates, '\n')
                        
                        array_top = []
                        array_mid = []
                        array_bot = []
                        
                        iterator = True
                        
                    elif iterator:
                        
                        a = array_top
                        b = list(reversed(array_mid))
                        c = array_bot
                        
                        #a = list(reversed(array_top))
                        #b = array_mid
                        #c = list(reversed(array_bot))
                        
                        #print(a, '\n\n', b, '\n\n', c, '\n')
                        
                        sheet_coordinates+= a + b + c
                        
                        sheet_coordinates.append('calibratex')
                        
                        #print(sheet_coordinates, '\n')
                        
                        array_top = []
                        array_mid = []
                        array_bot = []
                        
                        iterator = False
                        
                    #sheet_coordinates.append('calibratex')
                
                printable_text = printable_text[vertical_characters:]     # recorta el array de texto a la cantidad de linesas maximas verticales soportadas por la hoja
                
                total_coordinates.append(sheet_coordinates)
                
                page_cont+= 1
        
            total_coordinates.append(['endprint'])  # agrega identificador de termino de impresion
            
            with open('config/sysfile.csv','w+', newline='') as print_file:
                   wr = csv.writer(print_file, delimiter='\n')
                   wr.writerows(total_coordinates)
            
            total_coordinates = []
            sheet_coordinates = []
            array_top = []
            array_mid = []
            array_bot = []
            a = []
            b = []
            c = []
            #print('listo')
        
            text = ''
        
            AlertMessages(frame, '¿Desea IMPRIMIR el documento?', 'sounds/desea_imprimir_spanish_penelope.mp3')
            
    else:

        mixer.Sound('sounds/revise_conexion_spanish_penelope.mp3').play()
    
    
def redo_undo(input_text_box, action):    # funcion para rehacer o deshacer cambios de la caja de entrada de texto, y para el manejo de errores de las propias funciones

    button_audio = mixer.Sound('sounds/ventana_emergente_sfx.wav')
    button_audio.play()    

    if action == 'redo':
        try:
            input_text_box.edit_redo()
        except: pass
        
    elif action == 'undo':
        try:
            input_text_box.edit_undo()
        except: pass
    
    input_text_box.focus_force()
    
def button_iterator_check(input_text_box):
    
    global button_iterator
    
    if button_iterator:
        
        button_iterator = False
        
        input_text_box.focus_force()
        
    elif not button_iterator:
        
        button_iterator = True
    
class HighLightButtons(object):                    # Clase para cambiar fondo de los botones con el teclado, y seleccionar accion.
    
    def __init__(self, frame, button_list, button_list_str, input_text_box, text_font_size_input):      # recibe el frame donde se ubican los botones y una lista de los mismos, organizados por frame untilizado en la ventana principal
        
        self.frame = frame
        self.button_list = button_list
        self.button_list_str = button_list_str
        self.text_font_size_input = text_font_size_input
        self.posi = 0
        self.posj = 0
        self.action = None
        self.selected_button = button_list[self.posi][self.posj]
        self.selected_button.config(bg = highlight_color)
        self.selected_button.update()
        
        self.bindings(input_text_box)
        
    def bindings(self, input_text_box):    # para mapear los botones del teclado
        
        self.frame.bind('<Left>', lambda event: self.leftkey(input_text_box))
        self.frame.bind('<Right>', lambda event: self.rightkey(input_text_box))
        self.frame.bind('<Up>', lambda event: self.upkey(input_text_box))
        self.frame.bind('<Down>', lambda event: self.downkey(input_text_box))
        self.frame.bind('<Return>', lambda event: self.select_action(input_text_box))
     
    def leftkey(self, input_text_box):    # tecla izquierda presionada
    
        if button_iterator:    
    
            self.frame.focus_force()
         
            self.selected_button.config(bg = button_color)
            self.selected_button.update()
            
            if self.posj == 0:
                
                self.posj = len(self.button_list[self.posi])
                
            self.posj-= 1
            
            self.selected_button = self.button_list[self.posi][self.posj]
            self.selected_button.config(bg = highlight_color)
            
        elif not button_iterator:
            
            input_text_box.focus_force()
            return
        
    def rightkey(self, input_text_box): # tecla derecha presionada
    
        if button_iterator:
    
            self.frame.focus_force()
            
            self.selected_button.config(bg = button_color)
            self.selected_button.update()
            self.posj+= 1
            
            if self.posj == len(self.button_list[self.posi]):
                
                self.posj = 0
            
            self.selected_button = self.button_list[self.posi][self.posj]
            self.selected_button.config(bg = highlight_color)
            
        elif not button_iterator:
            
            input_text_box.focus_force()
            return
        
    def upkey(self, input_text_box):    # tecla arriba presionada
    
        if button_iterator:
    
            self.frame.focus_force()    
        
            self.posj = 0
            
            self.selected_button.config(bg = button_color)
            self.selected_button.update()
            
            if self.posi == 0:
                
                self.posi = len(self.button_list)
                
            self.posi-= 1
            
            self.selected_button = self.button_list[self.posi][self.posj]
            self.selected_button.config(bg = highlight_color)
            
        elif not button_iterator:
            
            input_text_box.focus_force()
            return
        
    def downkey(self, input_text_box):    # tecla abajo presionada
    
        if button_iterator:
        
            self.frame.focus_force()
            
            self.posj = 0
            
            self.selected_button.config(bg = button_color)
            self.selected_button.update()
            self.posi+= 1
            
            if self.posi == len(self.button_list):
                
                self.posi = 0
            
            self.selected_button = self.button_list[self.posi][self.posj]
            self.selected_button.config(bg = highlight_color)
            
        elif not button_iterator:
            
            input_text_box.focus_force()
            return
    
    def select_action(self, input_text_box):
        
        if button_iterator:
        
            self.frame.focus_force()
            
            if self.button_list_str[self.posi][self.posj] == 'Boton_vista_preliminar':
                
                preview(self.frame, input_text_box)
            
            elif self.button_list_str[self.posi][self.posj] == 'Boton_cancelar':
                
                cancel_print(self.frame)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_escuchar_texto':
                
                get_tts_text(self.frame, input_text_box)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_detener_lectura':
                
                stop_tts()
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_imprimir':
                
                print_braille(self.frame, input_text_box)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_pausar':
                
                pause_print(self.frame)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_salir':
                
                closeApp(self.frame, False)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_letter_max':
                
                input_text_size(True, self.text_font_size_input)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_letter_min':
                
                input_text_size(False, self.text_font_size_input)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_voz':
                
                speech_recognition(self.button_list[self.posi][self.posj], input_text_box)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_contraste':
                
                change_contrast(self.frame, input_text_box)
                
            elif self.button_list_str[self.posi][self.posj] == 'input_text_box':
                
                input_text_box.config(bg = button_color)
                
                input_text_box.focus_force()
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_agrandar':
                
                cambiar_tamano(self.frame, True, input_text_box)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_reducir':
                
                cambiar_tamano(self.frame, False, input_text_box)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_activate_audio':
                
                activate_audio()
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_deactivate_audio':
                
                deactivate_audio()
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_undo':
                
                redo_undo(input_text_box, 'undo')
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_redo':
                
                redo_undo(input_text_box, 'redo')
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_erase_text':
                
                erase_text(input_text_box)
                
            elif self.button_list_str[self.posi][self.posj] == 'Boton_ajustes':    
                
                Settings(self.frame)
    
        elif not button_iterator:
            
            input_text_box.focus_force()
        
####################################################################

def __main__():
    
    # Estructura de la ventana
    root = tk.Tk()
    
    root.title("Braille Printer")                               # Titulo de la ventana
    #root.maxsize(GetSystemMetrics(0),GetSystemMetrics(1))       # maxsize(Ancho,Alto) GetSystemMetrics para maxima resolucion de la pantalla
    root.config(bg= background_color, bd=15)                                        # borde exterior de 15 píxeles, color blanco
    root.iconphoto(False, tk.PhotoImage(file='icons/window_icon.png'))          # Icono de la ventana
    root.resizable(0,0)
    #geometry = '1425x907+50+50'       # Construye un string para establecer dimensiones y posicion de la ventana principal (root)  (cambiar para ajustar se tamano de monitor huesped)
    geometry = str(round(GetSystemMetrics(0) * 0.742)) + 'x' + str(round(GetSystemMetrics(1) * 0.8398)) + '+' + str(round(GetSystemMetrics(0) / 38.4)) + '+' + str(round(GetSystemMetrics(1) / 21.6))
    root.geometry(geometry)
    mixer.init()                               # Inicializa mixer
    
    global window_first_build
    
    if not window_first_build:       # Reproduce mensaje de binvenida solo al inicio
        mixer.Sound('sounds/bienvenido_spanish_penelope.mp3').play()
    
    #####################################################################################
    
    ############################################# INICIALIZAR IMAGENES ################################################
    
    ###################### Bar_1 ######################
    icon01 = resize_icon('icons/icon01.png', 1, 'icon')    # Reescalado de icono con factor de ajuste individual, segundo argumento ==1 (tamano normal), <1 agrandar icono, >1 reducir icono
    icon02 = resize_icon('icons/icon02.png', 1, 'icon')    
    icon03 = resize_icon('icons/icon03.png', 1, 'icon')   
    icon04 = resize_icon('icons/stop_tts.png', 1, 'icon')    
    icon05 = resize_icon('icons/icon04.png', 1, 'icon')   
    icon06 = resize_icon('icons/pausa.png', 1, 'icon')   
    icon07 = resize_icon('icons/icon06.png', 1, 'icon')   
    
    ###################### Bar_2 ######################
    icon08 = resize_icon('icons/letter_max.png', 2, 'icon')   
    icon09 = resize_icon('icons/letter.png', 2, 'icon')     
    icon10 = resize_icon('icons/letter_min.png', 2, 'icon')   
    icon11 = resize_icon('icons/microphone.png', 2, 'icon')     
    icon12 = resize_icon('icons/contraste.png', 2, 'icon')     
    
    ###################### Bar_3 ######################
    icon13 = resize_icon('icons/expand.png', 2, 'icon')      
    icon14 = resize_icon('icons/shrink.png', 2, 'icon')
    icon15 = resize_icon('icons/icon05_1.png', 2, 'icon')      
    icon16 = resize_icon('icons/icon05_2.png', 2, 'icon')
    icon17 = resize_icon('icons/settings.png', 2, 'icon')
    icon18 = resize_icon('icons/erase_text.png', 2, 'icon')
    icon19 = resize_icon('icons/redo.png', 2, 'icon')
    icon20 = resize_icon('icons/undo.png', 2, 'icon')
    
    ##########################################################################################
    
    # Configuracion de tamano para la fuente de texto del cuadro de texto
    
    text_font_size_input = Font(family="Verdana", size = scrolled_font_size)
    
    ############################################# FRAMES PARA BOTONES ################################################
  
    #########################################
    
    Bar_1 = tk.Frame(root, bg = background_color)       # Frame de botones superiores
    Bar_1.pack(side = 'top', fill = 'x', expand = False)
    
    Bar_2 = tk.Frame(root, bg = background_color)       # Frame de botones izquierda
    Bar_2.pack(side = 'left', expand = False, pady=button_separation_Y)
    
    Bar_3 = tk.Frame(root, bg = background_color)       # Frame para botones inferiores
    Bar_3.pack(side = 'bottom', fill = 'x', pady=button_separation_Y)
    
    Bar_4 = tk.Frame(root, bg = background_color)       # Frame para scrolledtext
    Bar_4.pack(side = 'left', expand = False, padx=int(button_separation_X/2), pady=button_separation_Y)

    
    ############################################# BOTONES ################################################

    ######## Bar_1 ######## 
    
    # Boton vista preliminar
    Boton_vista_preliminar = tk.Button(Bar_1, text= 'Vista preliminar', font =(text_font, text_font_size), compound = tk.BOTTOM, image= icon01, bg = button_color, fg = text_color, command=lambda:preview(root, input_text_box)) 
    CreateToolTip(Boton_vista_preliminar, "Boton para ver la vista preliminar de\nlas hojas a imprimir.<Control-F1>", "sounds/vista_preliminar_spanish_penelope.mp3")
    Boton_vista_preliminar.pack(side = "left", expand = False, pady=button_separation_Y)
    
    # Label de separacion
    label_b11 = tk.Label(Bar_1, text = ' ', width = int(tamano_icon//13), bg = background_color)
    label_b11.pack(side = "left", expand = True)
    
    # Boton cancelar impresion
    Boton_cancelar = tk.Button(Bar_1, text= "Cancelar", font =(text_font, text_font_size), compound = tk.BOTTOM, image= icon02, bg = button_color, fg = text_color, command=lambda:cancel_print(root))
    CreateToolTip(Boton_cancelar, "Al presionar este boton se cancela\nlo que se este imprimiendo\nen el momento.<Control-F2>", "sounds/cancelar_impresion_spanish_penelope.mp3")
    Boton_cancelar.pack(side = "left", expand = False, pady=button_separation_Y)
    
    # Label de separacion
    label_b11 = tk.Label(Bar_1, text = ' ', width = int(tamano_icon//13), bg = background_color)
    label_b11.pack(side = "left", expand = True)
    
    # Boton escuchar texto
    Boton_escuchar_texto = tk.Button(Bar_1, text= "Escuchar Texto", font =(text_font, text_font_size), compound = tk.BOTTOM, image= icon03, bg = button_color, fg = text_color, command=lambda:get_tts_text(root, input_text_box))   # (pyttsx3) tts_PYTTSX3(root, input_text_box)   #(gTTS) tts_gTTS(root, input_text_box)
    CreateToolTip(Boton_escuchar_texto, "Boton escuchar texto.<Control-F3>", "sounds/escuchar_texto_spanish_penelope.mp3")
    Boton_escuchar_texto.pack(side = "left", expand = False, pady=button_separation_Y)
    
    # Label de separacion
    label_b11 = tk.Label(Bar_1, text = ' ', width = int(tamano_icon//13), bg = background_color)
    label_b11.pack(side = "left", expand = True)
    
    # Boton detener lectura
    Boton_detener_lectura = tk.Button(Bar_1, text= "Detener lectura", font =(text_font, text_font_size), compound = tk.BOTTOM, image= icon04, bg = button_color, fg = text_color, command=lambda:stop_tts())
    CreateToolTip(Boton_detener_lectura, "Boton para detener lectura de texto\nseleccionado.<Control-F4>", "sounds/detener_tts_spanish_penelope.mp3")
    Boton_detener_lectura.pack(side = "left", expand = False, pady=button_separation_Y)
    
    # Label de separacion
    label_b11 = tk.Label(Bar_1, text = ' ', width = int(tamano_icon//13), bg = background_color)
    label_b11.pack(side = "left", expand = True)
    
    # Boton imprimir texto
    Boton_imprimir = tk.Button(Bar_1, text= "Imprimir", font =(text_font, text_font_size), compound = tk.BOTTOM, image= icon05, bg = button_color, fg = text_color, command=lambda:print_braille(root, input_text_box))
    CreateToolTip(Boton_imprimir, "Boton imprimir.<Control-p>", "sounds/imprimir_documento_spanish_penelope.mp3")
    Boton_imprimir.pack(side = "left", expand = False, pady=button_separation_Y)
    
    # Label de separacion
    label_b11 = tk.Label(Bar_1, text = ' ', width = int(tamano_icon//13), bg = background_color)
    label_b11.pack(side = "left", expand = True)
    
    # Boton pausar
    Boton_pausar = tk.Button(Bar_1, text= "Pausar", font =(text_font, text_font_size), compound = tk.BOTTOM, image= icon06, bg = button_color, fg = text_color, command=lambda:pause_print(root))
    CreateToolTip(Boton_pausar, "Pausar impresión.<Control-F5>", "sounds/pausar_impresion_spanish_penelope.mp3")
    Boton_pausar.pack(side = "left", expand = False, pady=button_separation_Y)
    
    # Label de separacion
    label_b11 = tk.Label(Bar_1, text = ' ', width = int(tamano_icon//13), bg = background_color)
    label_b11.pack(side = "left", expand = True)
    
    # Boton Salir
    Boton_salir = tk.Button(Bar_1, text= "Salir", font =(text_font, text_font_size), compound = tk.BOTTOM, image= icon07, bg = button_color, fg = text_color, command=lambda:closeApp(root, False))
    CreateToolTip(Boton_salir, "Cerrar la aplicación.<Escape>", "sounds/cerrar_aplicacion_spanish_penelope.mp3")
    Boton_salir.pack(side = "left", expand = False, pady=button_separation_Y)
    
    ######## Bar_2 ########
    
    # Boton para aumentar tamaño de texto de entrada
    Boton_letter_max = tk.Button(Bar_2, image= icon08, bg = button_color, fg = text_color, command=lambda:input_text_size(True, text_font_size_input))
    CreateToolTip(Boton_letter_max, "Aumentar tamaño de\ntexto de entrada.<F1>", "sounds/aumentar_texto_spanish_penelope.mp3")
    Boton_letter_max.pack(side = "top", pady = button_separation_Y)
    
    # Label con imagen representando una letra 'A'
    label_A = tk.Label(Bar_2, text = 'A', image = icon09, bg = button_color)
    label_A.pack(side = 'top')
    
    # Boton para disminuir tamño de texto de entrada
    Boton_letter_min = tk.Button(Bar_2, image= icon10, bg = button_color, fg = text_color, command=lambda:input_text_size(False, text_font_size_input))
    CreateToolTip(Boton_letter_min, "Reducir tamaño de\ntexto de entrada.<F2>", "sounds/reducir_texto_spanish_penelope.mp3")
    Boton_letter_min.pack(side = "top", pady = button_separation_Y)
    
    # Label separacion 
    label_separacion_b2 = tk.Label(Bar_2, text = ' ', bg = background_color, height = button_separation_Y)
    label_separacion_b2.pack(side = "top")
    
    # Boton de reconocimiento de voz
    Boton_voz = tk.Button(Bar_2, image= icon11, bg = button_color, fg = text_color, command=lambda:speech_recognition(Boton_voz, input_text_box))   # speech_recognition(input_text_box)
    CreateToolTip(Boton_voz, "Activar reconocimiento\nde voz.<Control-s>", "sounds/voz_spanish_penelope.mp3")
    Boton_voz.pack(side = "top")
    
    # Label separacion 
    label_separacion_b3 = tk.Label(Bar_2, text = ' ', bg = background_color, height = button_separation_Y)
    label_separacion_b3.pack(side = "top")
    
    # Boton para aumentar contraste
    Boton_contraste = tk.Button(Bar_2, image = icon12, bg = button_color, fg = text_color, command=lambda:change_contrast(root, input_text_box))
    CreateToolTip(Boton_contraste, "Cambiar contraste\nde la interfaz.<F3>", "sounds/contraste_spanish_penelope.mp3")
    Boton_contraste.pack(side = "bottom", pady = button_separation_Y)
    
    ######## Bar_4 ######## ENTRADA DE TEXTO ########
    
    # Caja de entrada de texto
    input_text_box = scrolledtext.ScrolledText(Bar_4, wrap="word", height = round(tamano_icon/3), width = round(tamano_icon/0.8), font = text_font_size_input, bg = button_color, fg = text_color, bd=5, undo = True)   #height = round(root.winfo_height())
    input_text_box.focus_set()
    input_text_box.pack(side = "left", expand = False)

    ######## Bar_3 ########
    
    # Boton para agrandar elementos de la aplicación
    Boton_agrandar = tk.Button(Bar_3, image= icon13, bg = button_color, fg = text_color, command=lambda:cambiar_tamano(root, True, input_text_box))
    CreateToolTip(Boton_agrandar, "Boton para agrandar elementos\nde la aplicación.<F4>", "sounds/agrandar_app_spanish_penelope.mp3")
    Boton_agrandar.pack(side = "left")
    
    # Boton para reducir elementos de la aplicación
    Boton_reducir = tk.Button(Bar_3, image= icon14, bg = button_color, fg = text_color, command=lambda:cambiar_tamano(root, False, input_text_box))
    CreateToolTip(Boton_reducir, "Boton para reducir elementos\nde la aplicación.<F5>", "sounds/reducir_app_spanish_penelope.mp3")
    Boton_reducir.pack(side = "left", padx = button_separation_X)
    
    # Boton para habilitar audio
    Boton_activate_audio = tk.Button(Bar_3, image = icon16, bg = button_color, fg = text_color, command=lambda:activate_audio())
    CreateToolTip(Boton_activate_audio, "Boton para habilitar sonido\ndescriptivo de los botones.<F6>", "sounds/habilitar_audio_spanish_penelope.mp3")
    Boton_activate_audio.pack(side = "left")
    
    # Boton para deshabilitar audio
    Boton_deactivate_audio = tk.Button(Bar_3, image = icon15, bg = button_color, fg = text_color, command=lambda:deactivate_audio())
    CreateToolTip(Boton_deactivate_audio, "Boton para deshabilitar sonido\ndescriptivo de los botones.<F7>", "sounds/deshabilitar_audio_spanish_penelope.mp3")
    Boton_deactivate_audio.pack(side = "left", padx = button_separation_X)
    
    # label para mostrar el estado de la conexion de la impresora
    connection_label = tk.Label(Bar_3, text = 'Impresora Desconectada.', font = (text_font, int(text_font_size//1.3)), bg = 'red', fg = 'yellow')
    CreateToolTip(connection_label, "Muestra si la impresora esta\nconectada o desconectada.", "sounds/estado_conexion_spanish_penelope.mp3")
    connection_label.pack(side = "left")
    
    # Label de separacion
    label_separacion02 = tk.Label(Bar_3, text = ' ', width = int(tamano_icon//3.4), bg = background_color)
    label_separacion02.pack(side = "left", expand = True)
    
    # boton para deshacer cambios en la caja de entrada de texto
    Boton_undo = tk.Button(Bar_3, image= icon20, bg = button_color, fg = text_color, command=lambda:redo_undo(input_text_box, 'undo'))
    CreateToolTip(Boton_undo, "Boton deshacer cambios del\ntexto ingresado.<F8>", "sounds/deshacer_spanish_penelope.mp3")
    Boton_undo.pack(side = "left", expand = False)
    
    # boton para rehacer cambios en la caja de entrada de texto
    Boton_redo = tk.Button(Bar_3, image= icon19, bg = button_color, fg = text_color, command=lambda:redo_undo(input_text_box, 'redo'))
    CreateToolTip(Boton_redo, "Boton rehacer cambios del\ntexto ingresado.<F9>", "sounds/rehacer_spanish_penelope.mp3")
    Boton_redo.pack(side = "left", expand = False, padx = button_separation_X)
    
    # Label de separacion
    label_separacion02 = tk.Label(Bar_3, text = ' ', width = int(tamano_icon//3.4), bg = background_color)
    label_separacion02.pack(side = "left", expand = True)
    
    # Boton para borrar todo el texto de entrada
    Boton_erase_text = tk.Button(Bar_3, image= icon18, bg = button_color, fg = text_color, command=lambda:erase_text(input_text_box))
    CreateToolTip(Boton_erase_text, "Boton para borrar todo\nel texto ingresado.<Control-e>", "sounds/borrar_texto_spanish_penelope.mp3")
    Boton_erase_text.pack(side = "left", expand = False, padx = button_separation_X)
    
    # Boton para abrir ventana de seleccionar tamano de hoja
    Boton_ajustes = tk.Button(Bar_3, image= icon17, bg = button_color, fg = text_color, command=lambda:Settings(root))
    CreateToolTip(Boton_ajustes, "Boton para seleccionar tamaño\nde hoja para impresión.<F10>", "sounds/seleccionar_tamano_hoja_spanish_penelope.mp3")
    Boton_ajustes.pack(side = "left", expand = False)

    ########################## Listas ##########################
    
    button_list = [[Boton_vista_preliminar, Boton_cancelar, Boton_escuchar_texto, Boton_detener_lectura, Boton_imprimir, Boton_pausar, Boton_salir],
                   [Boton_letter_max, input_text_box], 
                   [Boton_letter_min, input_text_box],
                   [Boton_voz, input_text_box],
                   [Boton_contraste, input_text_box], 
                   [Boton_agrandar, Boton_reducir, Boton_activate_audio, Boton_deactivate_audio, Boton_undo, Boton_redo, Boton_erase_text, Boton_ajustes]]
    
    button_list_str = [['Boton_vista_preliminar', 'Boton_cancelar', 'Boton_escuchar_texto', 'Boton_detener_lectura', 'Boton_imprimir', 'Boton_pausar', 'Boton_salir'],
                       ['Boton_letter_max', 'input_text_box'], 
                       ['Boton_letter_min', 'input_text_box'],
                       ['Boton_voz', 'input_text_box'],
                       ['Boton_contraste', 'input_text_box'], 
                       ['Boton_agrandar', 'Boton_reducir', 'Boton_activate_audio', 'Boton_deactivate_audio', 'Boton_undo', 'Boton_redo', 'Boton_erase_text', 'Boton_ajustes']]
    
    HighLightButtons(root, button_list, button_list_str, input_text_box, text_font_size_input)
    
    ########################## Binds para botones ################################
    
    ############# para funciones principales (7 superiores) ######################
    root.bind('<Control-F1>', lambda event: preview(root, input_text_box))
    root.bind('<Control-F2>', lambda event: cancel_print(root))
    root.bind('<Control-F3>', lambda event: get_tts_text(root, input_text_box))
    root.bind('<Control-F4>', lambda event: stop_tts())
    root.bind('<Control-p>', lambda event: print_braille(root, input_text_box))
    root.bind('<Control-F5>', lambda event: pause_print(root))
    root.bind('<Escape>', lambda event: closeApp(root, False))
    
    ############# para funciones secundarias (12) ######################
    root.bind('<F1>', lambda event: input_text_size(True, text_font_size_input))
    root.bind('<F2>', lambda event: input_text_size(False, text_font_size_input))
    root.bind('<Control-s>', lambda event: speech_recognition(Boton_voz, input_text_box))
    root.bind('<F3>', lambda event: change_contrast(root, input_text_box))
    root.bind('<F4>', lambda event: cambiar_tamano(root, True, input_text_box))
    root.bind('<F5>', lambda event: cambiar_tamano(root, False, input_text_box))
    root.bind('<F6>', lambda event: activate_audio())
    root.bind('<F7>', lambda event: deactivate_audio())
    root.bind('<F8>', lambda event: redo_undo(input_text_box, 'undo'))
    root.bind('<F9>', lambda event: redo_undo(input_text_box, 'redo'))
    root.bind('<Control-e>', lambda event: erase_text(input_text_box))
    root.bind('<F10>', lambda event: Settings(root))
    root.bind('<Control-x>', lambda event: button_iterator_check(input_text_box))
    # Loop para ejecutar funcion check_printer_connection en 'paralelo' a el mainloop principal,
    # se ejecuta despues de 3 segundos de iniciada la aplicacion.
    root.after(3000, check_printer_connection, root, connection_label)

    ######## CONFIGURACIÓN FNAL DE LA VENTANA PRINCIPAL ########
    
    window_first_build = True
    root.update()       # Acualiza la ventana root, permitiendo obtener los valores de las dimensiones de la ventana creada de acuerdo a los elementos que contiene
    Bar_1.update()
    Bar_2.update()
    Bar_3.update()
    Bar_4.update()
    
    #input_text_box.config(font=(text_font, text_font_size_input))
    root.focus_force()
    input_text_box.focus_force()
    #geometry = str(root.winfo_width()) + 'x' + str(root.winfo_height()) + '+' + pos_ini + '+' + pos_ini       # Construye un string para establecer dimensiones y posicion de la ventana principal (root)
    #print(geometry)
    #geometry = '+' + pos_ini + '+' + pos_ini
    #root.geometry(geometry)   # Establece tamaño del frame root de acuerdo al tamaño de los iconos al momento de inciar el programa en el formato especificado en geometry (Ancho,Alto, posicion inicial X (Horizontal) en el monitor, posicion inicial Y (Vertical) en el monitor )
    root.protocol("WM_DELETE_WINDOW", False)  
    root.mainloop()           # Mainloop para root
    
############################################################################################################
############################################################################################################

if __name__ == '__main__':
    
    # comprobacion de directorios
    directory_check()
    
    ################### ARDUINO ####################

    arduino_serial = None         # para asignar el puerto serial cuando es abierto

    connection_baud = 9600        # bits por segundo (No modificar)
    
    with open('config/printerid.txt') as f:    #para leer id del dispositivo
        sys_config = f.readlines()
    
    printer_id = sys_config[0].strip()   # id del dispositivo, variable segun el mismo, asi que si se utiliza otro hardware, este id debe cambiarse
    
    #printer_id = 'USB VID:PID=1A86:7523'   # id del dispositivo, variable segun el mismo, asi que si se utiliza otro hardware, este id debe cambiarse
    
    printer_connection_status = False     # variable para almacenar estado de la impresora
    
    sending_information = False        # variable para indicar si se esta enviando informacion a arduino
    
    callback = None
    
    pause_signal = False
    
    cancel_signal = False
    
    pause_row = 0
    #################################################
    
    #configuracion necesaria de pyplot para ver las imagenes en escala de grises
    plt.rcParams['image.cmap'] = 'gray'
                      
    # Ruta de archivos de audio temporales
    
    audio_temp = "temp/audio/tts_temp_audio.wav"   # Ruta default para archivo temporal de audio para tts
    
    # Variable para tamano de los iconos
    
    tamano_icon = round(GetSystemMetrics(1)/10.8)  # GetSystemMetrics(1) ===> resolucion vertical de monitor huesped ||| 13,5  ====> Factor para establecer tamaño de ventana
  
    # Separacion de los botones con iconos respecto al temaño de los mismos en el eje X
    
    button_separation_X = int(tamano_icon/4)
    
    # Separacion de los botones con iconos respecto al temaño de los mismos en el eje Y
    
    button_separation_Y = int(tamano_icon/16)
    
    ############################# COLORES  Y FUENTE ############################# 
    
    # Fuente del texto
    
    text_font = 'Verdana'
    
    # Color fondo de ventana
    
    background_color = 'gray60'
    
    # Color de los botones
    
    button_color = 'gray90'
    
    # Color del texto
    
    text_color = 'black'
    
    ################################################################### 
    
    # Configuracion de tamano para la fuente de texto de los iconos de acuerdo al tamano de los mismos
    
    text_font_size = int(tamano_icon/6)
    
    # Posicion inicial de la primera ventana en la pantalla al ejecutarse el programa (en pixeles)
    
    pos_ini = '50'
    
    # Separacion para los iconos dependiendo del tamano de los mismos
    
    icon_separation = int(tamano_icon/6)   
    
    # Variable para tamaño de hoja seleccionada
    
    selected_sheet_size = 'Carta'                      # Tamano por defecto = Carta  /// Disponibles: Carta, Oficio, A4
    
    # Variable auxiliar para selccion de hoja
    
    last_sheet_selected = 'Carta'
    
    # Variable para estado de contraste
    
    contrast_state = False               
    
    # Variable para estado de audio
    
    audio_state = False
    
    ############### Configuracion de medidas fisicas formato braille ###################### (Medidas en mm*10)
    
    # Separacion entre puntos de un caracter horizontal
    
    dot_spacing_h = 24                # (a)  
    
    # separacion entre caracteres horizontal
    
    character_spacing_h = 60        # (c)
    
    # Separacion entre puntos de un caracter vertical
    
    dot_spacing_v = 24                  # (b)     
    
    # separacion entre caracteres vertical
    
    character_spacing_v = 100         # (d)
    
    # Profundidad del punto
    
    dot_depth = 2
    
    # Radio de puntos
    
    radius = 12 // 2
    
    # Margenes de hoja
    
    margin_h = (((PaperSheets.sheet_size[selected_sheet_size][0]*10) - ((dot_spacing_h * 30) + 29 * (character_spacing_h - 24))) - 2) // 2
    #print(margin_h)
    margin_v = 60
    
    # Fuente para letras en imagen
    
    font_size = 21
    
    top_font = ImageFont.truetype('fonts/Cabin-VariableFont_wdth,wght.ttf', font_size)
    
    ###################################################################
    
    # Configuracion pyttsx3
    
    # Variable para establecer velocidad de TTS pyttsx3
    
    pyttsx3_rate = 130                # < 125, mas lento ::: > 125, mas rapido.
    
    driver_name = 'sapi5'
    
    tts_type = sys_config[1]
    
    # Configuracion gTTS
    
    # Idioma para tts (espanol-americano)
    
    tts_lang = 'es-us'    #'en'
    
    ###################################################################
    
    # Contador para reproducir audio de bienvenida solo una vez
    
    window_first_build = False
    
    # tamano de fuente para texto de entrada
    
    scrolled_font_size = 15
    
    ###################################################################
    
    # Ruta para guardar imagenes
    
    save_route = 'Saved Images/'
    
    ###############################################################
    
    # para tiempos, solo botencion de datos
    start_time = 0
    #start_time = time.process_time()
    end_time = 0
    #end_time = time.process_time()
    #print('Inicio: ' + str(start_time) + ' s\nTermino: ' + str(end_time) + ' s\nDuracion: ' + str(end_time - start_time) + ' s')
    
    ########################### icnicializar pytts3 ##################################
    
    pyttsx3engine = pyttsx3.init(driverName=driver_name) # Crea objeto pyttsx3
    pyttsx3engine.setProperty('rate', pyttsx3_rate)  # Establece velocidad de reproduccion
    #pyttsx3engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0')  # Configura idioma de tts.
    
    ############################################################################################
    
    ######## Configuracion para reconicimiento de voz ################
    
    # variable para saber si se esta usando el microfono
    recording = False
    
    # variable para asignar funcion de escuchar en el fondo
    stop_listening = None
    
    r = sr.Recognizer()
    ###########################################################################
    
    button_iterator = False
    
    highlight_color = 'cyan'
    
    sys_config = None
    
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 0 )
    
    __main__()