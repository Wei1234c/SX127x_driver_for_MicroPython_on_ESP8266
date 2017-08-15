from machine import Pin, SPI, reset
import config
import led 
  

PIN_ID_FOR_LORA_RESET = 4 

PIN_ID_FOR_LORA_SS = 15
PIN_ID_FOR_LORA_SCK = 14 
PIN_ID_FOR_MOSI = 13 
PIN_ID_FOR_MISO = 12 

PIN_ID_FOR_LORA_DIO0 = 5 
PIN_ID_FOR_LORA_DIO1 = None 
PIN_ID_FOR_LORA_DIO2 = None 
PIN_ID_FOR_LORA_DIO3 = None
PIN_ID_FOR_LORA_DIO4 = None
PIN_ID_FOR_LORA_DIO5 = None


if config.IS_ESP8266:
    ON_BOARD_LED_PIN_NO = 2
    ON_BOARD_LED_HIGH_IS_ON = False
    GPIO_PINS = (0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16)
    spi = SPI(1, baudrate = 10000000, polarity = 0, phase = 0)        
    
if config.IS_ESP32:
    ON_BOARD_LED_PIN_NO = 2
    ON_BOARD_LED_HIGH_IS_ON = True
    GPIO_PINS = (0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16)  
    
    spi = None
    
    try:
        spi = SPI(1, baudrate = 10000000, polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
                  sck = Pin(PIN_ID_FOR_LORA_SCK, Pin.OUT), 
                  mosi = Pin(PIN_ID_FOR_MOSI, Pin.OUT), 
                  miso = Pin(PIN_ID_FOR_MISO, Pin.IN)) 
    except Exception as e:
        print(e)
        if spi: spi.deinit()
        reset()  # in case SPI is already in use, need to reset. 


class mock:
    pass   

def prepare_pin(pin_id, in_out = Pin.OUT):
    if pin_id:
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
    if pin:
        pin.set_handler_for_irq_on_rising_edge = lambda handler: pin.irq(handler = handler, trigger = Pin.IRQ_RISING)
        pin.detach_irq = lambda : pin.irq(handler = None, trigger = 0)
        return pin

def prepare_spi(spi): 
    if spi:
        ss = prepare_pin(PIN_ID_FOR_LORA_SS)
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
        new_spi.close = spi.deinit
        
        return new_spi


            
class Controller:
        
    # The controller can be ESP8266, ESP32, Raspberry Pi, or a PC.
    # The controller needs to provide an interface consisted of:
    # 1. a SPI, with transfer function.
    # 2. a reset pin, with low(), high() functions.
    # 3. IRQ pinS , to be triggered by RFM96W's DIO0~5 pins. These pins each has two functions:
    #   3.1 set_handler_for_irq_on_rising_edge() 
    #   3.2 detach_irq()
    # 4. a function to blink on-board LED. 
        
    def __init__(self, 
                 pin_id_led = ON_BOARD_LED_PIN_NO, 
                 pin_id_reset = PIN_ID_FOR_LORA_RESET, 
                 pin_id_RxDone = PIN_ID_FOR_LORA_DIO0,
                 pin_id_RxTimeout = PIN_ID_FOR_LORA_DIO1,
                 pin_id_ValidHeader = None,
                 pin_id_CadDone = PIN_ID_FOR_LORA_DIO3,
                 pin_id_CadDetected = PIN_ID_FOR_LORA_DIO4,
                 pin_id_PayloadCrcError = None):
        
        self.spi = prepare_spi(spi)
        
        self.pin_led = prepare_pin(pin_id_led)
        self.blink_led = lambda times = 1, \
                                on_seconds = 0.1, \
                                off_seconds = 0.1: \
                                led.blink(self.pin_led,
                                          times = times,
                                          on_seconds = on_seconds,
                                          off_seconds = off_seconds,
                                          high_is_on = ON_BOARD_LED_HIGH_IS_ON) 
        self.blink_led(2, 0.5, 0.5)
        
        self.pin_reset = prepare_pin(pin_id_reset)
        
        self.pin_RxDone = prepare_irq_pin(pin_id_RxDone)
        self.pin_RxTimeout = prepare_irq_pin(pin_id_RxTimeout)
        self.pin_ValidHeader = prepare_irq_pin(pin_id_ValidHeader)
        self.pin_CadDone = prepare_irq_pin(pin_id_CadDone)
        self.pin_CadDetected = prepare_irq_pin(pin_id_CadDetected)
        self.pin_PayloadCrcError = prepare_irq_pin(pin_id_PayloadCrcError)
        
    def __exit__(self): 
        self.spi.close()        