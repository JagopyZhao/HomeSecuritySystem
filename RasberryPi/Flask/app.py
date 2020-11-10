from flask import Flask, render_template, Response
app = Flask(__name__)
 
import cv2
 
import Adafruit_DHT
import time
import json
import RPi.GPIO as GPIO   #导入树莓派提供的python模块

GPIO.setmode(GPIO.BCM)   #设置GPIO模式，BCM模式在所有数码派通用
GPIO.setup(24, GPIO.OUT)   #设置GPIO18为电流输出
 
# get data from DHT sensor
def getDHTdata():       
    sensor = Adafruit_DHT.DHT11
    gpio = 18
    hum, temp = Adafruit_DHT.read_retry(sensor,gpio)
     
    if hum is not None and temp is not None:
        print("Temp: %.1f, Humidity: %.1f" %(temp,hum))
    return temp,hum
	
#@app.route('/gpio/<int:id>',methods=['POST'])
#def gpio_led(id):
#	if request.method == 'POST':
#		GPIO.setmode(GPIO.BOARD)
#		if id<100:
#			GPIO.setup(id,GPIO.OUT)
#			GPIO.setmode(GPIO.BOARD)
#			GPIO.setup(id,GPIO.OUT)
#			GPIO.output(id,False)
#		else:
#			GPIO.setup(id-100,GPIO.OUT)
#			GPIO.output(id-100,True)
#	return redirect(url_for('show_index'))

 
 
@app.route("/index",methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/new_parameter',methods=['GET'])
def getnew_temperature():
    timeNow_parameter = time.asctime( time.localtime(time.time()))
    print("Current Time: ",timeNow_parameter)
    temp_parameter, hum_parameter = getDHTdata()
    updata_parameter = {
      'time': timeNow_parameter,
      'temp': temp_parameter,
      'humi' : hum_parameter
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

@app.route('/on',methods=['GET'])
def getnew_on():
    GPIO.output(24, GPIO.HIGH)   #GPIO18 输出3.3V
    return 'OK'

@app.route('/off',methods=['GET'])
def getnew_off():
    GPIO.output(24, GPIO.LOW)   #GPIO18 输出3.3V
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
    app.run(host='192.168.0.4',port=40960,debug=False)#, threaded=True,ssl_context=('server.crt', 'server.key')
