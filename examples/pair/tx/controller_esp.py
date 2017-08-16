from machine import Pin, SPI, reset
import config
import controller 
 

class Controller(controller.Controller):

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
        GPIO_PINS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
                     12, 13, 14, 15, 16, 17, 18, 19, 21, 22,
                     23, 25, 26, 27, 32, 34, 35, 36, 37, 38, 39)
                     
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

    
    def __init__(self, 
                 spi = spi, 
                 pin_id_led = ON_BOARD_LED_PIN_NO, 
                 on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
                 pin_id_reset = PIN_ID_FOR_LORA_RESET, 
                 pin_id_ss = PIN_ID_FOR_LORA_SS,
                 pin_id_RxDone = PIN_ID_FOR_LORA_DIO0,
                 pin_id_RxTimeout = PIN_ID_FOR_LORA_DIO1,
                 pin_id_ValidHeader = PIN_ID_FOR_LORA_DIO2,
                 pin_id_CadDone = PIN_ID_FOR_LORA_DIO3,
                 pin_id_CadDetected = PIN_ID_FOR_LORA_DIO4,
                 pin_id_PayloadCrcError = PIN_ID_FOR_LORA_DIO5, 
                 blink_on_start = (2, 0.5, 0.5)):
                
        super().__init__(spi, 
                         pin_id_led,
                         on_board_led_high_is_on,
                         pin_id_reset, 
                         pin_id_ss,
                         pin_id_RxDone,
                         pin_id_RxTimeout,
                         pin_id_ValidHeader,
                         pin_id_CadDone,
                         pin_id_CadDetected,
                         pin_id_PayloadCrcError)

        
    def prepare_pin(self, pin_id, in_out = Pin.OUT):
        if pin_id:
            pin = Pin(pin_id, in_out)
            new_pin = Controller.Mock()
            new_pin.value = pin.value
            
            if in_out == Pin.OUT:
                new_pin.low = lambda : pin.value(0)
                new_pin.high = lambda : pin.value(1)        
            else:
                new_pin.irq = pin.irq 
                
            return new_pin

            
    def prepare_irq_pin(self, pin_id): 
        pin = self.prepare_pin(pin_id, Pin.IN) 
        if pin:
            pin.set_handler_for_irq_on_rising_edge = lambda handler: pin.irq(handler = handler, trigger = Pin.IRQ_RISING)
            pin.detach_irq = lambda : pin.irq(handler = None, trigger = 0)
            return pin

            
    def prepare_spi(self, spi): 
        if spi:
            self.pin_ss.high()
            spi.init()               
            new_spi = Controller.Mock()  

            def transfer(address, value = 0x00):        
                response = bytearray(1)

                self.pin_ss.low()
                 
                spi.write(bytes([address]))
                spi.write_readinto(bytes([value]), response)

                self.pin_ss.high()

                return response
                
            new_spi.transfer = transfer
            new_spi.close = spi.deinit
            
            return new_spi
            
        
    def __exit__(self): 
        self.spi.close()
        