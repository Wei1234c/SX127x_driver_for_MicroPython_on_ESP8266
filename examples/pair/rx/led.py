# coding: utf-8

import time
import machine
from config import hardware


on_board_led = machine.Pin(hardware.ON_BOARD_LED_PIN_NO, machine.Pin.OUT)
on_board_led.value(0 if hardware.ON_BOARD_LED_HIGH_IS_ON else 1)  # LED off


def blink_on_board_led(times = 1, forever = False, on_seconds = 0.5, off_seconds = 0.5):
    blink(on_board_led, times, forever, on_seconds, off_seconds, hardware.ON_BOARD_LED_HIGH_IS_ON)
            

def blink(pin, times = 1, forever = False, on_seconds = 0.5, off_seconds = 0.5, high_is_on = False):
    
    on, off = (1, 0) if high_is_on else (0, 1)
    
    if forever:
        while True:
            blink_once(pin, on_seconds, off_seconds, on, off)
            
    if times > 0:
        for i in range(times):
            blink_once(pin, on_seconds, off_seconds, on, off)
            
            
def blink_once(pin, on_seconds = 0.5, off_seconds = 0.5, on = 1, off = 0):
    pin.value(on)
    time.sleep(on_seconds)
    pin.value(off)
    time.sleep(off_seconds)     