from config import millisecond


msgCount = 0            # count of outgoing messages
interval = 2000          # interval between sends
lastSendTime = 0        # time of last packet send


def setSpread(lora): 
    print("LoRa Duplex - Set spreading factor")
    lora.setSpreadingFactor(8)           # ranges from 6-12,default 7 see API docs
    
    do_loop(lora)


def do_loop(lora):    
    lastSendTime = millisecond()
    interval = (lastSendTime % 2000) + 1000
    global msgCount

    while True:
        if (millisecond() - lastSendTime > interval):
            message = "HeLoRa World! {}".format(msgCount)
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
        print("RSSI: {}".format(str(lora.packetRssi())))
        print("Snr: {}\n".format(str(lora.packetSnr()))) 

