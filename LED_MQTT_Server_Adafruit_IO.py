
"""
`rgb_led.py`
=======================================================================
Control a RGB LED using
Adafruit IO and Python

Tutorial Link: https://learn.adafruit.com/adafruit-io-basics-color

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Author(s): Brent Rubell for Adafruit Industries
Copyright (c) 2018 Adafruit Industries
Licensed under the MIT license.
All text above must be included in any redistribution.

Dependencies:
    - Adafruit_Blinka
        (https://github.com/adafruit/Adafruit_Blinka)
    - Adafruit_CircuitPython_PCA9685
        (https://github.com/adafruit/Adafruit_CircuitPython_PCA9685)
"""
# import system libraries
import time
from functions import send, sendW, sendMore

from Adafruit_IO import Client, Feed, RequestError
from statefile import ADAFRUIT_IO_KEY, ADAFRUIT_IO_USERNAME

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'color' feed
    toggle = aio.feeds('led-toggle')
except RequestError: # create an `color` feed
    feed = Feed(name='led-toggle')
    toggle = aio.create_feed(feed)

## Create the I2C bus interface.
#i2c_bus = I2C(SCL, SDA)

## Create a simple PCA9685 class instance.
#pca = PCA9685(i2c_bus)
#pca.frequency = 60
#prev_color = '#000000'

#def map_range(x, in_min, in_max, out_min, out_max):
#    """re-maps a number from one range to another."""
#    mapped = (x-in_min) * (out_max - out_min) / (in_max-in_min) + out_min
#    if out_min <= out_max:
#        return max(min(mapped, out_max), out_min)
#    return min(max(mapped, out_max), out_min)

prev_toggle_val=None
while True:
    # grab the `color` feed
    toggle_val = aio.receive(toggle.key)
    if toggle_val != prev_toggle_val:
        print(toggle_val.value)
        if toggle_val.value=='ON': sendMore(enable=1)
        else: sendMore(enable=0)

        ## print rgb values and hex value
        #print('Received Color: ')
        #red = aio.to_red(color_val.value)
        #print('\t - R: ', red)
        #green = aio.to_green(color_val.value)
        #print('\t - G: ', green)
        #blue = aio.to_blue(color_val.value)
        #print('\t - B: ', blue)
        #print('\t - HEX: ', color_val.value)
        ## map color values (0-255) to  16-bit values for the pca
        #red = map_range(int(red), 0, 255, 0, 65535)
        #green = map_range(int(green), 0, 255, 0, 65535)
        #blue = map_range(int(blue), 0, 255, 0, 65535)
        ## invert RGB values for common anode LEDs.
        #pca.channels[RED_PIN].duty_cycle = 65535 - int(red)
        #pca.channels[GREEN_PIN].duty_cycle = 65535 - int(green)
        #pca.channels[BLUE_PIN].duty_cycle = 65535 - int(blue)
    prev_toggle_val = toggle_val
    # let's wait a bit so we don't flood adafruit io's servers...
    time.sleep(0.5)
