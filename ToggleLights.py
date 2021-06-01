'''This script is supposed to work as a standalone file to change the value of the lights directly from the command line or by calling  command through another program.'''

import requests
import argparse
import time

def clearNone(dict):
    c={}
    for k,v in dict.items():
       if v is not None:
          c[k]=min(int(v),4095)
          c[k]=max(c[k],0)
    return c
t=0
test=0

mydict={}
if __name__ == '__main__':
    if t:tic=time.clock()
    if t:print('time0: {}'.format(time.clock()-tic))
    parser = argparse.ArgumentParser()
    parser.add_argument('-toggle', const=True, default=None, nargs='?')
    parser.add_argument('-w')
    parser.add_argument('-r')
    parser.add_argument('-g')
    parser.add_argument('-b')
    parser.add_argument('-diff', const=True, default=None, nargs='?')
    args = parser.parse_args()

    if t:print('time1: {}'.format(time.clock()-tic))
    #print(args.toggle)
    #print(args.w)
    #print(args.r)
    #print(args.g)
    #print(args.b)
    val={'w':0, 'r':0, 'g':0, 'b':0}

    ## Not needed after updating MCU code
    if args.diff and not test:
       r=requests.post('http://192.168.0.109/data/', data={})
       data=[int(float(i)) for i in r.text[6:].split(', ')]
       val['w']=data[0]
       val['r']=data[1]
       val['g']=data[2]
       val['b']=data[3]

    if not test:
        if t:print('time2: {}'.format(time.clock()-tic))
        myw = val['w']+float(args.w) if args.w is not None else args.w
        myr = val['r']+float(args.r) if args.r is not None else args.r
        myg = val['g']+float(args.g) if args.g is not None else args.g
        myb = val['b']+float(args.b) if args.b is not None else args.b
    ## Following is needed

    if t:print('time3: {}'.format(time.clock()-tic))
    mydict = {'toggle': args.toggle, 'W': myw, 'R': myr, 'G': myg, 'B': myb}
    ## if MCU has been updated to handle Diff argument:
    if test: mydict = {'toggle': args.toggle, 'W': args.w, 'R': args.r, 'G': args.g, 'B': args.b, 'Diff': args.Diff}
    else: mydict = {'toggle': args.toggle, 'W': myw, 'R': myr, 'G': myg, 'B': myb}
    mydict = clearNone(mydict)
    print(mydict)



    r=requests.post('http://192.168.0.109/data/', data=mydict)
    r=r.text
    print(r)

    if t: print('time4: {}'.format(time.clock()-tic))
