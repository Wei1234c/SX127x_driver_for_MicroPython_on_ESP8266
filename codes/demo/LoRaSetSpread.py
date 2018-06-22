from config_lora import millisecond


msgCount = 0            # count of outgoing messages
INTERVAL = 2000         # interval between sends
INTERVAL_BASE = 2000    # interval between sends base


def setSpread(lora): 
    print("LoRa Duplex - Set spreading factor")
    lora.setSpreadingFactor(8)           # ranges from 6-12,default 7 see API docs
    
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
        lora.blink_led() 
                
        try:
            payload = lora.read_payload()
            print("*** Received message ***\n{}".format(payload.decode()))
        except Exception as e:
            print(e)
        print("RSSI: {}".format(str(lora.packetRssi())))
        print("Snr: {}\n".format(str(lora.packetSnr()))) 

