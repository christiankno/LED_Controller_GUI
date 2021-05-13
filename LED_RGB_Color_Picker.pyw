
import tkinter as tk
from functions import *


#style = ttk.Style(root)
#style.theme_use('clam')

w = tk.Scale(root, label='W', length=300, from_=0, to=limit, orient='horizontal')
r = tk.Scale(root, label='R', length=300, from_=0, to=limit, orient='horizontal')
g = tk.Scale(root, label='G', length=300, from_=0, to=limit, orient='horizontal')
b = tk.Scale(root, label='B', length=300, from_=0, to=limit, orient='horizontal')
bright = tk.Scale(root, label='Brightness', length=300, from_=0, to=limit, orient='horizontal')
butt = tk.Button(root, command=pickColor, text='Pick')

data=getData()

w.set(data[0])

if max(data[1:])>0:
    r.set(data[1]*limit/max(data[1:]))
    g.set(data[2]*limit/max(data[1:]))
    b.set(data[3]*limit/max(data[1:]))
    bright.set(max(data[1:]))
else:
    r.set(data[1])
    g.set(data[2])
    b.set(data[3])
    bright.set(limit)


w.configure(command=lambda i: sendMore( w=int(i) ))
r.configure(command=lambda i: sendMore(rgb=multBrightness( [int(i), int(g.get()), int(b.get()) ], int(bright.get()) )) )
g.configure(command=lambda i: sendMore(rgb=multBrightness( [int(r.get()), int(i), int(b.get()) ], int(bright.get()) )) )
b.configure(command=lambda i: sendMore(rgb=multBrightness( [int(r.get()), int(g.get()), int(i) ], int(bright.get()) )) )
bright.configure(command=lambda i: sendMore(rgb=multBrightness( [int(r.get()), int(g.get()), int(b.get()) ], int(i) )) )

w.pack()
r.pack()
g.pack()
b.pack()
bright.pack()
butt.pack()

root.bind_all("<MouseWheel>",on_mousewheel)

root.mainloop()  

