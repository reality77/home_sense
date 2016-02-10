import vw

LED_COM_RX = 20
LED_COM_BPS = 2000

class Receiver:

    def __init__(self):
	return

    def setPi(self, pi):
	self.rx = vw.rx(pi, LED_COM_RX, LED_COM_BPS)

    def ready(self):
	return self.rx.ready()

    def get(self):
	return self.rx.get()

    def close(self):
	self.rx.cancel()

if __name__ == "__main__":

    try:
	import pigpio
	import time

	pi = pigpio.pi() 
	_rx = Receiver()
	_rx.setPi(pi)

	while True:
		#print "Waiting for receive..."
		while _rx.ready():
			print("=> " + "".join(chr(c) for c in _rx.get()))
		time.sleep(0.1)  
    except:
	pass

    _rx.close()
    pi.stop()
