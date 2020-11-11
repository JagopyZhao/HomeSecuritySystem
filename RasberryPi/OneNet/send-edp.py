#!/usr/bin/env python
# -*- coding:utf-8 -*-

from client import *
import time
import struct
import json
import threading
import select
import sqlite3
import rsa
import Adafruit_DHT
import RPi.GPIO as GPIO  

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM) 
GPIO.setup(24, GPIO.OUT)   #relay
GPIO.setup(19, GPIO.OUT)   #motor

GPIO.setup(17, GPIO.IN) #gas
GPIO.setup(4, GPIO.IN) #motion
GPIO.setup(27, GPIO.IN) #fire
GPIO.setup(23, GPIO.IN) #soil
GPIO.setup(22, GPIO.IN) #rain

sensor = Adafruit_DHT.DHT11
gpio = 18

host = "jjfaedp.hedevice.com"
#host = "192.168.0.12"
port = 876
DEV_ID = b'559451901'
AUTH_INFO = b'GPbHpXhSCwlYyIxfdxoMpcAYJKY='

relayStat = 0
motorStat = 0


pubkey, privkey = rsa.newkeys(1024)
#print("pubkey: ",pubkey)
#print("privkey: ",privkey)


def getSensorsData():
    global relayStat,motorStat
    #gas
    if GPIO.input(17):
        gasStat = 0
        print('Gas is closed')
    else:
        gasStat = 1
        print('Gas is triggered')
        
    #motion
    if GPIO.input(4):
        motionStat = 1
        print('Motion is triggered')
    else:
        motionStat = 0
        print('Motion is closed')
    
    #fire
    if GPIO.input(27):
        fireStat = 1
        print('Fire is triggered')
    else:
        fireStat = 0
        print('Fire is closed')
    
    #soil
    if GPIO.input(23):
        soilStat = 0
        print('Soil is closed')
    else:
        soilStat = 1
        print('Soil is triggered')    
    
    #rain
    if GPIO.input(22):
        rainStat = 0
        print('Rain is closed')
    else:
        rainStat = 1
        print('Rain is triggered')
    
    #relay
    if relayStat == 0:
        print('Relay is closed')
    else:
        print('Relay is opened')
    
    #motor
    if motorStat == 0:
        print('Motor is closed')
    else:
        print('Motor is opened')
        
    return gasStat,motionStat,fireStat,soilStat,rainStat,relayStat,motorStat
def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * 50) + (0.19 * 50 * angle / 180)
    return duty_cycle

def motorOn():
    pwm = GPIO.PWM(19, 50)
    pwm.start(0)
    for angle in range(0, 181, 15):
        dc = angle_to_duty_cycle(angle)
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.2)
    pwm.ChangeDutyCycle(angle_to_duty_cycle(90))
    pwm.stop()

def motorOff():
    pwm = GPIO.PWM(19, 50)
    pwm.start(0)
    for angle in range(180, -1, -15):
        dc = angle_to_duty_cycle(angle)
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.2)
    pwm.ChangeDutyCycle(angle_to_duty_cycle(90))
    pwm.stop()

def insert_localdb_temp(temp,humi,gas,motion,fire,soil,rain,relay,motor):
    # Connect to the database
    conn=sqlite3.connect('local.db')
    curs=conn.cursor()  
    # Insert database
    # strtemp = "%.1f" %(temp)
    # strhumi = "%.1f" %(humi)
    sql = "INSERT INTO sensordata(temperature,humidity,gas,motion,\
                                    fire,soil,rain,relay,motor) \
                                    VALUES(%.1f,%.1f,%.1f,%.1f,\
                                    %.1f,%.1f,%.1f,%.1f,%.1f)" \
                                    %(temp,humi,gas,motion,fire,soil,rain,relay,motor)
    curs.execute(sql)
    conn.commit()
    # Close the database
    conn.close()
    
def ping(c):
    while True:
        c.ping_req()
        time.sleep(30)

