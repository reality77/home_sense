import urllib2, urllib, json

DELAY = 30

COLOR_VIOLET = [0xFF, 0x00, 0xFF]
COLOR_LIGHT_VIOLET = [0x88, 0x00, 0xFF]
COLOR_BLUE = [0x00, 0x00, 0xFF]
COLOR_LIGHT_BLUE = [0x44, 0x66, 0xFF]
COLOR_GREEN_BLUE = [0x00, 0xFF, 0xFF]
COLOR_GREEN = [0x00, 0xFF, 0x33]
COLOR_YELLOW_GREEN = [0x88, 0xFF, 0x00]
COLOR_YELLOW = [0xFF, 0xDD, 0x00]
COLOR_ORANGE = [0xFF, 0x77, 0x00]
COLOR_RED = [0xFF, 0x00, 0x00]

COLORS = [COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_YELLOW_GREEN, COLOR_GREEN, COLOR_GREEN_BLUE, COLOR_LIGHT_BLUE, COLOR_BLUE, COLOR_LIGHT_VIOLET, COLOR_VIOLET]
INDEX = 0

#****************************************************************

class TestLed:
	def __init__(self):
		return

	def onRun(self, timerSec):
		global COLORS, INDEX, CALL_DELAY
		if (self.lastApiCallTimer is None) or (timerSec - self.lastApiCallTimer > DELAY):
                        self.lastApiCallTimer = timerSec
			INDEX = INDEX + 1
			if INDEX == len(COLORS):
				INDEX = 0
			color = COLORS[INDEX]
			data = [0x02, 0x03]
			data.extend(color)
			self.ledData = bytearray(data)
			return True
		else:
			return False

	def onSelect(self):
		self.lastApiCallTimer = None
		return "T"

	def getLedData(self):
		return self.ledData

	def onStop(self):
		return

#--------------------------
if __name__ == '__main__':

	w = TestLed()
	w.onSelect()
	w.onRun(1)
	print w.getLedData()

