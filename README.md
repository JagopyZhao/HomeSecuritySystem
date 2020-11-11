# Home Security System
This codes builds a real-time home security system based on the OneNet cloud platform to control the status of house through a smartphone. The system consists of a local part and a cloud part. The local part has I/O devices, router and Raspberry Pi (RPi) that collects and monitors sensor data and sends the data to the cloud, and the Flask web server is implemented on a Rasberry Pi. When a user is at home, the user can access the Flask web server to obtain the data directly. The cloud part is OneNet in China Mobile, which provides remote access service. The hybrid App is designed to provide the interaction between users and the home security system in the smartphone, and the EDP and RTSP protocol is implemented to transmit data and video stream. Experimental results show that users can receive sensor data and warning text message through the smartphone and monitor and control home status through OneNet cloud.

![](https://github.com/JagopyZhao/HomeSecuritySystem/raw/master/Images/homeSecuritySystem.png) 

## Cloud Part
##### Before connecting to OneNet, you need DEV-ID and API-KEY, and log in to OneNet to create a device. Visit English website(https://open.iot.10086.cn/v4/en/). For convenience, DEV-ID and API-KEY are provided in the code, just for testing. If you find that you can’t connect, contact me: kivenzhao2020@163.com

```python
DEV_ID = '559451901'
AUTH_INFO = 'GPbHpXhSCwlY*************' 
```

 * ### Run the following commands on the Raspberry Pi
```Bash
$ git clone https://github.com/JagopyZhao/HomeSecuritySystem.git
$ cd HomeSecuritySystem/RasberryPi/OneNet/
```
#### The python script needs to import the following packages：
```python
import time
import struct
import json
import threading
import select
import sqlite3
import rsa
import Adafruit_DHT
import RPi.GPIO as GPIO 
```
#### You need to install them on the Raspberry Pi. Like pip install ...

#### The following script is used to connect to OneNet. After running sen-edp.py, you can send data to OneNet and obtain commands to control the device.
```Bash
$ sudo python3 send-edp.py
```
#### If the following situation occurs：
```Bash
Is encrypted communication required?(y/n) :
```
#### Enter y or n to choose whether to encrypt the communication data.

 * ### Run the following apk on your Android phone
 * HybridApp
     * RPiSmartHmoe_1111085234.apk
 
![](https://github.com/JagopyZhao/HomeSecuritySystem/raw/master/Images/controlPanel2.png)

#### After opening the app, you do not need to enter the IP, just click Real-time updated.     
#### If you can’t see the video, please refer to Video Part.

## Local Part
 * ### Run the following commands on the Raspberry Pi
```Bash
$ git clone https://github.com/JagopyZhao/HomeSecuritySystem.git
$ cd HomeSecuritySystem/RasberryPi/Flask/
```

#### The python script needs to import the following packages：
```python
from flask import Flask, render_template, Response, request
```
#### Run the following command to start flask：
```Bash
$ sudo python3 python3 appcam.py
```
#### Open the mobile app and enter the IP of the Raspberry Pi to receive data and send control device commands.

## Video Part 
#### Refer to the following github：
#### https://github.com/BreeeZe/rpos

