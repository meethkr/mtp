#!/usr/bin/env python3

import socket, threading, sys, time

s = socket.socket()
s.bind(('127.0.0.1', 9500))
s.listen(5)
client_sockets = []
users = []
print("Listening")

def handle_client(conn):
    while True:
        try:
            data = conn.recv(4096)
            pro = input("Block recieved. Tamper? (Press y to tamper): ")
            
            if pro == "y":
                data = b"hello"
    
            for x in client_sockets:
                try:
                    x.send(data)
                except Exception as e:
                    print(e)
        except:
            pass

while True:
    conn,addr = s.accept()
    client_sockets.append(conn)
    print("Connections from", addr[0], "on port",addr[1])
    threading.Thread(target = handle_client,args = (conn,)).start()