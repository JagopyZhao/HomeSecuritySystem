# HomeSecuritySystem
This codes builds a real-time home security system based on the OneNet cloud platform to control the status of house through a smartphone. The system consists of a local part and a cloud part. The local part has I/O devices, router and Raspberry Pi (RPi) that collects and monitors sensor data and sends the data to the cloud, and the Flask web server is implemented on a Rasberry Pi. When a user is at home, the user can access the Flask web server to obtain the data directly. The cloud part is OneNet in China Mobile, which provides remote access service. The hybrid App is designed to provide the interaction between users and the home security system in the smartphone, and the EDP and RTSP protocol is implemented to transmit data and video stream. Experimental results show that users can receive sensor data and warning text message through the smartphone and monitor and control home status through OneNet cloud.

### (add img)

 * ### Run the following commands on the Raspberry Pi
```Bash
$ git clone https://github.com/JagopyZhao/HomeSecuritySystem.git
$ cd HomeSecuritySystem/RasberryPi/OneNet/
```
 * ##### The following script is used to connect to OneNet.After running sen-edp.py, you can send data to OneNet and obtain commands to control the device.
```Bash
$ sudo python3 send-edp.py
```

