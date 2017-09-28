from time import sleep
from machine import unique_id, Pin, I2C
import ubinascii
import display_ssd1306_i2c

def mac2eui(mac):
    mac = mac[0:6] + 'fffe' + mac[6:] 
    return hex(int(mac[0:2], 16) ^ 2)[2:] + mac[2:] 

def get_eui():
    id = ubinascii.hexlify(unique_id()).decode()  
    return mac2eui(id) 
    
def blink(pin_id, low_seconds = 0.05, high_seconds = 0.05):
    pin = Pin(pin_id, Pin.OUT)
    pin.value(0)
    sleep(low_seconds)
    pin.value(1)
    sleep(high_seconds)

print('EUI', get_eui()) 
blink(16)
Pin(15, Pin.OUT) 

oled = display_ssd1306_i2c.Display(width = 128, height = 64, 
                                   scl_pin_id = 15, sda_pin_id = 4, 
                                   freq = 400000) 

def show_packet(payload_string, rssi = None):
    oled.clear()
    line_idx = 0
    if rssi:
        oled.show_text('RSSI: {}'.format(rssi), x = 0, y = line_idx * 10, clear_first = False, show_now = False)
        line_idx += 1        
    for line, x, y in _wrap(payload_string, start_line = line_idx):
        oled.show_text(line, x = x, y = y, clear_first = False, show_now = False)
    oled.show()
    
def _wrap(text, start_line = 0, 
          height_per_line = 8, width_per_char = 8,
          start_pixel_each_line = 0):
          
    width = 128
    height = 32
    chars_per_line = width//width_per_char
    max_lines = height//height_per_line - start_line
    lines = [(text[chars_per_line*line: chars_per_line*(line+1)], 
              start_pixel_each_line, 
              height_per_line*(line+start_line))
             for line in range(max_lines)]
    return lines
     

# show_packet('Hello !', -128)
message = '12345678901234567890123456789012345678901234567890123456789012345678901234567890'
show_packet(message, -128)
# show_packet(message)
    