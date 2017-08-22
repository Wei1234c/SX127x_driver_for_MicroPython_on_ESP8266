import LoRaSetSpread 


def setSyncWord(lora):
 
    print("LoRa Duplex - set Sync Word")
    lora.setSyncWord(0xF3)      # ranges from 0-0xFF, default 0x34, see API docs 
    
    LoRaSetSpread.do_loop(lora)

