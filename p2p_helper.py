#!/usr/bin/env python3

import socket, threading, sys, time

# class Client(threading.Thread):    
#     def connect(self,host,port):
#         self.sock.connect((host,port))
#     def client(self,host,port,msg):               
#         sent=self.sock.send(msg)           
#         print "Sent\n"
#     def run(self):
#         self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#         try:
#             host=raw_input("Enter the hostname\n>>")            
#             port=int(raw_input("Enter the port\n>>"))
#         except EOFError:
#             print "Error"
#             return 1
        
#         print "Connecting\n"
#         s=''
#         self.connect(host,port)
#         print "Connected\n"
#         while 1:            
#             print "Waiting for message\n"
#             msg=raw_input('>>')
#             if msg=='exit':
#                 break
#             if msg=='':
#                 continue
#             print "Sending\n"
#             self.client(host,port,msg)
#         return(1)

s = socket.socket()
s.bind(('127.0.0.1', 7000))
s.listen(5)
client_sockets = []
users = []
print("Listening")

def handle_client(conn):
    while True:
        try:
            data = conn.recv(512)
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
    print("Activity")
    threading.Thread(target = handle_client,args = (conn,)).start()

