
import tkinter as tk
from functions import *


#style = ttk.Style(root)
#style.theme_use('clam')

def _on_mousewheel(event):
    d=event.delta/120*(limit>>7)
    if event.widget.widgetName=='scale': event.widget.set(event.widget.get()+d)

r = tk.Scale(root, label='R', length=300, from_=0, to=limit, orient='horizontal', command=setR)
g = tk.Scale(root, label='G', length=300, from_=0, to=limit, orient='horizontal', command=setG)
b = tk.Scale(root, label='B', length=300, from_=0, to=limit, orient='horizontal', command=setB)
bright = tk.Scale(root, label='Brightness', length=300, from_=0, to=limit, orient='horizontal', command=setBright)
butt = tk.Button(root, command=pickColor, text='Pick')
r.set(state[0])
g.set(state[1])
b.set(state[2])
bright.set(1024)
r.pack()
g.pack()
b.pack()
bright.pack()
butt.pack()
root.bind_all("<MouseWheel>",_on_mousewheel)

root.mainloop()  

