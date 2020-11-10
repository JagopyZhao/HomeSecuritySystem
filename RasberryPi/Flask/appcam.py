from flask import Flask, render_template, Response, request
app = Flask(__name__)
 
import cv2
import json
 
import Adafruit_DHT
import time
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)   #relay
GPIO.setup(19, GPIO.OUT)   #motor

GPIO.setup(17, GPIO.IN) #gas
GPIO.setup(4, GPIO.IN) #motion
GPIO.setup(27, GPIO.IN) #fire
GPIO.setup(23, GPIO.IN) #soil
GPIO.setup(22, GPIO.IN) #rain

relayStat = 0
motorStat = 0

# get data from DHT sensor
def getDHTdata():      
    sensor = Adafruit_DHT.DHT11
    gpio = 18
    hum, temp = Adafruit_DHT.read_retry(sensor,gpio)
     
    if hum is not None and temp is not None:
        print("Temp: %.1f, Humidity: %.1f" %(temp,hum))
    return temp,hum
    
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
        time.sleep(0.1)
    pwm.stop()


def motorOff():
    pwm = GPIO.PWM(19, 50)
    pwm.start(0)
    for angle in range(180, -1, -15):
        dc = angle_to_duty_cycle(angle)
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.1)
    pwm.stop()


@app.route("/index",methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/getSensorsData',methods=['GET'])
def getnew_temperature():
    #timeNow_parameter = time.asctime( time.localtime(time.time()))
    #print("Current Time: ",timeNow_parameter)
    temp_param, hum_param = getDHTdata()
    gas_param,motion_param,fire_param,soil_param,rain_param,relay_param,motor_param = getSensorsData()
    
    updata_parameter = {
      'temp': temp_param,
      'humi': hum_param,
      'gas': gas_param,
      'motion': motion_param,
      'fire': fire_param,
      'soil': soil_param,
      'rain': rain_param,
      'relay': relay_param,
      'motor': motor_param
    }
    return json.dumps(updata_parameter)

@app.route('/new_echart',methods=['GET'])
def getnew_echart():
    timeNow_echart = time.asctime( time.localtime(time.time()))
    print("Current Time: ",timeNow_echart)
    temp_echart, hum_echart = getDHTdata()
    updata_echart = {
      'time': timeNow_echart,
      'temp': temp_echart,
      'humi' : hum_echart
    }
    return json.dumps(updata_echart)

@app.route('/ctl_cmd',methods=['POST'])
def control():
    global relayStat,motorStat
    data = json.loads(request.form.get('data'))
    cmd = str(data)
    if 'relay' in cmd:
        if 'on' in cmd:
            GPIO.output(24, GPIO.HIGH)   #relay on
            relayStat = 1                #closed
        else:
            GPIO.output(24, GPIO.LOW)   #relay off
            relayStat = 0               #triggered
    else:
        if 'on' in cmd:
            motorOn()          #motor on
            motorStat= 1       #closed               
        else:
            motorOff()         #motor off
            motorStat = 0      #triggered
            
    return 'OK'
 
@app.route('/camera')
def cam():
    return render_template('camera.html')

@app.route('/echarts')
def echart():
    return render_template('echarts.html')
 
class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)#"rtmp://***************"
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        success, image = self.cap.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

def gen(camera):
    """Video streaming generator function."""
    frameCount = 0
    while True:
        frame = camera.get_frame()
        frameCount += 1
        print(frameCount)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
 
 
if __name__ == '__main__':
    app.run(host='192.168.0.20', port =5000, debug=True)#, threaded=True,ssl_context=('server.crt', 'server.key')
