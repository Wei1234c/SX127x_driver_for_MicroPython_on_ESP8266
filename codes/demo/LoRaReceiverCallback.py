import led


def receiveCallback(lora): 
    
    print("LoRa Receiver Callback")
    
    # register the receive callback
    lora.onReceive(on_receive)

    # put the radio into receive mode
    lora.receive()  

    
def on_receive(lora, packetSize):
        
    led.blink_on_board_led(on_seconds = 0.1, off_seconds = 0.1)
    
    # read packet
    payload = bytearray()

    while (lora.available()):
        b = lora.read()
        if b: payload.append(b)

    print("*** Received message ***\n{}".format(bytes(payload).decode())) 
    print("with RSSI {}\n".format(lora.packetRssi()))