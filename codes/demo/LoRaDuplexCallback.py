import time
from config import NODE_NAME, millisecond


msgCount = 0            # count of outgoing messages
INTERVAL = 2000         # interval between sends
INTERVAL_BASE = 2000    # interval between sends base
 

def duplexCallback(lora):    
    print("LoRa Duplex with callback")    
    lora.onReceive(on_receive)  # register the receive callback
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
            sendMessage(lora, message)                              # send message
            msgCount += 1 

            lora.receive()                                          # go into receive mode
    

def sendMessage(lora, outgoing):
    lora.println(outgoing)
    # print("Sending message:\n{}\n".format(outgoing))

    
def on_receive(lora, payload):
    lora.controller.blink_led()   
            
    try:
        print("*** Received message ***\n{}".format(payload.decode()))
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(lora.packetRssi()))
    