import requests
import statefile as cnf
import time
import typing
from collections.abc import Sequence


try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkcolorpicker import askcolor
except Exception as e: print(e)
import colorsys
state=cnf.state
PCA9685=1

limit=4095 if PCA9685 else 1024


state= [255,255,0] if state is None else list(state)
hsv=list(colorsys.rgb_to_hsv(*state))

try:
    root = tk.Tk()
except Exception as e:
    print(e)


def on_mousewheel(event) -> None:
    '''If the widget over which the mousewheel was scrolled is a scale, its value will get moved by the wheel in the corresponding direction'''
    d=event.delta/120*(limit>>7)
    if event.widget.widgetName=='scale': event.widget.set(event.widget.get()+d)
    print(type(event))
    return

def multBrightness(rgb: list, brightness: int):
    '''This Function combines the Brightness values with the raw RGB values to adjust them accordingly, returning the adjusted RGB values.'''
    rgbb=[int(i/limit*brightness) for i in rgb]
    return rgbb

def hsv2rgb(hsv: list) -> list:
    '''Converts a list containing HSV values into and returns a list containing RGB values'''
    hsv=[hsv[0]/limit, hsv[1]/limit, hsv[2]]
    rgb=[int(i) for i in list(colorsys.hsv_to_rgb(*hsv))]
    return(rgb)
    
def pickColor() -> None:
    '''Opens up a tkinter window to pick a color from the palette. Upon closing the window it sends the value to the LED controller'''
    global state
    try:
        rgb=getData()[1:]
        color = list(askcolor( tuple( [int(s*255/limit) for s in rgb] ), root)[0] )
        rgb = [int(s*limit/255) for s in color ]
        sendMore(rgb=rgb)
        saveState(rgb)
    except Exception as e:
        print('No Color Picked')
        print(e)
    return

def sendMore(rgb: list = None, w: int = None, toggle: bool = None, enable: bool = None, wrgb: list = None) -> list:
    '''This function sends the color/white values aswell as the toggle or enable flag to the LED controller. 
    The values for the LEDs can be passed separately as RGB and W or combined as WRGB.
    The set values are then received as a response and are then returned by the function'''
    data={}
    if wrgb is not None:
        w=wrgb[0]
        rgb=wrgb[1:]

    if rgb is not None: 
        data['R']=rgb[0]
        data['G']=rgb[1]
        data['B']=rgb[2]
    if w is not None: data['W']=w

    if enable is not None: data['enable']= enable
    elif toggle is not None: data['toggle']= toggle

    try:
        r=requests.post('http://192.168.0.109/data/', data=data)
        data=handleResponse(r)
    except Exception as e:
        print('problem posting information')
        print(e)
    return data

def getData() -> list:
    '''This function retrieves the data from the LED controller by sending an empty request.
    The response contains the current values of the LEDs which is returned as a list'''
    try:
        r=requests.post('http://192.168.0.109/data/')
        data=handleResponse(r)
    except Exception as e:
        print('problem posting information')
        print(e)
        data = cnf.state.append(0)
    return data


def saveState(rgb: list) -> None:
    '''This saves the current LED state to a local file. 
    Its use is getting deprecated since the LED state can be received as a response from the LED controller at any moment.'''
    with open('statefile.py', 'w') as f: f.write('state=['+str(rgb[0]) +","+str(rgb[1]) +","+str(rgb[2]) +"]")
    state=rgb
    return

def handleResponse(r) -> list:
    '''This parses the text response from the LED controller server to form a list containing the LED values. 
    Carefull. This function and the server response need to match in order to handle the text succesfully'''
    data=[int(float(i)) for i in r.text[6:].split(', ')]
    print(data)
    return data



def fadeTo(next: list, t: int = 1) -> None:
    '''This function fades the LED lights to the colors passed as the argument.
    The keyworded argument 't' defines the ime in seconds it should take to fade to the next color with a default value of 1.'''
    steps=t*50
    prev=getData()

    diff=[next[i]-prev[i] for i in range(len(next))]

    for i in range(steps+1):
        wrgb=[int(prev[j]+diff[j]/steps*i) for j in range(len(prev))]
        sendMore(wrgb=wrgb)
        time.sleep(0.02)
    return