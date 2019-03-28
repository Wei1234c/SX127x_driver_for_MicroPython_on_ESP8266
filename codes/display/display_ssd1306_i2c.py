# https://learn.adafruit.com/micropython-hardware-ssd1306-oled-display/software

import display
import ssd1306



class Display(ssd1306.SSD1306_I2C, display.Display):

    def __init__(self, i2c, width = 128, height = 64):
        super().__init__(width, height, i2c, addr = 0x3c, external_vcc = False)
