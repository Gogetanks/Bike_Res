from flask import Flask, flash, request, redirect, url_for, session, escape, send_file
from werkzeug.utils import secure_filename
import os
import RPi.GPIO as GPIO

IP_ADDRESS = '172.16.7.2'
LED_LOCKED_RED = 22
LED_UNLOCKED_GREEN = 27
#BTN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_LOCKED_RED, GPIO.OUT)
GPIO.setup(LED_UNLOCKED_GREEN, GPIO.OUT)
#GPIO.setup(BTN, GPIO.IN)

GPIO.output(LED_LOCKED_RED, GPIO.HIGH)
GPIO.output(LED_UNLOCKED_GREEN, GPIO.LOW)

app = Flask(__name__)


@app.route('/api/ping')
def ping():                                                                                          
    return '{ "' + IP_ADDRESS + '" : "OK" }' 

@app.route('/api/is_locked')
def isLocked():
    if GPIO.input(LED_LOCKED_RED) and not GPIO.input(LED_UNLOCKED_GREEN):
        return '{ "' + IP_ADDRESS + '" : "True" }'
    else:
        return '{ "' + IP_ADDRESS + '" : "False"}'
 
@app.route('/api/lock')
def lock():
    GPIO.output(LED_LOCKED_RED, GPIO.HIGH)
    GPIO.output(LED_UNLOCKED_GREEN, GPIO.LOW)
    if GPIO.input(LED_LOCKED_RED) and not GPIO.input(LED_UNLOCKED_GREEN):
        print('Bike is locked')
        return '{ "' + IP_ADDRESS + '" : "OK" }'
    else:
        print('ERROR: Bike is not locked')
        return '{ "' + IP_ADDRESS + '" : "FAIL" }'

@app.route('/api/unlock')
def unlock():                                                  
    GPIO.output(LED_LOCKED_RED, GPIO.LOW)
    GPIO.output(LED_UNLOCKED_GREEN, GPIO.HIGH)
    if not GPIO.input(LED_LOCKED_RED) and GPIO.input(LED_UNLOCKED_GREEN):
    	print('Bike is unlocked')             
    	return '{ "' + IP_ADDRESS + '" : "OK" }'
    else:
        print('ERROR: Bike is locked')
        return '{ "' + IP_ADDRESS + '" : "FAIL" }'

if __name__ == '__main__':
   app.run(debug=False, port=89, host=IP_ADDRESS)
