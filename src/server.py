#!/usr/bin/python

# Thanks to contributors of vw.py (https://github.com/joan2937/pigpio) 

"""
TODO : 
- When clicking the MODE button, don't change the mode directly  
but for the first click on the SELECT button to change it
- Receiver management
"""

from datetime import datetime
from datetime import timedelta
import RPi.GPIO as GPIO
import time
import os
from busgo import BusGo
from led_communication import LedCommunication
from weather import Weather
from receiver import Receiver
from testled import TestLed

#********************* Init GPIO
#led_working = 19
#led_power = 22
#button_select_out = 21
button_select_in = 19
#button_mode_out = 0 #TODO
button_mode_in = 26

GPIO.setmode(GPIO.BCM)
#GPIO.setup(led_power, GPIO.OUT, initial=GPIO.HIGH)
#GPIO.setup(led_working, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(button_select_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button_mode_in, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#********************* Init global variables
ready_to_shutdown = False
current_mode = 0

MODE__MIN = 0
MODE_STOP = 0
MODE_TESTLED = 1
MODE_BUSGO = 2
MODE_WEATHER = 3
MODE_GASPARD = 4
MODE__MAX = 4

MAX_SEND_RETRIES = 3

_oBusgo = BusGo()
_oTestled = TestLed()
_oWeather = Weather()
_oMoisture = TestLed()

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
            GPIO.cleanup()
            os.system("shutdown now -h")
            exit
    else :
        if not(_current is None):
            _current.onSelect()

# **************** Mode button
def button_mode_click(channel):
    global current_mode, ready_to_shutdown, _old, _current, ledstrip_data, ledstrip_retry
    current_mode += 1
    ready_to_shutdown = False
    if current_mode > MODE__MAX:
        current_mode = MODE__MIN
    
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
    elif current_mode == MODE_GASPARD:
        display("HUM")
        _current = _oMoisture

    disp = _current.onSelect()
    if not(disp is None) and disp != "":
    	display(disp)    
    ledstrip_data = None
    ledstrip_retry = 0
    
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
_current = _oTestled
_current.onSelect()
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
            

	while _rx.ready():
	    print("".join(chr (c) for c in _rx.get()))

        delta = (datetime.now() - timer_current)
        sleepduration = delta.total_seconds() * 1000 + delta.microseconds / 1000

        print sleepduration

        if sleepduration < 1000:
            time.sleep(TOTAL_SLEEP - sleepduration / 1000.0)
            print "Sleep : " + str(TOTAL_SLEEP - sleepduration / 1000.0)
        else:
            print "No sleep"
        timer_lastloop = timer_current;   

        time.sleep(TOTAL_SLEEP)
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
