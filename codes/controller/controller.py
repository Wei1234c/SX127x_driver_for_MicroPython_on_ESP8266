import time 

            
class Controller:

    class Mock:
        pass  
        
    spi = None
    
    ON_BOARD_LED_PIN_NO = None
    ON_BOARD_LED_HIGH_IS_ON = True
    GPIO_PINS = []
                 
    PIN_ID_FOR_LORA_RESET = None 

    PIN_ID_FOR_LORA_SS = None
    PIN_ID_FOR_LORA_SCK = None 
    PIN_ID_FOR_MOSI = None 
    PIN_ID_FOR_MISO = None 

    PIN_ID_FOR_LORA_DIO0 = None 
    PIN_ID_FOR_LORA_DIO1 = None 
    PIN_ID_FOR_LORA_DIO2 = None 
    PIN_ID_FOR_LORA_DIO3 = None
    PIN_ID_FOR_LORA_DIO4 = None
    PIN_ID_FOR_LORA_DIO5 = None
    
    
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

        self.pin_led = self.prepare_pin(pin_id_led)
        self.on_board_led_high_is_on = on_board_led_high_is_on
        self.pin_reset = self.prepare_pin(pin_id_reset)
        self.pin_ss = self.prepare_pin(pin_id_ss)
        
        self.spi = self.prepare_spi(spi)  # needs pin_ss, should be prepared after pin_ss.
                
        self.pin_RxDone = self.prepare_irq_pin(pin_id_RxDone)
        self.pin_RxTimeout = self.prepare_irq_pin(pin_id_RxTimeout)
        self.pin_ValidHeader = self.prepare_irq_pin(pin_id_ValidHeader)
        self.pin_CadDone = self.prepare_irq_pin(pin_id_CadDone)
        self.pin_CadDetected = self.prepare_irq_pin(pin_id_CadDetected)
        self.pin_PayloadCrcError = self.prepare_irq_pin(pin_id_PayloadCrcError)        
         
        self.blink_led(*blink_on_start)
        
    
    def prepare_pin(self, pin_id, in_out = None):
        reason = '''
            # a pin should provide:
            # .low()
            # .high()
            # .value()  # read input.
            # .irq()  # ref to the irq function of real pin object.
        '''
        raise NotImplementedError('reason')
        

    def prepare_irq_pin(self, pin_id):
        reason = '''
            # a irq_pin should provide:
            # .set_handler_for_irq_on_rising_edge()  # to set trigger and handler.
            # .detach_irq()
        '''
        raise NotImplementedError('reason')
        

    def prepare_spi(self, spi): 
        reason = '''
            # a spi should provide: 
            # .close()
            # .transfer(address, value = 0x00) 
        '''
        raise NotImplementedError('reason')        
        

    def blink_led(self, times = 1, on_seconds = 0.1, off_seconds = 0.1):
        for i in range(times):
            self.pin_led.high() if self.on_board_led_high_is_on else self.pin_led.low()
            time.sleep(on_seconds)
            self.pin_led.low() if self.on_board_led_high_is_on else self.pin_led.high()
            time.sleep(off_seconds) 

        
    def __exit__(self): 
        self.spi.close()        