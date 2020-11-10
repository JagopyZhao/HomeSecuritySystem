# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 21:09:36 2020

@author: Administrator
"""

from Crypto.Cipher import AES
import base64
import random

class AesEncry(object):
    
    def __init__(self,key):
        self.key = key
        
    def encrypt(self, data):
        #data = json.dumps(data)
        pad_list = [b'\x30',b'\x31',b'\x32',b'\x33',b'\x34',b'\x35',b'\x36',b'\x37',b'\x38',b'\x39',b'\x3A',b'\x3B',b'\x3C',b'\x3D',b'\x3E',b'\x3F']
        #print("data: ",data)
        dataLen = len(data)
        padding = 16 - dataLen%16
        print("padding: ",padding)
        for i in range(padding-1):
            data = data + bytes([random.randint(0,127)])
        data = data + pad_list[padding]
        #print("data: ",data)
        mode = AES.MODE_ECB
        #padding = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        cryptos = AES.new(self.key, mode)
        #print("cryptos: ",cryptos)
        cipher_text = cryptos.encrypt(data)
        print("cipher_text: ",cipher_text)
        print("len_cipher_text: ",len(cipher_text))
        #cipher = base64.b64encode(cipher_text)#.decode("utf-8")
        #print("cipher: ",cipher)
        return cipher_text
 
    def decrypt(self, data):
        cryptos = AES.new(self.key, AES.MODE_ECB)
        #print("cryptos1: ",cryptos)
        #decrpytBytes = base64.b64decode(data)
        #print("decrpytBytes: ",decrpytBytes)
        plaintext = cryptos.decrypt(data)#.decode('utf-8')
        #print("plaintext: ",plaintext[-1])
        padLen = plaintext[-1]
        #print("padLen: ",padLen)
        padIndex = len(plaintext)-padLen
        #print("padIndex: ",padIndex)
        plaintext = plaintext[0:padIndex]
        print("plaintext: ",plaintext)
        #plaintext = meg[:-ord(meg[-1])]
        #print("plaintext: ",plaintext)
        return plaintext
    
'''
aesInit = AesEncry(b't3ksnBdN6iF5TpmL')

cipher = aesInit.encrypt(b"\x00\x03EDP\x01@\x00\x80\x00\x09559451901\x00\x1cGPbHpXhSCwlYyIxfdxoMpcAYJKY=")
aesInit.decrypt(cipher)
'''