import sx127x
import config_lora 


import LoRaReceiverCallback_dual_channels
# import LoRaReceiverCallback

if config_lora.IS_ESP8266: 
    PIN_ID_SS_1 = 15
    PIN_ID_SS_2 = 16
    PIN_ID_FOR_LORA1_DIO0 = 5
    PIN_ID_FOR_LORA2_DIO0 = 0
if config_lora.IS_ESP32:
    PIN_ID_SS_1 = 15
    PIN_ID_SS_2 = 17
    PIN_ID_FOR_LORA1_DIO0 = 5
    PIN_ID_FOR_LORA2_DIO0 = 16
if config_lora.IS_RPi:        
    PIN_ID_SS_1 = 25
    PIN_ID_SS_2 = 7
    PIN_ID_FOR_LORA1_DIO0 = 17
    PIN_ID_FOR_LORA2_DIO0 = 27
 

def main(): 
    
    # Controller(spi = spi, 
               # pin_id_led = ON_BOARD_LED_PIN_NO, 
               # on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
               # pin_id_reset = PIN_ID_FOR_LORA_RESET, 
               # blink_on_start = (2, 0.5, 0.5))               
    controller = config_lora.Controller()
    
    
    # SX127x(name = 'SX127x',
           # parameters = {'frequency': 433E6, 'tx_power_level': 2, 'signal_bandwidth': 125E3,
                         # 'spreading_factor': 8, 'coding_rate': 5, 'preamble_length': 8,
                         # 'implicitHeader': False, 'sync_word': 0x12, 'enable_CRC': False},
           # onReceive = None)
           
    # controller.add_transceiver(transceiver,
                               # pin_id_ss = PIN_ID_FOR_LORA_SS,
                               # pin_id_RxDone = PIN_ID_FOR_LORA_DIO0,
                               # pin_id_RxTimeout = PIN_ID_FOR_LORA_DIO1,
                               # pin_id_ValidHeader = PIN_ID_FOR_LORA_DIO2,
                               # pin_id_CadDone = PIN_ID_FOR_LORA_DIO3,
                               # pin_id_CadDetected = PIN_ID_FOR_LORA_DIO4,
                               # pin_id_PayloadCrcError = PIN_ID_FOR_LORA_DIO5)                             
    lora1 = controller.add_transceiver(sx127x.SX127x(name = 'LoRa1'),
                                       pin_id_ss = PIN_ID_SS_1,
                                       pin_id_RxDone = PIN_ID_FOR_LORA1_DIO0)
    lora2 = controller.add_transceiver(sx127x.SX127x(name = 'LoRa2'),
                                       pin_id_ss = PIN_ID_SS_2,
                                       pin_id_RxDone = PIN_ID_FOR_LORA2_DIO0) 

    LoRaReceiverCallback_dual_channels.receiveCallback(lora1, lora2)
    # LoRaReceiverCallback.receiveCallback(lora1)
    
if __name__ == '__main__':
    main()