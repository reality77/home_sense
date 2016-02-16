import time

LED_COM_RX = 20
LED_COM_BPS = 2000

class Receiver:

    def __init__(self):
	print "Receiver --- debug mode - no active communication"
	return

    def ready(self):
	print "Sleeping 2 secs before ready"
	time.sleep(2)
	return True

    def get(self):
	light = 770
	humidity = 365
	data = bytearray()
	data.append(0xFE) # "sensor" mode for server
	data.append(0x01) # sensor id
	data.append(light >> 8) # light sensor value (high)
	data.append(light ^ (data[2] << 8)) # light sensor value (low)
	data.append(humidity >> 8) # moisture sensor value (high)
	data.append(humidity ^ (data[4] << 8)) # moisture sensor value (low)
	return data

    def close(self):
	print "Closed"

if __name__ == "__main__":

    if True:
    #try:
	import time

	_rx = Receiver()

	while True:
		#print "Waiting for receive..."
		while _rx.ready():
			print("=> " + "".join(chr(c) for c in _rx.get()))
		time.sleep(0.1)
    #except:
	#pass

    _rx.close()
