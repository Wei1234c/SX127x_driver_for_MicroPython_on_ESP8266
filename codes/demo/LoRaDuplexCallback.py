import time
from config import NODE_NAME, millisecond

msgCount = 0            # count of outgoing messages
localAddress = 0xBB     # address of this device
broadcastAddress = 0xFF # destination to send to
lastSendTime = 0        # last send time
interval = 2000         # interval between sends
 

def duplexCallback(lora): 
    
    print("LoRa Duplex with callback")
    # lora.setSpreadingFactor(8)           # ranges from 6-12,default 7 see API docs

    # register the receive callback
    lora.onReceive(on_receive) 
    lora.receive()  # go into receive mode
    do_loop(lora)  
  

def do_loop(lora):    
    
    lastSendTime = millisecond()
    interval = (lastSendTime % 2000) + 1000
    global msgCount

    while True:
        if (millisecond() - lastSendTime > interval):
            message = "HeLoRa World! - from {} {}".format(NODE_NAME, msgCount)
            sendMessage(lora, message)
            print("Sending message:\n{}\n".format(message))
            lastSendTime = millisecond()          # timestamp the message
            interval = (lastSendTime % 2000) + 1000    # 2-3 seconds
            msgCount += 1 

            lora.receive()  # go back into receive mode
    

def sendMessage(lora, outgoing, destination = broadcastAddress):
    lora.println(outgoing)

    
def on_receive(lora, packetSize):
    if packetSize == 0: 
        return False       # if there's no packet, return
        
    lora.controller.blink_led() 
    payload = lora.read_payload()    
            
    try:
        print("*** Received message ***\n{}".format(payload.decode())) 
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(lora.packetRssi()))
    