from flask import Flask

app = Flask(__name__)

print('__name__: ',__name__)



@app.route('/index')
def hello():
    return 'OK'

if __name__ == '__main__':
    app.run(host='192.168.0.12',port=5000)
