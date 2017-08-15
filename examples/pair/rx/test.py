import sx127x
import config 

# import LoRaDumpRegisters
# import LoRaSender
import LoRaReceiver
# import LoRaSetSpread
# import LoRaSetSyncWord
# import LoRaReceiverCallback
# import LoRaDuplex
# import LoRaDuplexCallback
 
 
def main(): 
    controller = config.Controller()
    lora = sx127x.SX127x(controller)
    print('lora', lora)

    # LoRaDumpRegisters.dumpRegisters(lora)
    # LoRaSender.send(lora)    
    LoRaReceiver.receive(lora)
    # LoRaSetSpread.setSpread(lora)
    # LoRaSetSyncWord.setSyncWord(lora)
    # LoRaReceiverCallback.receiveCallback(lora)
    # LoRaDuplex.duplex(lora)
    # LoRaDuplexCallback.duplexCallback(lora)

    
if __name__ == '__main__':
    main()