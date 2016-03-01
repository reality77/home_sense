#!/usr/bin/python

# Thanks to contributors of https://github.com/googlemaps/google-maps-services-python

from datetime import datetime
from datetime import timedelta
import time
import json

with open('config.json') as json_data_file:
    config = json.load(json_data_file)['busgo']

API_CALL_DELAY = 30

class BusGo:

    def __init__(self):
	global config
        self.address = config['gmaps_directions'][0]['target_address']
        self.ledData = None
 
    # **************** Maps API
    def getMinutesLeft(self, departure) :
        return 5

    # **************** Select button
    def onSelect(self):
        self.lastApiCallTimer = None
         #Evolution : plusieurs destinations (changer self.address et retourner nom de ligne sur ecran alphanumerique
        return "G"
        
    # **************** Running
    def onRun(self, timerSec):
    
        # Appel API
        if (self.lastApiCallTimer is None) or (timerSec - self.lastApiCallTimer > API_CALL_DELAY) :
            self.loopCount = 0;
            self.minutesLeft0 = 6
            self.minutesLeft1 = 14
            self.lastApiCallTimer = timerSec
            print "Minutes left 0 : " + str(self.minutesLeft0)
            print "Minutes left 1 : " + str(self.minutesLeft1)

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
        self.lastCalledTimerSec = timerSec

        return False

    # **************** Stopping
    def onStop(self):
        return
        
    # **************** LED Data
    def getLedData(self):
        return self.ledData;    
    
# ****************************** TEST **************************

if __name__ == "__main__":

    _busgo = BusGo()

    _busgo.onSelect()
    _busgo.onRun(1)
    leddata = _busgo.getLedData()
  
    print leddata  
    print "Has Led Data ? : " + str(not(leddata is None))

    
