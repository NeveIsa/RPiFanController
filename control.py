import sys
import os
import platform
import subprocess
import re


if 'ARCH' in platform.uname().release:
    __read_temp = lambda : subprocess.check_output("/opt/vc/bin/vcgencmd measure_temp", shell=True).strip().decode()

def sense_temp():
    temp = __read_temp()
    val = re.findall('\d+\.?\d+?',temp)[0]
    val = (val)
    return val


def get_wifi():
    ssid = subprocess.check_output('iwgetid -r', shell=True).decode().strip()
    passwd = subprocess.check_output(f'cat /etc/NetworkManager/system-connections/{ssid}.nmconnection', shell=True).decode().strip()
    passwd = re.findall("psk=.+",passwd)[0]    
    return ssid,passwd

if __name__ == "__main__":
     temp = sense_temp()
     ssid,passwd=get_wifi()

     
     
     
