
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

if max(data[0:3])>0:
    r.set(data[0]*limit/max(data[0:3]))
    g.set(data[1]*limit/max(data[0:3]))
    b.set(data[2]*limit/max(data[0:3]))
    bright.set(max(data[0:3]))
else:
    r.set(data[0])
    g.set(data[1])
    b.set(data[2])
    bright.set(limit)
w.set(data[3])


w.configure(command=lambda i: sendMore( w=int(i) ))
r.configure(command=lambda i: sendMore(rgb=multBrightness( [int(i), int(g.get()), int(b.get()) ], int(bright.get()) )) )
g.configure(command=lambda i: sendMore(rgb=multBrightness( [int(r.get()), int(i), int(b.get()) ], int(bright.get()) )) )
b.configure(command=lambda i: sendMore(rgb=multBrightness( [int(r.get()), int(g.get()), int(i) ], int(bright.get()) )) )
bright.configure(command=lambda i: sendMore(rgb=multBrightness( [int(r.get()), int(g.get()), int(b.get()) ], int(i) )) )


#w.configure(command=lambda i: sendW( int(i) ))
#r.configure(command=lambda i: multBrightness( [int(i), int(g.get()), int(b.get()) ], int(bright.get()) ))
#g.configure(command=lambda i: multBrightness( [int(r.get()), int(i), int(b.get()) ], int(bright.get()) ))
#b.configure(command=lambda i: multBrightness( [int(r.get()), int(g.get()), int(i) ], int(bright.get()) ))
#bright.configure(command=lambda i: multBrightness( [int(r.get()), int(g.get()), int(b.get()) ], int(i) ))

w.pack()
r.pack()
g.pack()
b.pack()
bright.pack()
butt.pack()

root.bind_all("<MouseWheel>",on_mousewheel)

root.mainloop()  

