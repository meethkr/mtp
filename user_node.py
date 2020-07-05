#!/usr/bin/env python3

import socket, threading, _thread



# def send_block(s):
#     while True:
#         inp = input("Message: ")  
#         s.send(inp.encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 9500))
    def recieve_block(s):
        while True:
            data = s.recv(1024).decode()  
            print('Received: ' + data) 

    while True:
        threading.Thread(target=recieve_block,args=(s,)).start()
        msg = input("Enter your message : ")
        s.send(msg.encode())
        
    s.close()
