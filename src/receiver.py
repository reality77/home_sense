import vw
import pigpio

LED_COM_RX = 12
LED_COM_BPS = 2000

class Receiver:

    def __init__(self):
	self.pi = pigpio.pi()
	self.rx = vw.rx(self.pi, LED_COM_RX, LED_COM_BPS)

    def ready(self):
	return self.rx.ready()

    def get():
	return self.rx.get()

    def close():
	self.rx.cancel()
	self.pi.stop()
