import RPi.GPIO as GPIO
import spidev
import controller 


GPIO.setmode(GPIO.BCM)

try:
    GPIO.cleanup()
except Exception as e:
    print(e)
    


class Controller(controller.Controller):
    
    # BOARD config
    ON_BOARD_LED_PIN_NO = 47  # RPi's on-board LED
    ON_BOARD_LED_HIGH_IS_ON = True
    GPIO_PINS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,)

    
    # LoRa config
    PIN_ID_FOR_LORA_RESET = 5

    PIN_ID_FOR_LORA_SS = 8
    PIN_ID_SCK = 11
    PIN_ID_MOSI = 10
    PIN_ID_MISO = 9

    PIN_ID_FOR_LORA_DIO0 = 17
    PIN_ID_FOR_LORA_DIO1 = None 
    PIN_ID_FOR_LORA_DIO2 = None 
    PIN_ID_FOR_LORA_DIO3 = None
    PIN_ID_FOR_LORA_DIO4 = None
    PIN_ID_FOR_LORA_DIO5 = None 
    

    def __init__(self, 
                 pin_id_led = ON_BOARD_LED_PIN_NO, 
                 on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
                 pin_id_reset = PIN_ID_FOR_LORA_RESET,
                 blink_on_start = (2, 0.5, 0.5)):
                
        super().__init__(pin_id_led,
                         on_board_led_high_is_on,
                         pin_id_reset,
                         blink_on_start)

         
    def prepare_pin(self, pin_id, in_out = GPIO.OUT):
        if pin_id is not None:
            GPIO.setup(pin_id, in_out) 
            new_pin = Controller.Mock()
            new_pin.pin_id = pin_id
            
            if in_out == GPIO.OUT:
                new_pin.low = lambda : GPIO.output(pin_id, GPIO.LOW)
                new_pin.high = lambda : GPIO.output(pin_id, GPIO.HIGH)
            else:
                new_pin.value = lambda : GPIO.input(pin_id)
                
            return new_pin
            

    def prepare_irq_pin(self, pin_id): 
        pin = self.prepare_pin(pin_id, GPIO.IN) 
        if pin:       
            pin.set_handler_for_irq_on_rising_edge = \
                lambda handler: GPIO.add_event_detect(pin.pin_id,
                                                      GPIO.RISING,
                                                      callback = handler)  
            pin.detach_irq = lambda : GPIO.remove_event_detect(pin.pin_id) 
            return pin

            
    def get_spi(self):             
        spi = None
        
        try: 
            spi = spidev.SpiDev()
            bus = 0
            device = 0
            spi.open(bus, device)            
            spi.max_speed_hz = 10000000
            spi.mode = 0b00
            spi.lsbfirst = False
                
        except Exception as e:
            print(e)
            GPIO.cleanup()
            if spi:
                spi.close()
                spi = None
        
        return spi
        
            
    # https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md
    # https://www.raspberrypi.org/forums/viewtopic.php?f=44&t=19489
    def prepare_spi(self, spi): 
        if spi:            
            new_spi = Controller.Mock()

            def transfer(pin_ss, address, value = 0x00):        
                response = bytearray(1)
                
                pin_ss.low()
                response.append(spi.xfer2([address, value])[1])                
                pin_ss.high()
                
                return response
                
            new_spi.transfer = transfer
            new_spi.close = spi.close         
            return new_spi 
            
        
    def __exit__(self): 
        GPIO.cleanup()
        self.spi.close()
        