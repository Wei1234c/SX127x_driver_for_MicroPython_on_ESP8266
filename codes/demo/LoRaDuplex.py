from config import NODE_NAME, millisecond

msgCount = 0            # count of outgoing messages
lastSendTime = 0        # last send time
interval = 2000         # interval between sends


def duplex(lora): 
    print("LoRa Duplex")  
    do_loop(lora)
    

def do_loop(lora):    
    lastSendTime = millisecond()
    interval = (lastSendTime % 2000) + 1000
    global msgCount

    while True:
        if (millisecond() - lastSendTime > interval):
            message = "HeLoRa World! - from {} {}".format(NODE_NAME, msgCount)
            sendMessage(lora, message)
            
            lastSendTime = millisecond()          # timestamp the message
            interval = (lastSendTime % 2000) + 1000    # 2-3 seconds
            msgCount += 1

        # parse for a packet, and call onReceive with the result:
        receive(lora) 
    

def sendMessage(lora, outgoing):
    lora.println(outgoing)
    print("Sending message:\n{}\n".format(outgoing))
    

def receive(lora):
    if lora.receivedPacket():    
        lora.controller.blink_led() 
        payload = lora.read_payload()
                
        try:
            print("*** Received message ***\n{}".format(payload.decode()))
        except Exception as e:
            print(e)
        print("with RSSI {}\n".format(lora.packetRssi()))
        