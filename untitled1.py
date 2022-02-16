# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 15:08:07 2022

@author: Sebafu
"""

import os
import datetime
import csv

def RUN():
    
    global IS_DOWN

    with open('Data/downtime_data.csv', mode='w') as speedcsv:
        csv_writer = csv.DictWriter(speedcsv, fieldnames=['Down Time', 'Up Time', 'Duration'])
        csv_writer.writeheader()
    
        while True:
            
            down_datetime = 0
            up_datetime = 0
            down_duration = 0
        
            response = os.system("ping -n 1 " + hostname)
            
            if response == 1:
                
                IS_DOWN = True
                
                _down = datetime.datetime.now()
                
                down_datetime = _down.strftime("%d-%m-%Y %H:%M:%S")
                
            elif response == 0 and IS_DOWN:
                
                _up = datetime.datetime.now()
                
                up_datetime = _up.strftime("%d-%m-%Y %H:%M:%S")
                
                down_duration = _up - _down
                
                #down_duration.strftime("%d-%m-%Y %H:%M:%S")
                
                csv_writer.writerow({
                    'Down Time': down_datetime,
                    'Up Time': up_datetime,
                    "Duration": down_duration
                })
                
                IS_DOWN = False
            
            print(str(down_datetime) + ' ' + str(up_datetime) + ' ' + str(down_duration))
    
if __name__ == '__main__':
    
    IS_DOWN = False
    
    hostname = "google.com"
    
    RUN()