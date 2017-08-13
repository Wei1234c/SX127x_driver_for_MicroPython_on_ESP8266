import time 
from config import WORKER_NAME

msgCount = 0            # count of outgoing messages
localAddress = 0xBB     # address of this device
broadcastAddress = 0xFF # destination to send to
lastSendTime = 0        # last send time
interval = 2000         # interval between sends


def duplex(lora): 
    print("LoRa Duplex")    
    # lora.setSpreadingFactor(8)
    
    do_loop(lora)
    

def do_loop(lora):    
    
    lastSendTime = time.ticks_ms()
    interval = (lastSendTime % 2000) + 1000
    global msgCount

    while True:
        if (time.ticks_ms() - lastSendTime > interval):
            message = "HeLoRa World! - from {} {}".format(WORKER_NAME, msgCount)
            sendMessage(lora, message)
            print("Sending message:\n{}\n".format(message))
            lastSendTime = time.ticks_ms()          # timestamp the message
            interval = (lastSendTime % 2000) + 1000    # 2-3 seconds
            msgCount += 1

        # parse for a packet, and call onReceive with the result:
        onReceive(lora, lora.parsePacket()) 
    

def sendMessage(lora, outgoing, destination = broadcastAddress):
    global msgCount
    
    lora.beginPacket()                   # start packet
    
    # meta = bytearray()         
    # meta.append(destination)              # add destination address
    # meta.append(localAddress)             # add sender address
    # meta.append(msgCount)                 # add message ID
    # meta.append(len(outgoing))            # add payload length
    # lora.write(meta)
    lora.print(outgoing)                 # add payload
    
    lora.endPacket()                     # finish packet and send it
    

def onReceive(lora, packetSize):
    if packetSize <= 0: 
        return False       # if there's no packet, return
    
    lora.controller.blink_led(on_seconds = 0.1, off_seconds = 0.1)
    
    # read packet header bytes:
    # recipient = lora.read()         # recipient address
    # sender = lora.read()            # sender address
    # incomingMsgId = lora.read()     # incoming msg ID
    # incomingLength = lora.read()    # incoming msg length

    payload = bytearray()

    while (lora.available()):
        b = lora.read()
        if b and 32 <= b <= 126:
            payload.append(b)
        
    print("*** Received message ***\n{}".format(bytes(payload).decode())) 
    print("with RSSI {}\n".format(lora.packetRssi()))

    # if len(payload) != incomingLength :   # check length for error
        # print(len(payload), incomingLength)
        # print("Error: message length does not match length")
        
    # # if the recipient isn't this device or broadcast,
    # elif recipient != localAddress and recipient != broadcastAddress :
        # print("This message is not for me or broadcasted.")
    
    # else:
        # # if message is for this device, or broadcast, print details:
        # print("*** Received message ***\nReceived from: 0x{0:0x}".format(sender))
        # print("Sent to: 0x{0:0x}".format(recipient))
        # print("Message ID: {}".format(incomingMsgId))
        # print("Message length: {}".format(incomingLength))
        # print("Message: {}".format(bytes(payload).decode()))
        # print("RSSI: {}".format(lora.packetRssi()))
        # print("Snr: {}\n".format(lora.packetSnr()))
        
        # return True