import socket
import requests
import json
HOST= ''
PORT= 50008

ip_address=None
from ip_address import ip_address
if ip_address is None: ip_address="192.168.0.109"

try:
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST,PORT))
    sock.listen(1)
    print('listening')
    while 1:
        conn, addr =sock.accept()
        print(f'Connected by: {addr}')
        data = conn.recv(1024)
        decoded_data=json.loads(data.decode())
        print(f'received Data: {repr(decoded_data)}')

        r=requests.post(f'http://{ip_address}/data/', data=decoded_data)
        r=r.text

        #print(f'response: {r}')
        if not data: break
        conn.sendall(r.encode())
        conn.close()
        print('connection closed')

except Exception as e:
    with open('SocketLog', 'a+') as f:
        f.write('{e}\n')
    raise e
