import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
try:
    GPIO.cleanup()
except Exception as e:
    print(e)

import spidev
import config
import led 
 
ON_BOARD_LED_PIN_NO = 47  # RPi's on-board LED
ON_BOARD_LED_HIGH_IS_ON = True
GPIO_PINS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 16, 27,)

PIN_ID_FOR_LORA_RESET = 5

PIN_ID_FOR_LORA_SS = 7
PIN_ID_FOR_LORA_SCK = 11
PIN_ID_FOR_MOSI = 10
PIN_ID_FOR_MISO = 9

PIN_ID_FOR_LORA_DIO0 = 4
PIN_ID_FOR_LORA_DIO1 = None 
PIN_ID_FOR_LORA_DIO2 = None 
PIN_ID_FOR_LORA_DIO3 = None
PIN_ID_FOR_LORA_DIO4 = None
PIN_ID_FOR_LORA_DIO5 = None

class mock:
    pass   

def prepare_pin(pin_id, in_out = GPIO.OUT):
    if pin_id:
        GPIO.setup(pin_id, in_out) 
        new_pin = mock()
        new_pin.pin_id = pin_id
        
        if in_out == GPIO.OUT:
            new_pin.low = lambda : GPIO.output(pin_id, GPIO.LOW)
            new_pin.high = lambda : GPIO.output(pin_id, GPIO.HIGH)
        else:
            new_pin.value = lambda : GPIO.input(pin_id)
            
        return new_pin

def prepare_irq_pin(pin_id): 
    pin = prepare_pin(pin_id, GPIO.IN) 
    if pin:       
        pin.set_handler_for_irq_on_rising_edge = \
            lambda handler: GPIO.add_event_detect(pin.pin_id,
                                                  GPIO.RISING,
                                                  callback = handler)  
        pin.detach_irq = lambda : GPIO.remove_event_detect(pin.pin_id) 
        return pin

def prepare_spi(spi): 
    if spi:
        spi.open(0, 0) 
        spi.max_speed_hz = 10000000
        spi.mode = 0b00
        spi.lsbfirst = False
        new_spi = mock()  

        def transfer(address, value = 0x00):        
            response = bytearray(1)             
            response.append(spi.xfer([address, value])[1])
            return response
            
        new_spi.transfer = transfer
        new_spi.close = spi.close         
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
        
        spi = None
        
        try: 
            spi = spidev.SpiDev()            
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
            
        except Exception as e:
            print(e)
            GPIO.cleanup()
            if spi: spi.close()
            
    def __exit__(self):
        GPIO.cleanup()
        self.spi.close()