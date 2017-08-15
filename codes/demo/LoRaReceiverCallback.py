def receiveCallback(lora): 
    
    print("LoRa Receiver Callback")
    
    # register the receive callback
    lora.onReceive(on_receive)

    # put the radio into receive mode
    lora.receive()  

    
def on_receive(lora, packetSize):
        
    lora.controller.blink_led()
    
    # read packet
    payload = lora.read_payload()
            
    try:
        print("*** Received message ***\n{}".format(payload.decode()))
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(lora.packetRssi()))