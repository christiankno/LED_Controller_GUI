import socket
import requests
import json
HOST= ''
PORT= 50008

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

        r=requests.post('http://192.168.0.109/data/', data=decoded_data)
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
