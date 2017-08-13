import sys
import os 


IS_MICROPYTHON = (sys.implementation.name == 'micropython')
IS_PC = False
IS_ESP32 = (os.uname().sysname == 'esp32')
IS_ESP8266 = (os.uname().sysname == 'esp8266')
IS_RPi = not (IS_MICROPYTHON or IS_PC)


if IS_MICROPYTHON:
    from machine import Pin, SPI, unique_id, reset
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
        
    if IS_ESP32:
        import hardware_esp32 as hardware
        try:
            spi = SPI(1, baudrate = 10000000, polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
                      sck = Pin(LORA_SCK_PIN, Pin.OUT), 
                      mosi = Pin(LORA_MOSI_PIN, Pin.OUT), 
                      miso = Pin(LORA_MISO_PIN, Pin.IN)) 
        except Exception as e:
            print(e)
            reset()  # SPI is already in use, need to reset.
                  
    class mock:
        pass
        
    def prepare_pin(pin_id, in_out = Pin.OUT):
        pin = Pin(pin_id, in_out)
        new_pin = mock()
        new_pin.value = pin.value
        
        if in_out == Pin.OUT:
            new_pin.low = lambda : pin.value(0)
            new_pin.high = lambda : pin.value(1)        
        else:
            new_pin.irq = pin.irq
            
        return new_pin
    
    def prepare_irq_pin(pin_id): 
        pin = prepare_pin(pin_id, Pin.IN) 
        pin.set_handler_for_irq_on_rising_edge = lambda handler: pin.irq(handler = handler, trigger = Pin.IRQ_RISING)
        pin.detach_irq = lambda : pin.irq(handler = None, trigger = 0)
        return pin

    def prepare_spi(spi):       
        ss = prepare_pin(LORA_SS_PIN)
        ss.high()
        spi.init()               
        new_spi = mock()  
    
        def transfer(address, value = 0x00):        
            response = bytearray(1)

            ss.low()
             
            spi.write(bytes([address]))
            spi.write_readinto(bytes([value]), response)

            ss.high()

            return response
            
        new_spi.transfer = transfer
        
        return new_spi
        
        
    # reset pin
    reset_pin = prepare_pin(LORA_RESET_PIN)

    # irq pin
    irq_pin = prepare_irq_pin(LORA_IRQ_PIN)if LORA_IRQ_PIN else None   
               
    # spi
    spi = prepare_spi(spi)
    
        
if IS_RPi:
    WORKER_NAME = 'RPi_366'
    
    
if IS_PC:
    WORKER_NAME = 'PC_366'    