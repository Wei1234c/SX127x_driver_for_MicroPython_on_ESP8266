from config import NODE_NAME, millisecond

msgCount = 0            # count of outgoing messages
INTERVAL = 1000         # interval between sends
INTERVAL_BASE = 2000    # interval between sends base


def duplex(lora): 
    print("LoRa Duplex")  
    do_loop(lora)
    

def do_loop(lora):    
    global msgCount
    
    lastSendTime = 0
    interval = 0

    while True:
        now = millisecond()
        if now < lastSendTime: lastSendTime = now 
        
        if (now - lastSendTime > interval):
            lastSendTime = now                                      # timestamp the message
            interval = (lastSendTime % INTERVAL) + INTERVAL_BASE    # 2-3 seconds   
            
            message = "{} {}".format(NODE_NAME, msgCount)
            sendMessage(lora, message)                  # send message
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
        