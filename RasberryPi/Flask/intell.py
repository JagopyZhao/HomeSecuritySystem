from flask import Flask,Response
#uncomment below to use Raspberry Pi camera instead
#from camera_pi import Camera
#comment this out if you're not using USB webcam
from camera_pi import Camera
app =Flask(__name__)
@app.route('/')
def index():
    return "hello world!"
def gen(camera):
    while True:
        frame = camera.get_frame()
#        yield frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/image.jpg')
def image():

    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, threaded=True)