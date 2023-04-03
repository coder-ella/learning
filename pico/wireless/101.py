import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

ssid = 'xxxxx'
password = 'xxxxxx'

print(f"STAT_IDLE: {network.STAT_IDLE}")
print(f"STAT_CONNECTING: {network.STAT_CONNECTING}")
print(f"STAT_WRONG_PASSWORD: {network.STAT_WRONG_PASSWORD}")
print(f"STAT_NO_AP_FOUND: {network.STAT_NO_AP_FOUND}")
print(f"STAT_CONNECT_FAIL: {network.STAT_CONNECT_FAIL}")
print(f"STAT_GOT_IP: {network.STAT_GOT_IP}")
'''
STAT_IDLE: 0
STAT_CONNECTING: 1
STAT_WRONG_PASSWORD: -3
STAT_NO_AP_FOUND: -2
STAT_CONNECT_FAIL: -1
STAT_GOT_IP: 3
'''
#errors:
#https://github.com/georgerobotics/cyw43-driver/blob/9bfca61173a94432839cd39210f1d1afdf602c42/src/cyw43.h#L80
#https://github.com/glenn20/micropython-espnow-utils
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    max_tries = 20
    try_count = 0
    while wlan.isconnected() == False\
          and try_count < max_tries\
          and wlan.status() > 0:
        try_count = try_count + 1
        print(f'{try_count}: Waiting for connection... {wlan.status()}')
        sleep(1)
        
    print(f'wlan.isconnected():{wlan.isconnected()} wlan.status(): {wlan.status()}')
    print(wlan.ifconfig())

try:
    connect()
except KeyboardInterrupt:
    machine.reset()
    

