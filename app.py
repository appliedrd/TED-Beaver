from flask import Flask, render_template,request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)
GPIO.setup(Relay_Ch3,GPIO.OUT)

valveState = 0


@app.route('/')
def index():
    return render_template('index.html', valveState="closed")


@app.route('/open', methods=['POST', 'GET'])
def open():
    try:
        GPIO.output(Relay_Ch1,GPIO.HIGH)
        #Control the Channel 1
        GPIO.output(Relay_Ch2,GPIO.LOW)
        time.sleep(0.5)
        
        GPIO.output(Relay_Ch2,GPIO.HIGH)
        print("Valve is open\n")
    except:
        print("except")
        GPIO.cleanup()
    return render_template('index.html', valveState="open")

@app.route('/close', methods=['POST', 'GET'])
def close():
    try:
        GPIO.output(Relay_Ch2,GPIO.HIGH)
        #Control the Channel 1
        GPIO.output(Relay_Ch1,GPIO.LOW)
        time.sleep(0.5)      
        GPIO.output(Relay_Ch1,GPIO.HIGH)
        print("Valve is closed\n")
    except:
        print("except")
        GPIO.cleanup()
    return render_template('index.html', valveState="closed")

if __name__ == '__main__':
    app.run()
