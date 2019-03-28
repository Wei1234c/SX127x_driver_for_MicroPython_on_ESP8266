# https://learn.adafruit.com/micropython-hardware-ssd1306-oled-display/software

import display
import ssd1306



class Display(ssd1306.SSD1306_SPI, display.Display):

    def __init__(self, spi, dc, res, cs, width = 128, height = 64):
        super().__init__(width, height, spi, dc, res, cs, external_vcc = False)
