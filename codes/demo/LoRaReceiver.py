def receive(lora):
    print("LoRa Receiver")

    while True:
        # try to parse packet
        packetSize = lora.parsePacket()
        
        if packetSize:            
            lora.controller.blink_led(on_seconds = 0.1, off_seconds = 0.1)
            
            # read packet
            payload = bytearray()
            
            while (lora.available()):
                b = lora.read()
                if b: payload.append(b)
                
            print("Received packet\n{}".format(bytes(payload).decode()))
            print("with RSSI: {}\n".format(lora.packetRssi()))