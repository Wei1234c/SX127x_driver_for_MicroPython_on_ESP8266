def receive(lora):
    print("LoRa Receiver")

    while True:
        # try to parse packet
        packetSize = lora.parsePacket()
        
        if packetSize:            
            lora.controller.blink_led()
            
            # read packet
            payload = lora.read_payload()
                    
            try:
                print("*** Received message ***\n{}".format(payload.decode()))
            except Exception as e:
                print(e)
            print("with RSSI: {}\n".format(lora.packetRssi()))