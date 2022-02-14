# https://learn.adafruit.com/micropython-hardware-ssd1306-oled-display/software
import time
import machine 
import ssd1306


class Display:
    
    def __init__(self, 
                 width = 128, height = 64, 
                 scl_pin_id = 5, sda_pin_id = 4,
                 freq = 400000): 
                 
        self.width = width
        self.height = height
        self.i2c = machine.I2C(scl = machine.Pin(scl_pin_id, machine.Pin.OUT),
                               sda = machine.Pin(sda_pin_id), 
                               freq = freq) 
        self.display = ssd1306.SSD1306_I2C(width, height, self.i2c)
        self.show = self.display.show
        

    def clear(self):
        self.display.fill(0)
        self.display.show()
        
        
    def show_text(self, text, x = 0, y = 0, clear_first = True, show_now = True, hold_seconds = 0):  
        if clear_first: self.display.fill(0)
        self.display.text(text, x, y)
        if show_now: 
            self.display.show()
            if hold_seconds > 0: time.sleep(hold_seconds) 

            
    def wrap(self, text, start_line = 0, 
             height_per_line = 8, width_per_char = 8,
             start_pixel_each_line = 0):
             
        chars_per_line = self.width//width_per_char
        max_lines = self.height//height_per_line - start_line
        lines = [(text[chars_per_line*line: chars_per_line*(line+1)], start_pixel_each_line, height_per_line*(line+start_line))
                 for line in range(max_lines)]
                    
        return lines
        

    def show_text_wrap(self, text,
                       start_line = 0, height_per_line = 8, width_per_char = 8, start_pixel_each_line = 0, 
                       clear_first = True, show_now = True, hold_seconds = 0):  
          
        if clear_first: self.clear()
        
        for line, x, y in self.wrap(text, start_line, height_per_line, width_per_char, start_pixel_each_line):
            self.show_text(line, x, y, clear_first = False, show_now = False) 
            
        if show_now: 
            self.display.show()
            if hold_seconds > 0: time.sleep(hold_seconds) 
    
                
    def show_datetime(self, year, month, day, hour, minute, second):   
        datetime = [year, month, day, hour, minute, second]
        datetime_str = ["{0:0>2}".format(d) for d in datetime]        
        
        self.show_text(text = '-'.join(datetime_str[:3]),
                        x = 0, y = 0, clear_first = True, show_now = False)
        self.show_text(text = ':'.join(datetime_str[3:6]),
                        x = 0, y = 10, clear_first = False, show_now = True)

                        
    def show_time(self, year, month, day, hour, minute, second):   
        self.show_datetime(year, month, day, hour, minute, second)
                            