'''This script is supposed to work as a standalone file to change the value of the lights directly from the command line or by calling  command through another program.'''
t=1
#from socket import socket
if t: import time
if t:tic=time.time()
if t:print(f'time_Start: {time.time()-tic}')

#import requests
import socket
import json

if t:print(f'time_Requests: {time.time()-tic}')
import argparse
if t:print(f'time_Argsparse: {time.time()-tic}')
#import functions

def clearNone(dict):
    c={}
    for k,v in dict.items():
       if v is not None:
          #c[k]=min(int(v),4095)
          #c[k]=max(c[k],0)
          c[k]=int(v)
    return c
diff_en=1

mydict={}
if __name__ == '__main__':
    if t:print(f'time0: {time.time()-tic}')
    parser = argparse.ArgumentParser()
    parser.add_argument('-toggle', const=True, default=None, nargs='?')
    parser.add_argument('-w')
    parser.add_argument('-r')
    parser.add_argument('-g')
    parser.add_argument('-b')
    parser.add_argument('-diff', const=True, default=None, nargs='?')
    parser.add_argument('-fade', const=True, default=None, nargs='?')
    args = parser.parse_args()

    if t:print(f'time1: {time.time()-tic}')
    #print(args.toggle)
    #print(args.w)
    #print(args.r)
    #print(args.g)
    #print(args.b)
    val={'w':0, 'r':0, 'g':0, 'b':0}

    ## Not needed after updating MCU code
    if args.diff and not diff_en:
       r=requests.post('http://192.168.0.109/data/', data={})
       data=[int(float(i)) for i in r.text[6:].split(', ')]
       val['w']=data[0]
       val['r']=data[1]
       val['g']=data[2]
       val['b']=data[3]

    if not diff_en:
        if t:print(f'time2: {time.time()-tic}')
        myw = val['w']+float(args.w) if args.w is not None else args.w
        myr = val['r']+float(args.r) if args.r is not None else args.r
        myg = val['g']+float(args.g) if args.g is not None else args.g
        myb = val['b']+float(args.b) if args.b is not None else args.b
    ## Following is needed

    if t:print('time3: {}'.format(time.time()-tic))
    #mydict = {'toggle': args.toggle, 'W': myw, 'R': myr, 'G': myg, 'B': myb}
    ## if MCU has been updated to handle Diff argument:
    if diff_en: mydict = {'toggle': args.toggle, 'W': args.w, 'R': args.r, 'G': args.g, 'B': args.b, 'Diff': args.diff}
    else: mydict = {'toggle': args.toggle, 'W': myw, 'R': myr, 'G': myg, 'B': myb}
    mydict = clearNone(mydict) # Removes any undefined variables
    print(f'sending: {mydict}')


    if args.fade: pass # to be implemented in the future
    #r=requests.post('http://192.168.0.109/data/', data=mydict)
    #r=r.text
    #print(f'response: {r}')

    HOST= ''
    PORT= 50008
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    encoded_data = json.dumps(mydict, indent=2).encode('utf-8')
    sock.sendall(encoded_data)
    rdata = sock.recv(1024)
    sock.close()
    print(f'received: {repr(rdata.decode())}')


    if t:print(f'time4: {time.time()-tic}')




