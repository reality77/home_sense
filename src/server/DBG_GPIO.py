class GPIO:
	def __init__(self):
		self.IN = 0
		self.OUT = 1
		self.BOARD = 0
		self.BCM = 1
		self.PUD_DOWN = 0
		self.PUD_UP = 1

	def setmode(self, val):
		print "GPIO - Set Mode : " + str(val)
		return

	def setup(pin, direction, pulldown):
		print "GPIO setup pin \#" + str(pin) + " - mode : " + str(direction)
		return

	def add_event_detect(pin, event, callback, bouncetime):
		print "GPIO event NO SET for pin \#" + str(pin)

	def cleanup():
		print "GPIO cleanup"
