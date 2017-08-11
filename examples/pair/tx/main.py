# coding: utf-8
import gc
gc.collect()

import sx127x
gc.collect()

import test
gc.collect()



# Signal boot successfully ___________
import led
led.blink_on_board_led(times = 2)


# Main ___________
# import test
test.main()