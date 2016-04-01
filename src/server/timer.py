#!/usr/bin/python

from datetime import datetime
from datetime import timedelta
import math
import time
import json

REFRESH_DELAY = 10 # 10 seconds

with open('config.json') as json_data_file:
    config = json.load(json_data_file)['timer']

class Timer:

    def __init__(self):
	global config
	self.lastApiCallTimer = None
	self.timerArray = config['timers']
	self.timerIndex = -1
	self.dateTimer = None
        self.ledData = None
 
    # **************** Select button
    def onSelect(self):

	self.lastApiCallTimer = None

	if self.timerIndex < 0:
		self.timerIndex = 0
	else:
		self.timerIndex = self.timerIndex + 1

	if self.timerIndex >= len(self.timerArray):
		self.timerIndex = -1

	if self.timerIndex >= 0:
		timer = self.timerArray[self.timerIndex]
		self.dateTimer = datetime.now() + timedelta(0, timer * 60)
	        return str(timer)
        else:
		self.dateTimer = None
		return "TIMR"
        
    # **************** Running
    def onRun(self, timerSec):

	delta = self.dateTimer - datetime.now()

	if (self.lastApiCallTimer is None) or (timerSec - self.lastApiCallTimer > REFRESH_DELAY):
	    self.lastApiCallTimer = timerSec
	    minutesToGo = delta.total_seconds() / 60
   	    print "Delta (min) = " + str(delta.total_seconds() / 60)
   	    timer = self.timerArray[self.timerIndex]

	    if (minutesToGo > 5 * 60):
	        # [GREEN] If delta > 5 minutes => Progress bar style (30 LEDS = full time spent)
		ledcount = round((timer - minutesToGo) * 30 / timer)
	    else:
		# [YELLOW/ORANGE/RED] 1 LED = 10 seconds => 30 LEDS = 5 minutes
		ledcount = round((5 * 60 - delta.total_seconds) / (5 * 60))

	    print "ledcount = " + str(ledcount)

	    return False
            data = []

            if not (self.minutesLeft0 is None):

                for i in range(0, 150, 5):
                    current = 15 - i/10.0
                    #print current
                    if current <= self.minutesLeft0 :
                        x = self.minutesLeft0 - current 
                    elif not(self.minutesLeft1 is None):
                        x = self.minutesLeft1 - current 
                    #print x
                    if x < 0:
                        data.append('')
                        #print ''
                    elif x < 3:
                        data.append('V')
                        #print 'V'
                    elif x < 5:
                        data.append('B')
                        #print 'B'
                    elif x < 10:
                        data.append('I')
                        #print 'I'
                    else:
                        data.append('R')
                        #print 'R'

            #print data
            dataarray = [0x02]
            lastcolor = 'XXXX'
            counter = 0
            for color in reversed(data):
                if color == lastcolor :
                    counter += 1
                else:
                    
                    if counter > 0:
                        if lastcolor != '':
                            dataarray.append(counter)
                            if lastcolor == 'R':
                                dataarray.append(0xFF)
                                dataarray.append(0x00)
                                dataarray.append(0x00)
                            elif lastcolor == 'V':
                                dataarray.append(0x00)
                                dataarray.append(0xFF)
                                dataarray.append(0x00)
                            elif lastcolor == 'B':
                                dataarray.append(0x00)
                                dataarray.append(0x00)
                                dataarray.append(0xFF)
                            elif lastcolor == 'I':
                                dataarray.append(0xFF)
                                dataarray.append(0x00)
                                dataarray.append(0xFF)
                    counter = 1
                    lastcolor = color
            
            if counter > 0:
                if lastcolor != '':
                    dataarray.append(counter)
                    if lastcolor == 'R':
                            dataarray.append(0xFF)
                            dataarray.append(0x00)
                            dataarray.append(0x00)
                    elif lastcolor == 'V':
                            dataarray.append(0x00)
                            dataarray.append(0xFF)
                            dataarray.append(0x00)
                    elif lastcolor == 'B':
                            dataarray.append(0x00)
                            dataarray.append(0x00)
                            dataarray.append(0xFF)
                    elif lastcolor == 'I':
                            dataarray.append(0xFF)
                            dataarray.append(0x00)
                            dataarray.append(0xFF)

            print "Data = " + str(dataarray)
        
            self.ledData = bytearray(dataarray)

            return True
	else:
	    return False            
        
    # **************** Stopping
    def onStop(self):
        return
        
    # **************** LED Data
    def getLedData(self):
        return self.ledData;    
    
# ****************************** TEST **************************

if __name__ == "__main__":

    _timer = Timer()

    alpha = _timer.onSelect()
    print "Alpha LEDs : " + alpha
    time.sleep(5)
    _timer.onRun(1)
    leddata = _timer.getLedData()
  
    print leddata  
    print "Has Led Data ? : " + str(not(leddata is None))

    
