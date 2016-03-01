#!/usr/bin/python

# Thanks to contributors of vw.py (https://github.com/joan2937/pigpio) 

"""
TODO : 
- When clicking the MODE button, don't change the mode directly  
but for the first click on the SELECT button to change it
- Receiver management
"""
import json

with open('config.json') as json_data_file:
	config = json.load(json_data_file)['server']
EXTERNAL_DEBUG_MODE = config['external_debug_mode']


if EXTERNAL_DEBUG_MODE:
    from DBG_led_communication import LedCommunication
    from DBG_receiver import Receiver
    import DBG_GPIO as GPIO
    from DBG_busgo import BusGo
else:
    from led_communication import LedCommunication
    from receiver import Receiver
    import RPi.GPIO as GPIO
    from busgo import BusGo

from datetime import datetime
from datetime import timedelta
import time
import os
import json
from weather import Weather
from testled import TestLed
from sensor import Sensor
from timer_check import TimerCheck

#********************* Init GPIO
#led_working = 19
#led_power = 22
button_select_in = 19
button_mode_in = 26

GPIO.setmode(GPIO.BCM)
#GPIO.setup(led_power, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.setup(led_working, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(button_select_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_mode_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#********************* Init global variables
with open('config.json') as json_data_file:
	config = json.load(json_data_file)['server']

ready_to_shutdown = False
current_mode = 0
automatic_mode = 1

_timerCheck = TimerCheck()

MODE__MIN = 0
MODE_STOP = 0
MODE_TESTLED = 1
MODE_BUSGO = 2
MODE_WEATHER = 3
MODE_SENSOR = 4
MODE__MAX = 4

MAX_SEND_RETRIES = 3

_oBusgo = BusGo()
_oTestled = TestLed()
_oWeather = Weather()
_oSensor = Sensor()

_ledComm = LedCommunication()
_rx = Receiver()

_current = None
_old = None

# **************** Shutdown button
def button_select_click(channel):
    global current_mode, ready_to_shutdown
    if current_mode == MODE_STOP:
        if not ready_to_shutdown :
            display("STP?")
            ready_to_shutdown = True
        else :
            display("SHUT")
	    if not(EXTERNAL_DEBUG_MODE):
		GPIO.cleanup()
	        os.system("shutdown now -h")
	    else:
		print("DEBUG : SHUTDOWN BUTTON CLICKED")
	    exit
    else :
        if not(_current is None):
            _current.onSelect()

# **************** Mode button
def button_mode_click(channel):
    global current_mode
    mode = current_mode
    mode += 1
    if mode > MODE__MAX:
        mode = MODE__MIN
    changeMode(mode)

# **************** Mode button
def changeMode(mode):
    global current_mode, ready_to_shutdown, _old, _current, ledstrip_data, ledstrip_retry
    automatic_mode = 0
    ready_to_shutdown = False

    if mode == current_mode:
	return 0

    current_mode = mode

    _old = _current

    if not(_old is None):
        _old.onStop()

    if current_mode == MODE_STOP:
        display("STOP")
        _current = None
    elif current_mode == MODE_TESTLED:
        display("TEST")
        _current = _oTestled
    elif current_mode == MODE_BUSGO:
        display("BUS")
        _current = _oBusgo
    elif current_mode == MODE_WEATHER:
        display("WHTR")
        _current = _oWeather
    elif current_mode == MODE_SENSOR:
        display("SENS")
        _current = _oSensor

    if not(_current is None):
        disp = _current.onSelect()
        if not(disp is None) and disp != "":
            display(disp)
    ledstrip_data = None
    ledstrip_retry = 0
    return 1

def display(data):
    #TODO Affichage alphanumerique
    print("Display : " + data)

# **************** Working LED Functions
def startWorking() :
    #GPIO.output(led_working, GPIO.HIGH)
    return

def stopWorking() :
    #GPIO.output(led_working, GPIO.LOW)
    return

# **************************** MAIN *******************

#test
#_current = _oTestled
#_current.onSelect()
#fin test

GPIO.add_event_detect(button_select_in, GPIO.RISING, callback=button_select_click, bouncetime=500)
GPIO.add_event_detect(button_mode_in, GPIO.RISING, callback=button_mode_click, bouncetime=500)

TOTAL_SLEEP = 2

if True:
#try :
    print "Starting main program"
    
    timer_start = datetime.now()
    timer_current = 0
    timer_lastloop = 0
    ledstrip_data = None
    ledstrip_retry = 0
    while 1:

        timer_current = datetime.now()

	if automatic_mode:
	    timerData = _timerCheck.check()
	    if not(timerData is None):
	    	# Auto-mode activated
		mode = int(timerData['mode'])
	    	if changeMode(mode):
		    print "Automatic mode changed"
	    else:
		# Auto-mode stopped
		if current_mode != MODE_STOP:
		    changeMode(MODE_STOP)
		    print "Automatic mode stopped"

        if not(_current is None):
            print "Running"
            startWorking()
            if _current.onRun((datetime.now() - timer_start).total_seconds()):
                ledstrip_data = _current.getLedData()
                ledstrip_retry = 0
            stopWorking()

        if ledstrip_retry < MAX_SEND_RETRIES:
            print "LED retry : " + str(ledstrip_retry)
            ledstrip_retry = ledstrip_retry + 1
            if not(ledstrip_data is None):
                _ledComm.sendLedColors(ledstrip_data)
                print "Sent to LED"
            else:
                _ledComm.sendLedReset()
                print "LED Reset"

        delta = (datetime.now() - timer_current)
        sleepduration = (delta.total_seconds() + delta.microseconds / 1000000)

        if sleepduration < TOTAL_SLEEP:
            print "Sleep : " + str(TOTAL_SLEEP - sleepduration)
            time.sleep(TOTAL_SLEEP - sleepduration)
        else:
            print "No sleep"
        timer_lastloop = timer_current
#except:
    try:
        if not(_current is None):
            _current.onStop()
        display("ERR")

	_rx.close()
        
        # 3 attempts to light off the led strip
        _ledComm.sendLedReset()
        sleep(2)
        _ledComm.sendLedReset()
        sleep(2)
        _ledComm.sendLedReset()
    except:
        pass

GPIO.cleanup()
