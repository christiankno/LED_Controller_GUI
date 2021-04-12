
import tkinter as tk
from functions import *


#style = ttk.Style(root)
#style.theme_use('clam')


h = tk.Scale(root, label='H', length=300, from_=0, to=1000, orient='horizontal', command=setH)
s = tk.Scale(root, label='S', length=300, from_=0, to=1000, orient='horizontal', command=setS)
v = tk.Scale(root, label='V', length=300, from_=0, to=1024, orient='horizontal', command=setV)
butt = tk.Button(root, command=pickColor, text='Pick')
h.set(hsv[0])
s.set(hsv[1])
v.set(hsv[2])
h.pack()
s.pack()
v.pack()
butt.pack()


root.mainloop()  

