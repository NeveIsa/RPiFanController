#!/usr/bin/env python

import sys
import os
import platform
import subprocess
import re
import time
from Adafruit_MCP4725 import MCP4725
import sys
from functools import partial


if 'ARCH' in platform.uname().release:
    __read_temp = lambda : subprocess.check_output("/opt/vc/bin/vcgencmd measure_temp", shell=True).strip().decode()

def sense_temp():
    temp = __read_temp()
    val = re.findall('\d+\.?\d+?',temp)[0]
    val = float(val)
    return val


def get_wifi():
    ssid = subprocess.check_output('iwgetid -r', shell=True).decode().strip()
    passwd = subprocess.check_output(f'cat /etc/NetworkManager/system-connections/{ssid}.nmconnection', shell=True).decode().strip()
    passwd = re.findall("psk=.+",passwd)[0]    
    return ssid,passwd


__last_volts=-1
def fan_speed(val):
    global __last_volts
    
    BASE_SPEED = 700
    SPEED_RANGE = 200
    
    #check if val in 0 to 100
    if val<0: val=0
    if val>100: val=100
    
    volts = BASE_SPEED + int(SPEED_RANGE * val/100)

    # stop if val==0
    if val==0: volts=0

    if __last_volts!=volts:
        DAC.set_voltage(volts)
        __last_volts = volts

__speed = 0
def simple_fan_control(current_temp,temp_setpoint=40):
    global __speed
    diff = current_temp - temp_setpoint

    if diff > 0:
        # speed inc. 10 per degree celsius
        __speed = diff*10 

    # if temp drops below setpoint by 6 degrees
    elif diff < -6:
        __speed = 0
    else:
        __speed -= 5
        if __speed <= 0: __speed+=5
        
    fan_speed(__speed)

    return __speed
        

if __name__ == "__main__":

    #ssid,passwd=get_wifi()
    #print(f'Connected @ {ssid}')

    # get setpoint
    TEMP_SETPOINT = 40
    if len(sys.argv)>1:
        TEMP_SETPOINT = int(sys.argv[1])
    controller = partial(simple_fan_control, temp_setpoint=TEMP_SETPOINT)    

    DAC = MCP4725(address=0x61, busnum=1)
    
    while True:
        try:
            temp = sense_temp()
            speed = controller(temp)            
            print(f'temp->{temp}\tspeed->{speed}')
            time.sleep(1)
        except Exception as e:
            print('Exception ->', e)
            raise

     
     
     
