# https://learn.adafruit.com/micropython-hardware-ssd1306-oled-display/software
import time

import ssd1306



class Display(ssd1306.SSD1306_I2C):

    def __init__(self, i2c, width = 128, height = 64):
        super().__init__(width, height, i2c, addr = 0x3c, external_vcc = False)


    def clear(self):
        self.fill(0)
        self.show()


    def show_text(self, text, x = 0, y = 0, clear_first = True, show_now = True, hold_seconds = 0):
        if clear_first:
            self.fill(0)
        self.text(text, x, y)
        if show_now:
            self.show()
            if hold_seconds > 0:
                time.sleep(hold_seconds)


    def wrap(self, text, start_line = 0, height_per_line = 8, width_per_char = 8, start_pixel_each_line = 0):
        chars_per_line = self.width // width_per_char
        max_lines = self.height // height_per_line - start_line
        lines = [(text[chars_per_line * line: chars_per_line * (line + 1)], start_pixel_each_line,
                  height_per_line * (line + start_line)) for line in range(max_lines)]

        return lines


    def show_text_wrap(self, text, start_line = 0, height_per_line = 8, width_per_char = 8, start_pixel_each_line = 0,
                       clear_first = True, show_now = True, hold_seconds = 0):

        if clear_first:
            self.clear()

        for line, x, y in self.wrap(text, start_line, height_per_line, width_per_char, start_pixel_each_line):
            self.show_text(line, x, y, clear_first = False, show_now = False)

        if show_now:
            self.show()
            if hold_seconds > 0:
                time.sleep(hold_seconds)


    def show_datetime(self, year, month, day, hour, minute, second):
        datetime = [year, month, day, hour, minute, second]
        datetime_str = ["{0:0>2}".format(d) for d in datetime]

        self.show_text(text = '-'.join(datetime_str[:3]), x = 0, y = 0, clear_first = True, show_now = False)
        self.show_text(text = ':'.join(datetime_str[3:6]), x = 0, y = 10, clear_first = False, show_now = True)


    def show_time(self, year, month, day, hour, minute, second):
        self.show_datetime(year, month, day, hour, minute, second)
