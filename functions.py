import requests
import statefile as cnf
import tkinter as tk
import tkinter.ttk as ttk
import colorsys
from tkcolorpicker import askcolor
state=cnf.state
PCA9685=1

limit=4095 if PCA9685 else 1024


if state is None: state=(255,255,0)
state=list(state)
hsv=list(colorsys.rgb_to_hsv(*state))

root = tk.Tk()

def setR(R):
    state[0]=int(R)
    send(state)
    saveState(state)

def setG(G):
    state[1]=int(G)
    send(state)
    saveState(state)

def setB(B):
    state[2]=int(B)
    send(state)
    saveState(state)

def setH(H):
    global state
    hsv=list(colorsys.rgb_to_hsv(*state))
    hsv[0]=int(H)/1000
    state=list(colorsys.hsv_to_rgb(*hsv))
    send(state)
    saveState(state)

def setS(S):
    global state
    hsv=list(colorsys.rgb_to_hsv(*state))
    hsv[1]=int(S)/1000
    state=list(colorsys.hsv_to_rgb(*hsv))
    send(state)
    saveState(state)
    
def setV(V):
    global state
    hsv=list(colorsys.rgb_to_hsv(*state))
    hsv[2]=int(V)
    state=list(colorsys.hsv_to_rgb(*hsv))
    send(state)
    saveState(state)
    
def setBright(bright):
    global state
    bright=int(bright)
    s=[0,0,0]
    #for i in range(len(state)): 
    #    s[i]=int(state[i]*int(bright)/1024)
    s=[int(i*bright/limit) for i in state]
    send(s)

def pickColor():
    global state
    try:
        state = [int(s*limit/255) for s in list(askcolor( tuple( [int(s*255/limit) for s in state] ), root)[0]) ]
        send(state)
        saveState(state)
    except Exception as e:
        print('No Color Picked')
        print(e)


def send(rgb):
    try:
        requests.post('http://192.168.0.109/data/', data={'R': rgb[0], 'G': rgb[1], 'B': rgb[2]})
    except Exception as e:
        print('problem posting information')
        print(e)
    print(rgb)
    return

def saveState(rgb):
    with open('statefile.py', 'w') as f: f.write('state=['+str(rgb[0]) +","+str(rgb[1]) +","+str(rgb[2]) +"]")
    state=rgb