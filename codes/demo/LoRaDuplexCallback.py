import time
from config import NODE_NAME, millisecond


msgCount = 0            # count of outgoing messages
lastSendTime = 0        # last send time
interval = 2000         # interval between sends
 

def duplexCallback(lora):    
    print("LoRa Duplex with callback")    
    lora.onReceive(on_receive)  # register the receive callback
    lora.receive()              # go into receive mode
    do_loop(lora)
  

def do_loop(lora):    
    
    lastSendTime = millisecond()
    interval = (lastSendTime % 2000) + 1000
    global msgCount

    while True:
        if (millisecond() - lastSendTime > interval):
            message = "{} {}".format(NODE_NAME, msgCount)
            sendMessage(lora, message)                  # send message
            
            lastSendTime = millisecond()                # timestamp the message
            interval = (lastSendTime % 2000) + 1000     # 2-3 seconds
            msgCount += 1 

            lora.receive()  # go back into receive mode
    

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
    