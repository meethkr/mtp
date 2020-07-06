#!/usr/bin/env python3

import socket
import threading
import _thread
import random
import string
import hashlib
import pickle
import time
import queue
import cryptography
from cryptography.fernet import Fernet

# def send_block(s):
#     while True:
#         inp = input("Message: ")  
#         s.send(inp.encode())
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', 9500))
    currIndex = 0
    currChain = []
    sq = queue.Queue()
    rq = queue.Queue()
    def recieve_block(s, rq):
        global currIndex
        while True:
            en_b = s.recv(4096)            
            print('Received block:', en_b) 
            # en_b = s.recv(4096)
            # while True:
            #     packet = s.recv(4096)
            #     if not packet: 
            #         break
            #     en_b += packet

            h, key = rq.get()
            f = Fernet(key)

            print("Computed hash of block", hashlib.sha224(en_b).hexdigest())
            print("Recieved hash of block", h)

            if h != hashlib.sha224(en_b).hexdigest() :
                print("Mismatch!")
            else:
                db = f.decrypt(en_b)
                lb = pickle.loads(db)
                currIndex += 1
                currChain.append(lb)
                print("Block Added to Chain")

            print("Enter g to generate a random block, s to show the chain: ")


    def peer_to_peer_send(ps, sq):
        while True:
            h, key = sq.get()
            pd = pickle.dumps((h, key))
            ps.send(pd)

    def peer_to_peer_recv(ps, rq):
        while True:
            pr = ps.recv(4096)
            # pr = b""
            # while True:
            #     packet = ps.recv(4096)
            #     if not packet: break
            #     pr += packet
            
            h, key = pickle.loads(pr)
            rq.put((h, key))

    def randomData(len):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(len))
        
    ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ps.connect(('127.0.0.1', 7000))

    threading.Thread(target=recieve_block,args=(s,rq)).start()
    threading.Thread(target=peer_to_peer_recv,args=(ps, rq)).start()
    threading.Thread(target=peer_to_peer_send,args=(ps, sq)).start()

    print("Enter g to generate a random block, s to show the chain: ")
    while True:
        time.sleep(1)
        msg = input()

        if msg == "g" :
            print("Generating a block")
            random.seed()
            block_index = currIndex
            block_id = random.randrange(9999)
            block_data = randomData(20)
            time.sleep(1)

            print("Generated block")
            print("Index:", currIndex)
            print("ID:", block_id)
            print("Data:", block_data, "\n")
            time.sleep(1)

            print("Encrypting the block")
            block = (block_index, block_id, block_data)
            key = Fernet.generate_key()
            f = Fernet(key)

            p = pickle.dumps(block)
            encrypted_block = f.encrypt(p)
            print("Encrypted block:", encrypted_block)

            h = hashlib.sha224(encrypted_block).hexdigest()
            print("The hash of the encrypted block is", h)
            s.send(encrypted_block)
            sq.put((h, key))
            time.sleep(1)
            print("")
            print("Sent block to CDN")
            print("Pushed hash to P2P Network")



        elif msg == "s" :
            for i in currChain:
                print(i)
        
    s.close()
