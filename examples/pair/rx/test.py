import sx127x
import config 

# import LoRaDumpRegisters
# import LoRaSender
import LoRaReceiver
# import LoRaSetSpread
# import LoRaSetSyncWord
# import LoRaReceiverCallback
# import LoRaReceiverCallback_dual_channels
# import LoRaDuplex
# import LoRaDuplexCallback
# import LoRaPingPong

if config.IS_ESP8266: 
    PIN_ID_SS = 15
    PIN_ID_FOR_LORA_DIO0 = 5
if config.IS_ESP32:
    PIN_ID_SS = 15
    PIN_ID_FOR_LORA_DIO0 = 5
if config.IS_RPi:        
    PIN_ID_SS = 25
    PIN_ID_FOR_LORA_DIO0 = 17
    
 
def main(): 
    
    # Controller(spi = spi, 
               # pin_id_led = ON_BOARD_LED_PIN_NO,
               # on_board_led_high_is_on = ON_BOARD_LED_HIGH_IS_ON,
               # pin_id_reset = PIN_ID_FOR_LORA_RESET, 
               # pin_id_ss = PIN_ID_FOR_LORA_SS,
               # pin_id_RxDone = PIN_ID_FOR_LORA_DIO0,
               # pin_id_RxTimeout = PIN_ID_FOR_LORA_DIO1,
               # pin_id_ValidHeader = PIN_ID_FOR_LORA_DIO2,
               # pin_id_CadDone = PIN_ID_FOR_LORA_DIO3,
               # pin_id_CadDetected = PIN_ID_FOR_LORA_DIO4,
               # pin_id_PayloadCrcError = PIN_ID_FOR_LORA_DIO5, 
               # blink_on_start = (2, 0.5, 0.5))
    controller = config.Controller()
    
    # SX127x(controller,
           # name,
           # frequency = 433E6, tx_power_level = 2, 
           # signal_bandwidth = 125E3, spreading_factor = 8, coding_rate = 5,
           # preamble_length = 8, implicitHeaderMode = False, sync_word = 0x12, enable_CRC = False,
           # onReceive = None)
    lora = controller.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                      pin_id_ss = PIN_ID_SS,
                                      pin_id_RxDone = PIN_ID_FOR_LORA_DIO0)
    print('lora', lora)
    

    # LoRaDumpRegisters.dumpRegisters(lora)
    # LoRaSender.send(lora)    
    LoRaReceiver.receive(lora)
    # LoRaSetSpread.setSpread(lora)
    # LoRaSetSyncWord.setSyncWord(lora)
    # LoRaReceiverCallback.receiveCallback(lora)
    # LoRaReceiverCallback_dual_channels.receiveCallback(lora1, lora2)
    # LoRaDuplex.duplex(lora)
    # LoRaDuplexCallback.duplexCallback(lora)
    # LoRaPingPong.ping_pong(lora)

    
if __name__ == '__main__':
    main()