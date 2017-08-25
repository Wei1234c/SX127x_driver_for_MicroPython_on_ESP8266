import sys
import os 
import time


IS_MICROPYTHON = (sys.implementation.name == 'micropython')
IS_PC = False
IS_ESP32 = (os.uname().sysname == 'esp32')
IS_ESP8266 = (os.uname().sysname == 'esp8266')
IS_RPi = not (IS_MICROPYTHON or IS_PC)


if IS_MICROPYTHON:
        
    # Node Name
    from machine import unique_id
    import ubinascii
    unique_id = ubinascii.hexlify(unique_id()).decode()  
        
    if IS_ESP8266:
        NODE_NAME = 'ESP8266_'
    if IS_ESP32:
        NODE_NAME = 'ESP32_'
        
    NODE_NAME = NODE_NAME + unique_id    
    
    # millisecond
    millisecond = time.ticks_ms
    # microsecond = time.ticks_us

    
    # Controller
    from controller_esp import Controller
    
    
        
if IS_RPi:
    
    # Node Name
    import socket
    NODE_NAME = 'RPi_' + socket.gethostname()
    
    # millisecond
    millisecond = lambda : time.time() * 1000
    
    # Controller
    from controller_rpi import Controller
    
    
    
if IS_PC:
    
    # Node Name
    import socket
    NODE_NAME = 'PC_' + socket.gethostname()
    
    # millisecond
    millisecond = lambda : time.time() * 1000
    
    # Controller
    from controller_pc import Controller  