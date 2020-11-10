# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 20:46:20 2020

@author: Administrator
"""

import rsa
 
 
# rsa加密
def rsaEncrypt(str):
    # 生成公钥、私钥
    (pubkey, privkey) = rsa.newkeys(1024)
    print("公钥:\n%s\n私钥:\n:%s" % (pubkey, privkey))
    print(type(privkey))
    # 明文编码格式
    content = str.encode("utf-8")
    # 公钥加密
    crypto = rsa.encrypt(content, pubkey)
    return (crypto, privkey)
 
 
# rsa解密
def rsaDecrypt(str, pk):
    # 私钥解密
    content = rsa.decrypt(str, pk)
    print("content: ",content)
    con = content.decode("utf-8")
    return con
 
 
if __name__ == "__main__":
 
    _, pk = rsaEncrypt("hello")
    strB = b'\x9b.\x94\xb9\x0bq\xc8f\xa1\xb9\xbc]\x90\xd5\xa26\xb3\xaeJo\x9bM6\xf6\x00\xef\xfcV\xd1\xa0E\xcc\x12!\tO\xd6\xa6X.(S\x05\x85e\xe3lH\xe7e\x1f\xfc\xa2Y\xb2\x13i\xe3\x86\xbd\xdf\x16V\xfbw\xf3n\xe5\xd9_\xf2\x83\xb2\x8e\x9btDA\xa2e\x85\x9a\x1c\x94i\xf0\xa0\xcd\xd8\x01\xf1\xe2|\xe9\x87\x13\xcbI\x85\xde\x16\xee\x9f\x80/\t\x80\x87\x9a;\x85d\xcb\xff\xa6K\x8b]\x9e\x9c\xd7w\x950\x8a\x0c\xa8I'
    print("加密后密文：",len(strB))
    content = rsaDecrypt(strB, pk)
    print("解密后明文：\n%s" % content)