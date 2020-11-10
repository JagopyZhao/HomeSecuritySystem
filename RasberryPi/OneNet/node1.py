# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 11:35:30 2020

@author: Administrator
"""
import socket

client = socket.socket()

client_address = ("localhost",40960)
client.connect(client_address)

client.send("hello world!".encode())

client.close()