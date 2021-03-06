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
        print(f'fan level: {volts}/4096')
        DAC.set_voltage(volts)
        __last_volts = volts


if __name__ == "__main__":

    
    DAC = MCP4725(address=0x61, busnum=1)

    temp = sense_temp()
    print(f'temp: {temp}')

    if len(sys.argv) < 2:
        print(f'USAGE:\n\t{sys.argv[0]} fanspeed_out_of_100')
        sys.exit()
        
    speed = int(sys.argv[1])

    fan_speed(speed)
    
    

    exit()
     
     
     
