# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 11:28:50 2020

@author: Administrator
"""

import socket

#实例化socket
server = socket.socket()

#绑定IP和端口号
server_address = ("localhost",40960)
server.bind(server_address)

#监听
server.listen()

#接收数据
con,addr = server.accept()
print("con: ",con)
print("addr: ",addr)
datas = con.recv(1024)
print('接收到的数据：',datas)

server.close()
