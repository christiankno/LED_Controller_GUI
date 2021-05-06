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
    state = aio.feeds('rgb-lights.state')
    aio.feeds()
except RequestError:
    feed = Feed(name='led-toggle')
    toggle = aio.create_feed(feed)
    feed = Feed(name='rgb-lights.state')
    state = aio.create_feed(feed)

toggle_data=None
prev_toggle_data=None
state_data=None
prev_state_data=aio.receive(state.key)
while True:
    try:
        toggle_data = aio.receive(toggle.key)
        state_data = aio.receive(state.key)
    except Excception as e:
        print(e)

    if toggle_data != prev_toggle_data:
        print(toggle_data.value)
        if toggle_data.value=='ON': sendMore(enable=1)
        else: sendMore(enable=0)

    if state_data != prev_state_data and state_data.value != '0':
        print(state_data.value)
        wrgb=[int(i) for i in state_data.value.split(',')]
        send(wrgb[1:])
        sendW(wrgb[0])
        try:
            aio.send(state.key, '0')
        except Exception as e:
            print(e)

    prev_state_data = state_data
    prev_toggle_data = toggle_data
    time.sleep(0.5)


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
