import sx127x
import config


# import LoRaDumpRegisters
import LoRaSender
# import LoRaReceiver
# import LoRaSetSpread
# import LoRaSetSyncWord
# import LoRaReceiverCallback
# import LoRaDuplex
# import LoRaDuplexCallback

# lora = sx127x.SX127x(SPI(1, baudrate=10000000, polarity=0, phase=0))
# print('lora.begin()', lora.begin())
 
 
def main(): 
    lora = sx127x.SX127x(config.spi, 
                         ss_pin_id = config.LORA_SS_PIN, 
                         reset_pin_id = config.LORA_RESET_PIN, 
                         irq_pin_id = config.LORA_IRQ_PIN)
    print('lora', lora)

    # LoRaDumpRegisters.dumpRegisters(lora)
    LoRaSender.send(lora)    
    # LoRaReceiver.receive(lora)
    # LoRaSetSpread.setSpread(lora)
    # LoRaSetSyncWord.setSyncWord(lora)
    # LoRaReceiverCallback.receiveCallback(lora)
    # LoRaDuplex.duplex(lora)
    # LoRaDuplexCallback.duplexCallback(lora)

    
if __name__ == '__main__':
    main()