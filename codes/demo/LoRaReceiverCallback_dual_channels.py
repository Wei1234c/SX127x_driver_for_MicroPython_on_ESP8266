def receiveCallback(lora1, lora2): 
    
    print("LoRa Receiver Callback Dual Channels")
    
    # register the receive callback
    lora1.onReceive(on_receive)
    lora2.onReceive(on_receive)

    # put the radio into receive mode
    lora1.receive()  
    lora2.receive()

    
def on_receive(lora, payload):
    lora.blink_led()
    
    try:
        print("*** Received message ***\n{}: {} {} {}".format(lora.name, 
                                                              lora.pin_ss.pin_id, 
                                                              lora.pin_RxDone.pin_id,
                                                              payload))
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(lora.packetRssi()))
    