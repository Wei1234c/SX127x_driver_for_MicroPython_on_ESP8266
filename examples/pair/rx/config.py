import sys
import os 


IS_MICROPYTHON = (sys.implementation.name == 'micropython')
IS_PC = False
IS_ESP32 = (os.uname().sysname == 'esp32')
IS_ESP8266 = (os.uname().sysname == 'esp8266')
IS_RPi = not (IS_MICROPYTHON or IS_PC)


if IS_MICROPYTHON:
    from machine import Pin, SPI, unique_id
    import ubinascii
    unique_id = ubinascii.hexlify(unique_id()).decode() 
    WORKER_NAME = 'NodeMCU_' + unique_id
    
    LORA_RESET_PIN = 4    
    LORA_SS_PIN = 15
    LORA_SCK_PIN = 14
    LORA_MOSI_PIN = 13
    LORA_MISO_PIN = 12
    LORA_IRQ_PIN = 5    
        
    if IS_ESP8266:        
        import hardware_esp8266 as hardware
        spi = SPI(1, baudrate = 10000000, polarity = 0, phase = 0)
        spi.init()
        
    if IS_ESP32:
        import hardware_esp32 as hardware
        spi = SPI(1, baudrate = 10000000, polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
                  sck = Pin(LORA_SCK_PIN, Pin.OUT), 
                  mosi = Pin(LORA_MOSI_PIN, Pin.OUT), 
                  miso = Pin(LORA_MISO_PIN, Pin.IN))
        spi.init()
        
        
if IS_RPi:
    WORKER_NAME = 'RPi_366'
    
    
if IS_PC:
    WORKER_NAME = 'PC_366'    