def edp_save_data(c):
    while True:
        hum_param,temp_param = Adafruit_DHT.read_retry(sensor,gpio)
        gas_param,motion_param,fire_param,soil_param,rain_param,relay_param,motor_param = getSensorsData()
        if temp_param is not None and hum_param is not None:
            print("Temp: %.1f, Humi: %.1f" %(temp_param,hum_param))
            insert_localdb_temp(temp_param,hum_param,gas_param,motion_param,\
                                fire_param,soil_param,rain_param,relay_param,motor_param)
        else:
            print("failed!")
            break
        '''
        dict = {"temp":{"temp":temp_param},"humi":{"humi":hum_param},\
                                           "gas":{"gas":gas_param},\
                                           "motion":{"motion":motion_param},\
                                           "fire":{"fire":fire_param},\
                                           "soil":{"soil":soil_param},\
                                           "rain":{"rain":rain_param},\
                                           "relay":{"relay":relay_param},\
                                           "motor":{"motor":motor_param}}
        '''
        dict = {"temp":temp_param,\
                "humi":hum_param,\
                "gas":gas_param,\
                "motion":motion_param,\
                "fire":fire_param,\
                "soil":soil_param,\
                "rain":rain_param,\
                "relay":relay_param,\
                "motor":motor_param,\
                "reserved":False}
        data = json.dumps(dict)
        c.save_data(data, 3, b'521265215')
        #c.push_data(DEV_ID,data)
        print("send......")
        c.clear_packet()
        time.sleep(3)
        

    
def doRead(c, s):

    global relayStat,motorStat
    rlist = [s.sock]
    while True:
        r, w, e = select.select(rlist, [], [], 5)
        
        if not r:
            print('> > > > > >')
            continue
        else:
            for sock in r:
                if sock is s.sock:
                    c.read_packet()
                    type = c.edp_packet_type()
                    print("Type :",type)
                    if type == CONN_RESP:
                        print("<<CONN_RESP")
                    elif type == CONN_CLOSE:
                        print("<<CONN_CLOSE")
                        c.handle_conn_resp()
                    elif type == CMD_REQ:
                        print("<<CMD_REQ")
                        (cmdid, cmd_len, msg, msg_len) = c.handle_cmd_req()
                        print('command is: ',msg)
                        if b'01' in msg:
                            GPIO.output(24, GPIO.HIGH)   #relay on
                            relayStat = 1
                        elif b'00' in msg:
                            GPIO.output(24, GPIO.LOW)   #relay off
                            relayStat = 0
                        elif b'11' in msg:
                            motorOn()   #motor on
                            motorStat = 1
                        elif b'10' in msg:
                            motorOff()   #motor off
                            motorStat = 0
                        else:
                            print("command error!")
                    elif type == SAVE_ACK:
                        print("<<SAVE_ACK")
                        #(desc_len, desc) = c.handle_save_ack()
                        #print('result is: ',desc)
                    elif type == SAVE_DATA:
                        print("<<SAVE_DATA")
                        comm = c.handle_save_data()
                        print('command is: ',comm)
                        if b'01' in comm:
                            GPIO.output(24, GPIO.HIGH)   #relay on
                            relayStat = 1
                        elif b'00' in comm:
                            GPIO.output(24, GPIO.LOW)   #relay off
                            relayStat = 0
                        elif b'11' in comm:
                            motorOn()   #motor on
                            motorStat = 1
                        elif b'10' in comm:
                            motorOff()   #motor off
                            motorStat = 0
                        else:
                            print("command error!")
                    elif type == PING_RESP:
                        print("<<PING_RESP")
                    elif type == ENCRYPT_RESP:
                        print("<<ENCRYPT_RESP")
                        c.handle_encrypt_resp(privkey)
                        print("Conn_req...")
                        c.conn_req()
                    else:
                        print("not done or unknown type")
                        break


        

if __name__ == '__main__':
    
    num = input('Is encrypted communication required?(y/n) :')
    if 'y' in num:
        ENCRYPT = 1
    else:
        ENCRYPT = 0
    
    sock = mysocket()
    client = Client(sock, DEV_ID, AUTH_INFO, ENCRYPT)
    sock.connect(host, port)
    
    if(ENCRYPT):
        print("encrypt_req...")
        #e = 65537
        #n = 117328402135096170106152357914549095523453759831388217240185185841168796097712968814522417228794746573726966269617101507900395038257114361036891534296708984823782519153687509968406430941813383029954297617320888962598592020478171876013816045615396003586291784557126513968024257417205205465334935528226652226509
        client.encrypt_req(pubkey.e,pubkey.n)
    else:
        print("Conn_req...")
        client.conn_req()
    #doRead(client,sock)
    
    t1 = threading.Thread(args=(client, sock), target=doRead)
    #t2 = threading.Thread(args=(client,), target=ping)
    t3 = threading.Thread(args=(client,), target=edp_save_data)

    t1.start()
    #t2.start()
    t3.start()

    t1.join()
    #t2.join()
    t3.join()

    
    GPIO.cleanup()
