
import tkinter as tk
from functions import *


#style = ttk.Style(root)
#style.theme_use('clam')

h = tk.Scale(root, label='H', length=300, from_=0, to=limit, orient='horizontal')
s = tk.Scale(root, label='S', length=300, from_=0, to=limit, orient='horizontal')
v = tk.Scale(root, label='V', length=300, from_=0, to=limit, orient='horizontal')
butt = tk.Button(root, command=pickColor, text='Pick')

h.set(hsv[0]*limit)
s.set(hsv[1]*limit)
v.set(hsv[2])

h.configure(command=lambda i: setHSV( [int(i), int(s.get()), int(v.get()) ] ))
s.configure(command=lambda i: setHSV( [int(h.get()), int(i), int(v.get()) ] ))
v.configure(command=lambda i: setHSV( [int(h.get()), int(s.get()), int(i) ] ))

h.pack()
s.pack()
v.pack()
butt.pack()

root.bind_all("<MouseWheel>",on_mousewheel)

root.mainloop()  

