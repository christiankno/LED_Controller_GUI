# import system libraries
import time
import os
from functions import send, sendW, sendMore
if not os.path.isfile('./config.py'):
    with open('./config.py', 'w+') as f:
        f.write("ADAFRUIT_IO_KEY=''\nADAFRUIT_IO_USERNAME=''")
    print('pleade fill in the missing configuration data')

from config import *
from Adafruit_IO import Client, Feed, RequestError

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: 
    toggle = aio.feeds('led-toggle')
except RequestError:
    feed = Feed(name='led-toggle')
    toggle = aio.create_feed(feed)

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
