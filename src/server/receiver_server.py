#!/usr/bin/python

EXTERNAL_DEBUG_MODE = 1

import time
if EXTERNAL_DEBUG_MODE:
	from DBG_receiver import Receiver
else:
	from receiver import Receiver

# ************************** FUNCTIONS *********************
def readInt(highValue, lowValue):
	val = (highValue << 8) + lowValue
	return val

# *************************** MAIN *************************
data_directory = "~/Documents/home_sense_data/";

_rx = Receiver()
print "Waiting for messages"

if True:
#try:
	while True:
		while _rx.ready():
			data = _rx.get()
			if data[0] == int(0xFE) and len(data) >= 2:
				id_client = data[1]
				data.pop(0) # removes the 0XFE from data 
				data.pop(0) # removes the id_client from data
				f = open(data_directory + str(id_client), 'w')
				print "Message received from " + str(id_client)
				print "Light = " + str(readInt(data[2], data[3]))
				print "Moisture = " + str(readInt(data[4], data[5]))
				f.write(data)
				f.close()

		time.sleep(2)
#except:
#	print "An error has occured"
#	pass

_rx.close()

print "Receiver is closed"
