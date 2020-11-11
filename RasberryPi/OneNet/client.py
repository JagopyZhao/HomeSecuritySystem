#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import struct

from aesTest import AesEncry

CONN_SUCCESS = 0x00
CONN_REQ = 0x10
CONN_RESP = 0x20
PUSH_DATA = 0x30
CONN_CLOSE = 0x40
SAVE_DATA = 0x80
SAVE_ACK = 0x90
CMD_REQ = 0xA0
CMD_RESP = 0xB0
PING_REQ = 0xC0
PING_RESP = 0xD0
ENCRYPT_REQ = 0xE0
ENCRYPT_RESP = 0xF0

EDP1 = 1
PROTOCOL_NAME1 = b'EDP'

import rsa

# rsa解密
def rsaDecrypt(str, pk):
    # 私钥解密
    content = rsa.decrypt(str, pk)
    con = content.decode("utf-8")
    print("type(con): ",type(con))
    return con

class mysocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg, msg_len):
        totallen = 0
        while totallen < msg_len:
            sent = self.sock.send(msg[totallen:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totallen = totallen + sent

    def myreceive(self):
        chunks = []
        chunk = self.sock.recv(1024)
        if chunk == '':
            raise RuntimeError("socket connection broken")
        print("chunk: ",chunk)
        print("Len(chunk): ",len(chunk))
        chunks.append(chunk)
        #print("type(chunks): ",type(chunks))
        #print("chunks: ",chunks)
        return chunks

class Client:
    def __init__(self, sock, username, password, encrypt ,protocol=EDP1, keepalive=128):
        if username == "" or username is None:
            raise ValueError('username must not be empty')
        if password == "" or password is None:
            raise ValueError('password must not be empty')
        self._username = username
        self._password = password
        self._keepalive = keepalive
        self._protocol = protocol
        self._sock = sock
        self._from_packet = None
        self._to_packet = None

        self._cmdid = None
        self._cmdlen = None
        self._cmdmsglen = None
        self._cmdmsg = None
        
        
        self.key = None
        self.encrypt = encrypt

    def _pack_remaining_length(self, packet, remaining_length):
        remaining_bytes = []
        while True:
            byte = remaining_length % 128 #取余 16
            #print('byte1: ',byte)
            #print('remaining_length: ',remaining_length)
            remaining_length = int(remaining_length / 128) #除以   
            #print('remaining_length1: ',remaining_length)
            if remaining_length > 0:
                #print('type(byte): ',type(byte))
                byte = byte | 128
                #print('byte2: ',byte)

            remaining_bytes.append(byte)
            packet.extend(struct.pack("!B", byte))
            if remaining_length == 0:
                return packet

    def _unpack_remaining_length(self, packet):
        multiplier = 1
        value = 0
        len = 0
        i = 1

        while True:
            byte = struct.unpack('!B', bytes([packet[i]]))
            i+=1
            value += (byte[0] & 127) * multiplier
            multiplier *= 128
            len += 1

            if len > 4:
                return (-1)

            if byte[0] & 128 == 0:
                break
        return len

    def _pack_str16(self, packet, data):
        if isinstance(data, bytes):
            packet.extend(struct.pack("!H", len(data)))
            packet.extend(data)
        elif isinstance(data, str):
            udata = data.encode('utf-8')
            packet_format = "!H" + str(len(udata)) + "s"
            packet.extend(struct.pack(packet_format, len(udata), udata))
        elif isinstance(data, str):
            udata = data.encode('utf-8')
            packet_format = "!H" + str(len(udata)) + "s"
            packet.extend(struct.pack(packet_format, len(udata), udata))
        else:
            raise TypeError

    def _pack_str32(self, packet, data):
        if isinstance(data, bytes):
            packet.extend(struct.pack("!I", len(data)))
            packet.extend(data)
        elif isinstance(data, str):
            udata = data.encode('utf-8')
            packet_format = "!I" + str(len(udata)) + "s"
            packet.extend(struct.pack(packet_format, len(udata), udata))
        elif isinstance(data, str):
            udata = data.encode('utf-8')
            packet_format = "!I" + str(len(udata)) + "s"
            packet.extend(struct.pack(packet_format, len(udata), udata))
        else:
            raise TypeError


    def _read(self):
        packet = self._sock.myreceive()
        print("packet_myreceive: ",packet)
        self._from_packet = packet[0]
        print("len_packet_myreceive: ",len(self._from_packet))
        #Packet_form = struct.unpack('!BBBB',self._from_packet)
        #print("type(self._from_packet): ",type(self._from_packet))
        #print("self._from_packet: ",self._from_packet)


        
    
    def _build_encrypt_req(self,e,n):
        command = ENCRYPT_REQ
        packet = bytearray()
        packet.extend(struct.pack("!B", command))
        #print("packet1: ",packet)

        remaining_length = 1+2+4+128+1 #136
        #self._pack_remaining_length(packet, remaining_length)
        packet.extend(b'\x85\x01')
        packet.extend(struct.pack("!I", e))
        #print("packet2: ",packet)
        packet.extend(struct.pack("!128s", n.to_bytes(128, 'big')))
        #print("packet3: ",packet)
        packet.extend(struct.pack("!B", 1))
        #print("packet4: ",packet.hex())
        
        #bytes_str = b'\xE0\x85\x01\x00\x01\x00\x01\xA7\x14\xC8\xE9\xB9\x0F\xBE\x47\x1C\xE9\xF4\xD4\x3E\x56\x25\xD3\x43\x6F\x66\x20\xE2\x8C\x3C\x52\x00\xD8\x69\x54\xF5\x3E\xE6\x82\xA8\x65\x1D\xD6\x24\x37\xAE\x60\xC5\x14\xBF\xCF\x21\xDA\xF5\x40\x73\xEB\x28\x7B\x7C\x55\x57\x1E\xA2\x97\xE3\x6E\x93\xF8\xD3\x5B\x3C\x7B\x16\x2F\xF6\xD5\x2A\x1C\x82\xB5\xE2\x5B\xA9\xAD\x92\x96\xE2\x2A\xA0\x6F\x9D\x35\xF9\xFD\xB8\x89\xAC\xC0\x04\x23\x06\x94\x8D\x5F\xF8\x54\xD9\x5D\xB1\x53\xEE\x2F\x22\xB0\x51\xAB\x6B\x0D\xCD\x8E\xD4\x85\x32\x1C\xBB\x78\xFB\x43\x08\xF0\xE5\x0D\x03\xCD\x01'
        self._to_packet = packet
        #print("bytes_str: ",bytes_str)
        #print("len(bytes_str): ",len(bytes_str))
    

    def _build_push_data(self, dst_device_id, data):#=None
        command = PUSH_DATA
        packet = bytearray()
        packet.extend(struct.pack("!B", command))

        if dst_device_id is None or dst_device_id == '':
            remaining_length = 2+len(data)
            self._pack_remaining_length(packet, remaining_length)
            packet.extend(struct.pack("!H", 0))
        else:
            remaining_length = 2+len(dst_device_id)+len(data)
            self._pack_remaining_length(packet, remaining_length)
            packet.extend(struct.pack("!H"+str(len(dst_device_id))+"s", len(dst_device_id), dst_device_id))
        self._pack_str16(packet, data)
        self._to_packet = packet
        
    def _build_connect(self):
        if self._protocol == EDP1:
            protocol = PROTOCOL_NAME1
            proto_ver = 1
        keepalive = self._keepalive
        remaining_length = 2+len(protocol)+1+1+2\
                    +2+len(self._username) +2+len(self._password)
        connect_flags = 0
        connect_flags = connect_flags | 64
        
        packet = bytearray()

        if(self.encrypt==0):
            command = CONN_REQ #0x10
            packet.extend(struct.pack("!B", command))
            #print("remaining_length: ",remaining_length)
            #self._pack_remaining_length(packet, remaining_length)
            packet.extend(bytes([remaining_length]))
        packet.extend(struct.pack("!H"+str(len(protocol))+"sBBH", \
                    len(protocol), protocol, proto_ver, connect_flags, keepalive))

        self._pack_str16(packet, self._username)
        self._pack_str16(packet, self._password)
        print("packet: ",packet)
        
        if(self.encrypt==1):
            aesInit = AesEncry(self.key)#self.key
            cipher = aesInit.encrypt(bytes(packet))
            command = CONN_REQ #0x10
            packet_cipher = bytearray()
            packet_cipher.extend(struct.pack("!B", command))
            cipher_len = len(cipher)
            print("cipher_len: ",cipher_len)
            packet_cipher.extend(bytes([cipher_len]))
            packet_cipher.extend(cipher)
            self._to_packet = packet_cipher
            print("packet_cipher: ",packet_cipher)
        else:
            self._to_packet = packet
            print("packet: ",packet)

    def _build_save_data(self, dst_device_id, data, data_type):
        
        packet = bytearray()
        if(self.encrypt==0):
            command = SAVE_DATA
            packet.extend(struct.pack("!B", command))

        if dst_device_id is None or dst_device_id == '':
            if(self.encrypt==0):
                remaining_length = 1+1+2+len(data)
                print("remaining_length: ",remaining_length)
                #remaining_length = flag+datatype+2+data_len
                self._pack_remaining_length(packet, remaining_length)
            packet.extend(struct.pack("!B", 0))
        else:
            if(self.encrypt==0):
                remaining_length = 1+2+len(dst_device_id)+1+2+len(data)
                print("remaining_length: ",remaining_length)
                self._pack_remaining_length(packet, remaining_length)
            packet.extend(struct.pack("!BH"+str(len(dst_device_id))+"s", 128, len(dst_device_id), dst_device_id))

        packet.extend(struct.pack("!B", data_type))
        if data_type == 2:
            self._pack_str32(packet, data)
        else:
            self._pack_str16(packet, data)
        print("save_packet: ",packet)
        
        if(self.encrypt==1):
            aesInit = AesEncry(self.key)#self.key
            cipher = aesInit.encrypt(bytes(packet))
            command = SAVE_DATA
            packet_cipher = bytearray()
            packet_cipher.extend(struct.pack("!B", command))
            cipher_len = len(cipher)
            #print("cipher_len: ",cipher_len)
            self._pack_remaining_length(packet_cipher, cipher_len)
            #packet_cipher.extend(bytes([cipher_len]))
            packet_cipher.extend(cipher)
            self._to_packet = packet_cipher
            print("save_data_cipher: ",packet_cipher)
        
        else:
            self._to_packet = packet
            print("packet: ",packet)
        
        

    def _build_cmd_resp(self, cmdid, resp_body):
        command = CMD_RESP
        packet = bytearray()
        packet.extend(struct.pack("!B", command))
        remaining_length = 2+len(cmdid)+4+len(resp_body)
        self._pack_remaining_length(packet, remaining_length)

        self._pack_str16(packet, cmdid)
        self._pack_str32(packet, resp_body)
        self._to_packet = packet

    def _build_ping_req(self):
        command = PING_REQ
        packet = bytearray()
        packet.extend(struct.pack("!BB", command, 0))
        self._to_packet = packet

    def handle_cmd_req(self):
        receive_comm = self._from_packet
        aesInit = AesEncry(self.key) #self.key
        comm = aesInit.decrypt(receive_comm[2:])
        len_comm = len(comm)
        print("receive_comm: ",comm)
        print("comm: ",comm[len_comm-5:])
        return comm[len_comm-5:]
    
    def handle_encrypt_resp(self,privkey):
        #print('self._from_packet[0]: ',type(bytes([self._from_packet[0]])))
        key_bytes = self._from_packet[5:]
        ddata = rsaDecrypt(key_bytes,privkey)
        print("len(ddata): ",len(ddata))
        print("ddata: ",ddata)
        self.key = str.encode(ddata)
        #print('return key bytes : ',key_bytes)
        #(_result,) = struct.unpack('!B',bytes([self._from_packet[0]]))
        #return key_bytes

    def handle_save_ack(self):
        (have_json,) = struct.unpack('!B', self._from_packet[2])
        if have_json & 128 == 0:
            (rtype, remaining_length, desc_flag) = struct.unpack('!BBB', self._from_packet)
            return(0, 0)
        elif have_json & 128 == 128:
            (len,) = struct.unpack('!H', str(self._from_packet[3])+str(self._from_packet[4]))
            (rtype, remaining_length, desc_flag, desc_len, desc) = struct.unpack('!BBBH'+str(len)+'s',
                    self._from_packet)
            return (desc_len, desc)

    def handle_ping_resp(self):
        (rtype, remaining_length) = struct.unpack('!BB', self._from_packet)
        
    def handle_conn_resp(self):
        receive_pak = self._from_packet
        print("handle_conn_resp: ",receive_pak)
        aesInit = AesEncry(self.key) #self.key
        conn_resp_code = aesInit.decrypt(receive_pak[2:]+receive_pak[2:])

        print("conn_resp_code: ",int.from_bytes(conn_resp_code, 'big', signed=True))
        
    def handle_save_data(self):
        receive_save_data = self._from_packet
        aesInit = AesEncry(self.key) #self.key
        save_data = aesInit.decrypt(receive_save_data[2:])
        print("receive_save_data: ",save_data)
        print("save_data: ",save_data[15:])
        return save_data[15:]

    def conn_req(self):
        self._build_connect()
        self._sock.mysend(self._to_packet, len(self._to_packet))

    def push_data(self, dst_device_id, data):
        self._build_push_data(dst_device_id, data)
        self._sock.mysend(self._to_packet, len(self._to_packet))

    def save_data(self, data, data_type, dst_device_id):
        self._build_save_data(dst_device_id, data, data_type)
        self._sock.mysend(self._to_packet, len(self._to_packet))

    def cmd_resp(self, cmdid, resp_body="ok"):
        self._build_cmd_resp(cmdid, resp_body)
        self._sock.mysend(self._to_packet, len(self._to_packet))

    def conn_close(self):
        pass

    def ping_req(self):
        self._build_ping_req()
        self._sock.mysend(self._to_packet, len(self._to_packet))

    def edp_packet_type(self):
        #print('self._from_packet[0]: ',type(bytes([self._from_packet[0]])))
        print('self._from_packet[0]: ',bytes([self._from_packet[0]]))
        (_result,) = struct.unpack('!B',bytes([self._from_packet[0]]))
        return _result

    def read_packet(self):
        self._read()

    def is_conn_resp(self):
        self._read()
        _result = struct.unpack('!BBBB', self._from_packet)
        if _result[0] == CONN_RESP and _result[3] == CONN_SUCCESS:
            return True
        else:
            return False

    def clear_packet(self):
        self._from_packet = None
        self._to_packet = None
        
    def encrypt_req(self,e,n):
        self._build_encrypt_req(e,n)
        self._sock.mysend(self._to_packet, len(self._to_packet))
