import os
import sys
import time


try:
    machine = os.uname().machine
except Exception:
    machine = os.name

IS_PC = machine.startswith('x86_64') or machine.startswith('nt')
IS_RPi = machine.startswith('armv')
IS_ESP8266 = machine.startswith('ESP8266')
IS_ESP32 = machine.startswith('ESP32')
IS_TTGO_LORA_OLED = None
IS_MICROPYTHON = (sys.implementation.name == 'micropython')



def mac2eui(mac):
    mac = mac[0:6] + 'fffe' + mac[6:]
    return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:]



if IS_MICROPYTHON and (IS_ESP32 or IS_ESP8266):

    # Node Name
    import machine
    import ubinascii


    uuid = ubinascii.hexlify(machine.unique_id()).decode()

    if IS_ESP8266:
        NODE_NAME = 'ESP8266_'
    if IS_ESP32:
        NODE_NAME = 'ESP32_'
        import esp

    NODE_EUI = mac2eui(uuid)
    NODE_NAME = NODE_NAME + uuid

    # millisecond
    millisecond = time.ticks_ms

    # Controller
    SOFT_SPI = None
    IS_TTGO_LORA_OLED = (esp.flash_size() > 5000000)

    if IS_TTGO_LORA_OLED:
        SOFT_SPI = True
        from controller_esp_ttgo_lora_oled import Controller
    else:
        from controller_esp import Controller

if IS_RPi:

    # Node Name
    import socket


    NODE_NAME = 'RPi_' + socket.gethostname()

    # millisecond
    millisecond = lambda: time.time() * 1000

    # Controller
    from controller_rpi import Controller

if IS_PC:

    # Node Name
    import socket


    NODE_NAME = 'PC_' + socket.gethostname()

    # millisecond
    millisecond = lambda: time.time() * 1000

    # Controller
    # from controller_pc import Controller
