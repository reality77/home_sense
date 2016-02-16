#!/usr/bin/python

EXTERNAL_DEBUG_MODE = 0

import time
import json

if EXTERNAL_DEBUG_MODE:
	from DBG_receiver import Receiver
else:
	from receiver import Receiver

with open('config.json') as json_data_file:
	config = json.load(json_data_file)['server']

# ************************** FUNCTIONS *********************
def readInt(highValue, lowValue):
	val = (highValue << 8) + lowValue
	return val

# *************************** MAIN *************************
data_directory = config['data_directory'];

_rx = Receiver()
print "Waiting for messages"

if True:
#try:
	while True:
		while _rx.ready():
			print "ready"
			data = _rx.get()
			if data[0] == int(0xFE) and len(data) >= 2:
				id_client = data[1]
				data.pop(0) # removes the 0XFE from data 
				data.pop(0) # removes the id_client from data
				f = open(data_directory + str(id_client), 'w')
				print "Message received from " + str(id_client)
				print "Light = " + str(readInt(data[0], data[1]))
				print "Moisture = " + str(readInt(data[2], data[3]))
				f.write(bytearray(data))
				f.close()

		time.sleep(5)
#except:
#	print "An error has occured"
#	pass

_rx.close()

print "Receiver is closed"
