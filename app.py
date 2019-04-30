from flask import Flask, render_template,request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

#setup 
Relay_Ch1 = 26
Relay_Ch2 = 20
Relay_Ch3 = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

GPIO.setup(Relay_Ch1,GPIO.OUT)
GPIO.setup(Relay_Ch2,GPIO.OUT)
GPIO.setup(Relay_Ch3,GPIO.OUT)

valveState = 0

#GPIO.setmode(GPIO.BOARD)
#pir = 8                             #Assign pin 8 to PIR
#led = 10                            #Assign pin 10 to LED
# GPIO.setmode(GPIO.BCM)
pir = 14                             #Assign pin 8 to PIR
led = 15                            #Assign pin 10 to LED
GPIO.setup(pir, GPIO.IN)            #Setup GPIO pin PIR as input
GPIO.setup(led, GPIO.OUT)           #Setup GPIO pin for LED as output

pir_enabled=1
pir_counter = 0
time_motion_detected = -999
elapsed = 999
motion_grace_window = 10


@app.route('/')
def index():
    return render_template('index.html', valveState="closed")


@app.route('/open', methods=['POST', 'GET'])
def open(motion_state="no motion"):
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
    return render_template('index.html', valveState="open", motion=motion_state)

@app.route('/close', methods=['POST', 'GET'])
def close():
    global time_motion_detected  
    try:
        GPIO.output(Relay_Ch2,GPIO.HIGH)
        #Control the Channel 1
        GPIO.output(Relay_Ch1,GPIO.LOW)
        time.sleep(0.5)      
        GPIO.output(Relay_Ch1,GPIO.HIGH)
        print("Valve is closed\n")
        time_motion_detected = time.time()
    except:
        print("except")
        GPIO.cleanup()
    return render_template('index.html', valveState="closed", motion="enabled")

def render_with_context(template, _url='/', **kw):
    with app.test_request_context(_url):
        return render_template(template, **kw)


def pir_callback(channel):
    global elapsed, time_motion_detected, motion_grace_window, pir_counter
    print("checking for Movement...")
    if pir_enabled == 1:
        time.sleep(1)  # confirm the movement by waiting 1.5 sec
        if GPIO.input(pir): # and check again the input
            elapsed = time.time()- time_motion_detected
            print("Movement!")
            print(elapsed)
            if elapsed > motion_grace_window:
                time_motion_detected = time.time()
                print("actionable movement!")
                pir_counter=pir_counter+1
                #render_template('index.html', valveState="open", motion="motion detected")
                #open("motion detected")
                render_with_context('index.html', valveState="open", motion="motion detected")
            

GPIO.add_event_detect(pir, GPIO.RISING, callback=pir_callback, bouncetime=300)

if __name__ == '__main__':
    app.run()
