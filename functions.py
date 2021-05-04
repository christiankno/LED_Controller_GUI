import requests
import statefile as cnf
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


def on_mousewheel(event):
    d=event.delta/120*(limit>>7)
    if event.widget.widgetName=='scale': event.widget.set(event.widget.get()+d)

def setRGB(rgb, brightness):
    rgbb=[int(i/limit*brightness) for i in rgb]
    send(rgbb)
    saveState(rgbb)

def setHSV(hsv):
    hsv=[hsv[0]/limit, hsv[1]/limit, hsv[2]]
    rgb=[int(i) for i in list(colorsys.hsv_to_rgb(*hsv))]
    send(rgb)
    saveState(rgb)
    
def pickColor():
    global state
    try:
        color = list(askcolor( tuple( [int(s*255/limit) for s in state] ), root)[0] )
        state = [int(s*limit/255) for s in color ]
        send(state)
        saveState(state)
    except Exception as e:
        print('No Color Picked')
        print(e)

def send(rgb):
    try:
        r=requests.post('http://192.168.0.109/data/', data={'R': rgb[0], 'G': rgb[1], 'B': rgb[2]})
        data=handleResponse(r)
    except Exception as e:
        print('problem posting information')
        print(e)
    print(rgb)
    return

def sendW(W):
    try:
        r=requests.post('http://192.168.0.109/data/', data={'W': W})
        data=handleResponse(r)
    except Exception as e:
        print('problem posting information')
        print(e)
    return

def sendMore(toggle=None, enable=None):
    _={}
    if toggle is not None: _['toggle']= toggle
    if enable is not None: _['enable']= enable
    try:
        r=requests.post('http://192.168.0.109/data/', data=_)
        data=handleResponse(r)
    except Exception as e:
        print('problem posting information')
        print(e)
    return

def getData():
    try:
        r=requests.post('http://192.168.0.109/data/')
        data=handleResponse(r)
    except Exception as e:
        print('problem posting information')
        print(e)
        data = cnf.state.append(0)
    return data


def saveState(rgb):
    with open('statefile.py', 'w') as f: f.write('state=['+str(rgb[0]) +","+str(rgb[1]) +","+str(rgb[2]) +"]")
    state=rgb

def handleResponse(r):
    data=[int(float(i)) for i in r.text[6:].split(', ')]
    print(data)
    return data