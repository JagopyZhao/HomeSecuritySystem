#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sqlite3
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
gpio = 18

times = 0
 
def get_cpu_temp():
    _,temp = Adafruit_DHT.read_retry(sensor,gpio)
    return temp
 
def insert_cpu_temp(temp):
    # 连接数据库
    global times
    times = times + 1
    print("type(temp):",type(temp))
    print("temp:",temp)
    print("times:",times)
    
    conn=sqlite3.connect('cpu.db')
    curs=conn.cursor()  
    # 插入数据库
    strtemp = "%.1f" %(temp);
    curs.execute("INSERT INTO temps(temperature) VALUES((?))", (strtemp,))
    conn.commit()
    # 关闭数据库
    conn.close()
 
def main():
    while True:
        temp = get_cpu_temp()
        insert_cpu_temp(temp)
        time.sleep(10) 
 
if __name__ == '__main__':
    main()