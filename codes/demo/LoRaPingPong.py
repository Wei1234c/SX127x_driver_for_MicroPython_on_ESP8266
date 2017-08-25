import time
from config import NODE_NAME, millisecond


msgCount = 0            # count of outgoing messages
lastSendTime = 0        # last send time
interval = 2000         # interval between sends

messages = {} 

def ping_pong(lora):    
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
            now =  millisecond()            

            message = gen_message(NODE_NAME, msgCount, now)
            sendMessage(lora, message)                  # send message

            key = '{}_{}'.format(NODE_NAME, msgCount)
            messages[key] = {'node': NODE_NAME, 'msgCount': msgCount, 'ping': now, 'pong': None, 'done': False, 'elipse': None}
                        
            lastSendTime = millisecond()                # timestamp the message
            interval = (lastSendTime % 2000) + 1000     # 2-3 seconds
            msgCount += 1 

            lora.receive()  # go back into receive mode
    

def sendMessage(lora, outgoing):
    lora.println(outgoing)
    # print("Sending message:\n{}\n".format(outgoing))


def gen_message(NODE_NAME, msgCount, millisecond):
    return "{} {} {}".format(NODE_NAME, msgCount, millisecond)


def parse_message(payload):
    return tuple(payload.split())
    
    
def on_receive(lora, payload):
    lora.controller.blink_led()
    now = millisecond()   
    
    try:
        payload = payload.decode()
        sender_NODE_NAME, sender_msgCount, sent_millisecond = parse_message(payload)
        
        key = '{}_{}'.format(sender_NODE_NAME, sender_msgCount)
        item = messages.get(key)
        
        if item:  # matched message, calculate elipse time, and remove item.
            item['pong'] = now
            item['elipse'] = item['pong'] - item['ping']
            item['done'] = True
            
            message = "*** Pong after {} ms ***".format(item['elipse'])
            print(message)
            print(item)
            del messages[key]
        else:  # new message, send it back.
            print("*** Received message ***\n{}".format(payload))
            message = gen_message(sender_NODE_NAME, sender_msgCount, millisecond())
            sendMessage(lora, message)
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(lora.packetRssi()))
    