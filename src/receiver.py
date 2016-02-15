import vw
import pigpio

LED_COM_RX = 20
LED_COM_BPS = 2000

class Receiver:

    def __init__(self):
	self.pi = pigpio.pi()
	self.rx = vw.rx(self.pi, LED_COM_RX, LED_COM_BPS)

    def ready(self):
	return self.rx.ready()

    def get(self):
	return self.rx.get()

    def close(self):
	self.rx.cancel()
	self.pi.stop()

if __name__ == "__main__":

    try:
	import time

	_rx = Receiver()

	while True:
		#print "Waiting for receive..."
		while _rx.ready():
			print("=> " + "".join(chr(c) for c in _rx.get()))
		time.sleep(0.1)  
    except:
	pass

    _rx.close()
