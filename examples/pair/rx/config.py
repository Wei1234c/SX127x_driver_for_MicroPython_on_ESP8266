import sys
import os


IS_MICROPYTHON = (sys.implementation.name == 'micropython')
IS_PC = False
IS_ESP32 = (os.uname().sysname == 'esp32')
IS_ESP8266 = (os.uname().sysname == 'esp8266')
IS_RPi = not (IS_MICROPYTHON or IS_PC)


if IS_MICROPYTHON:    
    import machine
    import ubinascii
    unique_id = ubinascii.hexlify(machine.unique_id()).decode() 
    WORKER_NAME = 'NodeMCU_' + unique_id     
    
    if IS_ESP8266:        
        import hardware_esp8266 as hardware
    if IS_ESP32:
        pass        

if IS_RPi:
    WORKER_NAME = 'RPi_366'
    
if IS_PC:
    WORKER_NAME = 'PC_366'    