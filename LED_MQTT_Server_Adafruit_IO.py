# import system libraries
import time
import os
from Adafruit_IO import Client, Feed, RequestError
from functions import sendMore

source=os.path.dirname(os.path.abspath(__file__))

if not os.path.isfile(os.path.join(source,'config.py')):
    with open(os.path.join(source,'config.py'), 'w+') as f:
        f.write("ADAFRUIT_IO_KEY=''\nADAFRUIT_IO_USERNAME=''")
    print('pleade fill in the missing configuration data')

from config import *

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: 
    colorname = aio.feeds('rgb-lights.colorname')
    aio.feeds()
except RequestError as e:
    print(e)
    feed = Feed(name='rgb-lights.colorname')
    colorname = aio.create_feed(feed)

color_dict={
    'fire': '0,4095,680,0',
    'orange': '0,4095,680,0',
    'blue': '4095,0,0,4095',
    'white': '4095,0,0,0',
    'max':'4095,4095,4095,4095',
    'red':'1000,4095,0,0',
    'green':'2000,0,4095,0',
    'purple':'0,4095,0,620',
    'off':'off',
    'on':'on',
    }

while True:
    try:
        colorname_data = aio.receive(colorname.key)
        data={}

        if colorname_data.value != '0':
            color=colorname_data.value.lower()
            if color in color_dict.keys():
                print('Turning {}'.format(color))
                color_values=color_dict[color]
            else: print('color not recognized')
            
            if color_values=='on': data['enable']=1
            elif color_values=='off': data['enable']=0
            else: data['wrgb']=[int(i) for i in color_values.split(',')]

            try:
                aio.send(colorname.key, '0')
            except Exception as e:
                print('error sending colorname value')
                print(e)

            sendMore(**data)

        time.sleep(0.5)

    except Exception as e:
        print(e)


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
