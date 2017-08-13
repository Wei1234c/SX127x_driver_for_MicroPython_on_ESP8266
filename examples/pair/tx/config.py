import sys
import os 


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
        import hardware_esp8266 as hardware
        WORKER_NAME = 'ESP8266_'
    if IS_ESP32:
        import hardware_esp32 as hardware
        WORKER_NAME = 'ESP32_'
        
    WORKER_NAME = WORKER_NAME + unique_id
    
    
    # Controller
    from controller_esp import Controller
    
    
        
if IS_RPi:
    WORKER_NAME = 'RPi_366'
    
    
    
if IS_PC:
    WORKER_NAME = 'PC_366'    